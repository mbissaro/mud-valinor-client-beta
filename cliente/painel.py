"""Painel do mapa: minimapa clicável, prévia da sala sob o mouse, /rota e /sala.

Mouse: passar por cima de uma sala abre a prévia (descrição, saídas e o caminho até lá); clique esquerdo traça a
rota, duplo clique traça e já manda o /andar, clique direito centraliza o mapa nela, a roda rola o texto. /andar manda a rota de uma vez quando você pede
(speedwalk, como um alias); nada de gatilho esperando a sala para mandar o próximo passo."""
from __future__ import annotations

import curses
import os
import re
import select
import sys
import textwrap
import time

import mapa
from conexao import WIN

MAP_STYLE = {"cur": "accent", "room": "text", "route": "route", "peek": "peek", "link": "dim", "far": "far",
             "new": "new"}
MOUSE_ON, MOUSE_OFF = b"\033[?1003h\033[?1006h", b"\033[?1003l\033[?1006l"  # todo movimento, formato SGR
SGR = re.compile(r"(\d+);(\d+);(\d+)([Mm])")
SGR_WAIT = 0.15  # segundos para o resto de um evento que chegou partido (ssh, terminal lento)
WHEEL = 3
DOUBLE_CLICK = 0.4  # segundos entre os dois cliques do duplo clique
MAX_WALK = 20  # passos por /andar: rajadas curtas, você olha a tela entre uma e outra
BAR = 8  # células da barrinha de hp/m/mv
PANEL_MIN_COLS = 90
DOCK_MIN, DOCK_MAX, TEXT_MIN = 36, 50, 80  # largura das colunas da direita e o mínimo que fica para o texto
DOCKS = ("mapa", "equip", "who")


def win_mouse() -> tuple[int, int, int, bool] | None:
    """Evento do PDCurses no formato do SGR: (botão, x, y, apertou). 0 esquerdo, 2 direito, 64/65 roda, 35 movimento."""
    try:
        _, x, y, _, st = curses.getmouse()
    except curses.error:
        return None
    for flag, b, press in (("REPORT_MOUSE_POSITION", 35, True), ("BUTTON1_PRESSED", 0, True), ("BUTTON1_CLICKED", 0, True),
                           ("BUTTON1_DOUBLE_CLICKED", 0, True), ("BUTTON1_RELEASED", 0, False),
                           ("BUTTON3_PRESSED", 2, True), ("BUTTON3_CLICKED", 2, True), ("BUTTON4_PRESSED", 64, True),
                           ("BUTTON5_PRESSED", 65, True)):  # movimento antes: arrastar não vira clique
        if st & getattr(curses, flag, 0):
            return b, x, y, press
    return None


def bar(v: int, mx: int, n: int = BAR) -> tuple[str, str]:
    """(parte cheia, parte vazia) de uma barra de n células, com meia célula de precisão."""
    halves = round(max(0.0, min(1.0, v / max(mx, 1))) * 2 * n)
    if 0 < v < mx:
        halves = min(max(halves, 1), 2 * n - 1)  # quase vazia ainda aparece, quase cheia ainda falta
    full = "━" * (halves // 2) + "╸" * (halves % 2)
    return full, "─" * (n - len(full))


def steps(n: int) -> str:
    return f"{n} passo" + ("" if n == 1 else "s")


NOWHERE = "não sei onde você está: dê um look numa sala que a base conhece"


class Painel:
    """Parte do App que cuida do mapa; usa base, th, put, say, push, room, center, target e route dele."""

    def set_mouse(self, on: bool) -> None:
        """1003 = o terminal manda também o movimento (para o hover); desligado, o terminal volta a selecionar texto.
        Sem curses.mousemask de propósito: o ncurses 6.2 descarta o movimento sem botão apertado. No Windows não há
        sequência de terminal: o PDCurses entrega o mouse pelo getmouse."""
        self.mouse_on = on
        if WIN:
            curses.mousemask((curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION) if on else 0)
            curses.mouseinterval(0)  # aperta e solta separados; o duplo clique é contado aqui (DOUBLE_CLICK)
        else:
            os.write(1, MOUSE_ON if on else MOUSE_OFF)

    def sgr_next(self) -> bool:
        """Terminfo cujo kmous não é o do SGR (macOS, TERM=screen no tmux): o evento chega como ESC [ < b;x;yM digitado.
        Depois de um ESC, olha se vem [<; se não, devolve as teclas para a fila e o ESC segue como Esc."""
        got, end = [], time.time() + SGR_WAIT
        for want in "[<":
            ch = self.get_ch(end)
            if ch is None:
                break
            got.append(ch)
            if ch != want:
                break
        else:
            return True
        for ch in reversed(got):
            curses.ungetch(ch) if isinstance(ch, int) else curses.unget_wch(ch)
        return False

    def get_ch(self, end: float) -> str | int | None:
        """Próxima tecla da fila; se o resto do evento ainda não chegou (ssh, terminal lento), espera até end."""
        while True:
            try:
                return self.scr.get_wch()
            except curses.error:
                left = end - time.time()
                if left <= 0 or not select.select([sys.stdin], [], [], left)[0]:
                    return None

    def read_mouse(self) -> tuple[int, int, int, bool] | None:
        """Depois do KEY_MOUSE (o ESC [ < do terminfo), o resto do evento SGR fica na fila: b;x;y e M (aperta) ou m."""
        if WIN:
            return win_mouse()
        s, end = "", time.time() + SGR_WAIT
        while len(s) < 16 and not s.endswith(("M", "m")):
            ch = self.get_ch(end)
            if not isinstance(ch, str):
                break
            s += ch
        m = SGR.fullmatch(s)
        return (int(m[1]), int(m[2]) - 1, int(m[3]) - 1, m[4] == "M") if m else None

    def on_mouse(self) -> None:
        ev = self.read_mouse()
        if not ev:
            return
        b, x, y, press = ev
        rid = self.hits.get((y, x))
        spot = next((v for (sy, x0, x1), v in self.spots.items() if sy == y and x0 <= x < x1), None)
        if b & 64:  # roda: 64 sobe, 65 desce
            self.scroll = max(0, self.scroll + (-WHEEL if b & 1 else WHEEL))
        elif b & 32:  # movimento, com ou sem botão
            if (rid, spot) == (self.hover, self.spot_hover):
                return
            self.hover, self.spot_hover, self.hover_y = rid, spot, y
        elif press and b & 3 == 0 and spot:
            self.spot_click(spot)
        elif press and b & 3 == 0 and rid:
            last, at = getattr(self, "last_click", (None, 0.0))
            double = rid == last and time.time() - at < DOUBLE_CLICK
            self.last_click = (None, 0.0) if double else (rid, time.time())
            if not double or self.target != rid:  # o 1º clique já traçou; sem isso o 2º apagaria a rota
                self.click(rid)
            if double and self.target == rid:
                self.cmd_andar()
        elif press and b & 3 == 2 and rid:
            self.center, self.hover = (None if rid == self.room else rid), None
        else:
            return
        self.dirty = True

    def click(self, rid: str) -> None:
        title = self.base.rooms[rid]["title"]
        if self.target and rid in (self.target, self.room):
            self.target, self.route = None, []
            return self.say("rota apagada", "dim")
        if rid == self.room:
            return self.say(f"você está em {title}", "dim")
        if not self.room:
            return self.say(NOWHERE, "bad")
        self.target = rid
        self.reroute()
        if not self.route:
            self.target = None
            return self.say(f"sem caminho conhecido até {title}", "bad")
        self.show_route()

    # ------------------------------------------------------------------ rota e sala
    def cmd_rota(self, arg: str) -> None:
        if not arg:
            self.target, self.route = None, []
            return self.say("rota apagada", "dim")
        if self.room is None:
            return self.say(NOWHERE, "bad")
        hit = self.base.nearest(self.room, arg)
        if not hit or (hit[0] != self.room and not hit[1]):
            return self.say(f"nenhuma sala alcançável casa com “{arg}”", "bad")
        self.target = hit[0]
        self.reroute()
        if self.target:
            self.show_route()

    def show_route(self) -> None:
        self.push([("  rota até ", self.th["dim"]), (self.base.rooms[self.target]["title"], self.th["route"]),
                   (f" · {self.base.region(self.target)} · {steps(len(self.route))}", self.th["dim"])])
        self.push([("  ", 0), (mapa.speedwalk([d for d, _ in self.route]), self.th["route"] | curses.A_BOLD),
                   ("   /andar ou duplo clique vai até lá", self.th["dim"])])

    def closed(self, rid: str, d: str) -> bool:
        """Porta fechada nessa saída: na sala atual vale o que o servidor mostrou agora, nas outras, a base."""
        if rid == self.room and self.live:
            return f"!{d}" in next(iter(self.live["exits"]), "").split()
        return f"!{d}" in self.base.rooms[rid].get("exits", [])

    def door_ahead(self, cmd: str) -> None:
        """Você digitou uma direção que o servidor acabou de mostrar fechada (o ! das Saídas): o open vai antes, no
        mesmo Enter. É atalho do que você digitou; resposta do servidor nenhuma dispara comando (POLICY 4)."""
        d = mapa.DIRS.get(cmd.strip().lower())
        if d and self.live and self.closed(self.room, d) and self.last_sent != f"open {d}":
            self.send(f"open {d}")

    def cmd_andar(self) -> None:
        """Speedwalk que você dispara: manda os passos da rota de uma vez. Porta fechada no caminho: abre, passa e
        para do outro lado, porque se ela estiver trancada o passo falha e o resto sairia da sala errada."""
        if not self.sock or not self.ingame:
            return self.say("entre no jogo antes de andar", "bad")
        if not self.route:
            return self.say("sem rota: /rota <sala> ou clique numa sala do mapa", "dim")
        walk, src, door = [], self.room, None
        for d, dest in self.route[:MAX_WALK]:
            if self.closed(src, d):
                walk, door = walk + [f"open {d}", d], f"porta {d} de {self.base.rooms[src]['title']}"
                break
            walk.append(d)
            src = dest
        for cmd in walk:
            self.send(cmd)
        self.moved = None  # vários passos de uma vez: a sala é achada pelo texto, não pela última direção
        left = len(self.route) - len(walk) + bool(door)
        if left:
            self.say(f"abri a {door} e parei do outro lado: /andar continua" if door
                     else f"faltam {steps(left)}: /andar continua", "new")

    def reroute(self) -> None:
        if not self.target or not self.room:
            return
        if self.room == self.target:
            self.say(f"✓ chegou em {self.base.rooms[self.target]['title']}", "ok")
            self.target, self.route = None, []
            return
        self.route = self.base.route(self.room, lambda r: r == self.target) or []

    def cmd_sala(self, arg: str) -> None:
        rid = (self.base.nearest(self.room, arg) or (None,))[0] if arg else (self.center or self.room)
        if not rid:
            return self.say("sala desconhecida na base", "bad")
        r = self.base.rooms[rid]
        self.push([("  " + r["title"], self.th["accent"] | curses.A_BOLD),
                   (f"  {self.base.region(rid)} · {r.get('visits', 0)} visitas", self.th["dim"])])
        for ln in r["description"].splitlines():
            self.push([("  " + ln, self.th["text"])])
        links = self.base.links[rid]
        for d in mapa.sort_dirs(mapa.exits_of(r)):
            dest = self.base.rooms.get(links.get(d, ""), {}).get("title")
            self.push([(f"  {d:<3}", self.th["accent"]), (dest or "não percorrida", self.th["dim" if dest else "new"])])
        for key, label in (("mobs", "seres"), ("objects", "objetos")):
            for x in r.get(key, []):
                self.push([(f"  {label}: ", self.th["dim"]), (x, self.th["text"])])

    # ------------------------------------------------------------------ desenho
    def docks(self, W: int) -> list[tuple[int, int, tuple]]:
        """Colunas da direita: (x do separador, largura, painéis de cima para baixo). Com espaço, o mapa numa coluna e
        o equipamento em cima do who na outra; sem, uma coluna só com abas (F2 ou clique troca)."""
        if not self.panel:
            return []
        if W < PANEL_MIN_COLS:  # estreito: o painel cobre o texto até o Esc
            return [(0, W - 1, (self.dock,))]
        dw = min(DOCK_MAX, (W - TEXT_MIN - 2) // 2)
        if dw >= DOCK_MIN:
            return [(W - 2 * dw - 2, dw, ("mapa",)), (W - dw - 1, dw, ("equip", "who"))]
        pw = min(DOCK_MAX, max(32, W - 82))
        return [(W - pw - 1, pw, (self.dock,))]

    def draw_docks(self, cols: list, bottom: int) -> None:
        for sep, w, names in cols:
            for y in range(bottom):
                self.put(y, sep, "│", self.th["far"])
            x, top, rows = sep + 2, 0, bottom
            if len(cols) == 1:  # coluna única: abas no alto
                cx = x
                for name in DOCKS:
                    on = name == self.dock
                    label = {"mapa": " Mapa ", "equip": " Equipamento ", "who": " Who "}[name]
                    self.spots[(0, cx, cx + len(label))] = ("dock", name)
                    cx = self.put(0, cx, label, (self.th["accent"] | curses.A_BOLD | curses.A_REVERSE) if on
                                  else self.th["dim"], x + w - 2) + 1
                if sep == 0:
                    self.put(0, cx + 1, "Esc volta ao texto", self.th["far"], x + w - 2)
                top, rows = 2, bottom - 2
            if names == ("equip", "who"):
                wh = min(rows // 2, max(5, len(self.who) + 2))
                self.draw_bag(x, top, rows - wh - 1, w - 2)
                self.put(top + rows - wh - 1, sep + 1, "─" * w, self.th["far"])
                self.draw_who(x, top + rows - wh, wh, w - 2)
            else:
                {"mapa": self.draw_panel, "equip": self.draw_bag, "who": self.draw_who}[names[0]](x, top, rows, w - 2)

    def draw_panel(self, x: int, top: int, rows: int, w: int) -> None:
        rid = self.center or self.room
        if not rid:
            self.put(top, x, "Mapa", self.th["accent"] | curses.A_BOLD)
            msg = ["", f"base: {len(self.base.rooms)} salas", ""]
            if self.live:
                msg += ["sala nova, fora da base:", self.live["title"], "saídas: " + " ".join(mapa.sort_dirs(self.live_exits))]
            else:
                msg += ["entre no jogo ou dê um look", "para o mapa achar você"]
            for i, m in enumerate(msg):
                self.put(top + 1 + i, x, m, self.th["new" if self.live and i > 2 else "dim"], x + w)
            return
        r = self.base.rooms[rid]
        self.put(top, x, r["title"], self.th["accent"] | curses.A_BOLD, x + w)
        sub = self.base.region(rid) + ("  · navegando, /mapa volta" if self.center else "")
        self.put(top + 1, x, sub, self.th["dim"], x + w)
        info = self.panel_info(rid, r)[:max(0, rows - 12)]
        mh = rows - 3 - len(info)
        self.peek = self.base.route(self.room, lambda a: a == self.hover) if self.hover and self.room else None
        grid, cells = self.base.minimap(rid, w, mh, frozenset(b for _, b in self.route),
                                        frozenset(b for _, b in self.peek or []), self.room or "")
        for y, row in enumerate(grid):
            for cx, (ch, st) in enumerate(row):
                if ch != " ":
                    a = self.th[MAP_STYLE[st]] | (curses.A_BOLD if st in ("cur", "route") else 0)
                    if self.hover and cells.get((y, cx)) == self.hover:
                        a |= curses.A_REVERSE
                    self.put(top + 2 + y, x + cx, ch, a, x + w)
        self.hits = {(top + 2 + gy, x + gx): a for (gy, gx), a in cells.items()}
        for i, segs in enumerate(info):
            cx = x
            for t, a in segs:
                cx = self.put(top + 3 + mh + i, cx, t, a, x + w)

    def panel_info(self, rid: str, r: dict) -> list[list]:
        here = rid == self.room and not self.center
        links = self.base.links[rid]
        out = []
        for d in mapa.sort_dirs(self.live_exits if here else mapa.exits_of(r)):
            dest = self.base.rooms.get(links.get(d, ""), {}).get("title")
            out.append([(f"{d:<3}", self.th["accent"]), (dest or "não percorrida", self.th["dim" if dest else "new"])])
        seen = (list(self.live["mobs"]) + list(self.live["objects"])) if here and self.live else \
            r.get("mobs", []) + r.get("objects", [])
        for x in seen[:4]:
            out.append([("· ", self.th["dim"]), (x, self.th["text"])])
        return out

    def preview_rows(self, rid: str, iw: int) -> list[tuple[str, str]]:
        """Linhas (texto, estilo) da prévia: título, região, descrição, saídas, o que tem lá e o caminho até lá."""
        b, r = self.base, self.base.rooms[rid]
        rows = [(r["title"], "title"), (f"{b.region(rid)} · {r.get('visits', 0)} visitas", "dim")]
        desc = textwrap.wrap(" ".join(r["description"].split()), iw)
        rows += [(ln, "text") for ln in desc[:5]] + ([("…", "dim")] if len(desc) > 5 else [])
        links = b.links[rid]
        ex = [f"{d} {b.rooms[links[d]]['title']}" if links.get(d) in b.rooms else f"{d} (não percorrida)"
              for d in mapa.sort_dirs(mapa.exits_of(r))]
        rows += [(ln, "dim") for ln in textwrap.wrap("saídas: " + " · ".join(ex), iw)[:3]]
        rows += [("· " + t, "text") for t in (r.get("mobs", []) + r.get("objects", []))[:3]]
        if rid == self.room:
            rows.append(("você está aqui", "accent"))
        elif not self.room:
            rows.append(("posição atual desconhecida", "dim"))
        elif self.peek is None:
            rows.append(("sem caminho conhecido daqui", "bad"))
        else:
            walk = f"{steps(len(self.peek))}: " + mapa.speedwalk([d for d, _ in self.peek])
            rows += [(ln, "peek") for ln in textwrap.wrap(walk, iw)[:2]]
        tip = "clique: apagar a rota · duplo: ir" if rid == self.target else "clique: rota · duplo: ir · direito: centralizar"
        return rows + [(tip, "far")]

    def draw_preview(self, bottom: int, ow: int) -> None:
        """Caixa flutuante à esquerda do painel, na altura da sala sob o mouse."""
        bw = min(60, ow - 4)
        rows = self.preview_rows(self.hover, bw - 4)[:max(1, bottom - 2)]
        bh = len(rows) + 2
        y0, x0 = max(0, min(self.hover_y - 1, bottom - bh)), max(0, ow - bw - 1)
        edge = self.th["accent"]
        self.put(y0, x0, "╭" + "─" * (bw - 2) + "╮", edge)
        for i, (text, st) in enumerate(rows, 1):
            self.put(y0 + i, x0, "│" + " " * (bw - 2) + "│", edge)
            attr = self.th["accent"] | curses.A_BOLD if st == "title" else self.th[st]
            self.put(y0 + i, x0 + 2, text, attr, x0 + bw - 2)
        self.put(y0 + bh - 1, x0, "╰" + "─" * (bw - 2) + "╯", edge)

    def draw_status(self, y: int, W: int) -> None:
        if time.time() - self.ctrlc < 2:
            self.put(y, 2, "Ctrl-C de novo para sair (envia quit)", self.th["accent"])
            return
        x = 2
        if self.stats:
            for v, mx, unit, tone in zip(self.stats, self.maxstats, ("hp", "m", "mv"), ("ok", "peek", "new")):
                tone = "bad" if v * 4 <= mx else "new" if unit == "hp" and v * 2 <= mx else tone
                full, empty = bar(v, mx)
                x = self.put(y, x, unit + " ", self.th["dim"])
                x = self.put(y, x, full, self.th[tone])
                x = self.put(y, x, empty, self.th["far"])
                x = self.put(y, x, f" {v}  ", self.th["text"])
        if self.room:
            x = self.put(y, x, "· " + self.base.rooms[self.room]["title"], self.th["text"])
            x = self.put(y, x, " · " + self.base.region(self.room), self.th["dim"])
        elif self.live:
            x = self.put(y, x, "· sala nova, fora da base: " + self.live["title"], self.th["new"])
        if self.route:
            x = self.put(y, x, f" · rota {steps(len(self.route))}, próximo {self.route[0][0]}", self.th["route"])
        right = ("↑ rolando, PgDn volta  " if self.scroll else "") + ("● conectado" if self.sock else "○ desconectado")
        if W - len(right) - 2 > x:
            self.put(y, W - len(right) - 2, right, self.th["ok" if self.sock and not self.scroll else "dim"])
        idle = self.idle_label()
        if idle and W - len(right) - len(idle[0]) - 5 > x:
            self.put(y, W - len(right) - len(idle[0]) - 5, idle[0], self.th[idle[1]] | curses.A_BOLD)
