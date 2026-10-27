#!/usr/bin/env python3
"""Cliente de terminal para o MUD Valinor no jeito do Claude Code: a saída rola em cima, a caixa de entrada fica
embaixo com a barra de status, e um painel lateral mostra o mapa da base (db/valinor.json) em volta da sala atual.

Uso: python3 cliente/valinor.py [host] [porta]
Grava como o mud.sh: logs/raw.log (bytes do servidor), logs/transcript.log (legível) e logs/chat.log.
VALINOR_LOGS=<pasta> grava em outra pasta (para testes, sem sujar a fonte da wiki).
Só envia o que você digita ou pede: /andar manda a rota traçada de uma vez (speedwalk) e a direção com porta fechada
leva o open junto; nada de gatilhos (POLICY 4). Tab completa, → aceita a sugestão cinza do histórico;
no mapa, o mouse mostra a prévia da sala e o clique traça a rota (painel.py)."""
from __future__ import annotations

import curses
import locale
import os
import re
import socket
import sys
import time
from collections import deque
from itertools import islice

import completar
import logo
import mapa
import paleta as P
import leitor
from conexao import ANSI, ASKS_PW, LOGS, STD_PROMPT, WIN, load_chars, secrets, shape, telnet, vitals, wait
from conversa import Conversa, who_scan
from logo import IDLE_FRAME, Abertura
from mochila import EQ_HEAD, INV_HEAD, Mochila
from painel import DOCKS, MAX_WALK, MOUSE_OFF, PANEL_MIN_COLS, Painel
from vigia import Vigia, keepalive

HOST, PORT = "mud.valinor.com.br", 4000
VERSAO = "0.1.2"
QUIET = 0.4  # segundos de silêncio do servidor que fecham uma resposta quando o prompt não é o padrão
SGR_IN = r"(?:\x1b\[[0-9;]*m)*"  # com as cores ligadas o servidor colore cada número do prompt
PROMPT = re.compile(rf"<{SGR_IN}(-?\d+)hp {SGR_IN}(-?\d+)m {SGR_IN}(-?\d+)mv{SGR_IN}> ?")
MAXES = re.compile(r"(Vida|Mana|Movimento):\s*-?\d+\s*(?:/|de)\s*(\d+)")  # do score, com e sem Modo Aural
HOLD = re.compile(r"<[-\dhpmv \x1b\[;]{0,80}$")  # começo de prompt partido entre dois pacotes
CHAT = re.compile(r"^\(OOC\) .+ (disse|perguntou|exclamou)|para você '")
SCROLLBACK = 5000
COMMANDS = {
    "/ajuda": "comandos e atalhos do cliente",
    "/mapa": "liga ou desliga o mapa; /mapa <sala> centraliza nela",
    "/rota": "/rota <sala ou região>: caminho mais curto pela base",
    "/andar": f"manda a rota de uma vez (speedwalk, até {MAX_WALK} passos; abre a porta do caminho e para depois dela)",
    "/sala": "/sala [nome]: o que a base sabe da sala",
    "/busca": "/busca <texto>: salas, NPCs, criaturas, itens e objetos",
    "/eq": "mostra o painel de equipamento e inventário (com uma coluna só, F2 troca de painel)",
    "/who": "mostra o painel de quem está online",
    "/recarregar": "relê db/valinor.json depois de atualizar a base",
    "/mouse": "liga ou desliga o mouse (desligado, o terminal volta a selecionar texto)",
    "/limpar": "limpa a tela",
    "/personagem": "troca de personagem (depois do quit o seletor volta sozinho)",
    "/sair": "envia quit e fecha o cliente",
}
TAKES_ARG = {"/mapa", "/rota", "/sala", "/busca"}
THEME = {  # cor do FC-pallete.png (paleta.py) em 256 cores, cor em 8 cores
    "accent": (P.SUNSET, curses.COLOR_YELLOW), "dim": (P.STREET, curses.COLOR_WHITE), "ok": (P.LIME, curses.COLOR_GREEN),
    "bad": (P.CRIMSON, curses.COLOR_RED), "new": (P.SUN, curses.COLOR_YELLOW), "route": (P.HOUSE, curses.COLOR_CYAN),
    "far": (P.LILAC, curses.COLOR_WHITE), "text": (P.MIST, curses.COLOR_WHITE), "peek": (P.PINK, curses.COLOR_MAGENTA),
}


def cut(line: list, a: int, b: int) -> list:
    out, pos = [], 0
    for t, at in line:
        lo, hi = max(a, pos), min(b, pos + len(t))
        if lo < hi:
            out.append((t[lo - pos:hi - pos], at))
        pos += len(t)
    return out


def wrap(line: list, w: int) -> list[list]:
    """Quebra uma linha de segmentos (texto, atributo) em pedaços de até w colunas, de preferência no espaço."""
    text = "".join(t for t, _ in line)
    if len(text) <= w or w < 1:
        return [line]
    cuts, start = [], 0
    while len(text) - start > w:
        brk = text.rfind(" ", start, start + w + 1)
        if brk > start:
            cuts.append((start, brk))
            start = brk + 1
        else:
            cuts.append((start, start + w))
            start += w
    cuts.append((start, len(text)))
    return [cut(line, a, b) for a, b in cuts]


class App(Painel, Abertura, Mochila, Vigia, Conversa):
    def __init__(self, scr, host: str, port: int) -> None:
        self.scr, self.host, self.port = scr, host, port
        curses.raw()
        scr.nodelay(True)
        self.base = mapa.Base()
        self.lines: deque = deque(maxlen=SCROLLBACK)  # cada linha: lista de (texto, atributo curses)
        self.partial: list = []
        self.hold, self.tbuf, self.roomtxt = "", b"", ""
        self.fg, self.bold, self.rev, self.attr = -1, False, False, 0
        self.inp, self.cur, self.sel, self.scroll, self.outw, self.inx = "", 0, 0, 0, 80, 4
        self.hist: list[str] = []
        self.hpos = 0
        self.sock: socket.socket | None = None
        self.masked, self.ingame, self.quit_at = False, False, 0.0
        self.rx_at, self.std_prompt = 0.0, False  # último dado do servidor; já veio um prompt <Nhp Nm Nmv>
        self.digest_at = 0.0  # última resposta processada, pelo prompt (track) ou pelo silêncio (settle)
        self.prompt_re: re.Pattern | None = None  # molde do prompt personalizado, aprendido no silêncio
        self.stats: tuple | None = None
        self.maxstats = [1, 1, 1]
        self.room: str | None = None  # id na base
        self.live: dict | None = None  # sala como o servidor mostrou agora (parse_rooms do minerar)
        self.live_exits: set[str] = set()
        self.moved: str | None = None
        self.center: str | None = None  # sala escolhida com /mapa <sala>
        self.target: str | None = None
        self.route: list = []
        self.panel = scr.getmaxyx()[1] >= PANEL_MIN_COLS  # estreito, o painel cobre o texto: só abre quando pedir
        self.ctrlc, self.running, self.dirty = 0.0, True, True
        self.chars = load_chars()
        self.picking, self.pick, self.confirm, self.others = False, 0, False, []
        self.login: dict | None = None  # login automático do personagem escolhido no seletor
        self.char: str | None = None
        self.bag_init()
        self.talk_init()
        self.dock = "mapa"  # painel da coluna única, quando não cabem duas
        self.idle_reset()
        self.last_sent = ""
        self.tab, self.hide = False, None  # Tab força o popup; Esc esconde o popup para aquele texto
        self.hits: dict = {}  # (linha, coluna) da tela -> sala do minimapa, para o mouse
        self.spots: dict = {}  # (linha, x0, x1) -> (tipo, valor): abas, nomes do who, itens, botões
        self.hover, self.hover_y, self.peek, self.mouse_on = None, 0, None, False
        self.spot_hover: tuple | None = None
        self.logo, self.t0 = logo.cells(logo.load()), time.time()  # o logo brilha na abertura e no seletor
        self.logo_h = 1 + max((y for y, *_ in self.logo), default=-1)
        self.logo_w = 1 + max((x for _, x, *_ in self.logo), default=-1)
        self.colors()
        LOGS.mkdir(parents=True, exist_ok=True)
        self.raw = open(LOGS / "raw.log", "ab")
        self.tr = open(LOGS / "transcript.log", "a", encoding="utf-8")
        self.chat = open(LOGS / "chat.log", "a", encoding="utf-8")
        self.comp = completar.Completer(self.base, LOGS / "transcript.log", secrets())

    # ------------------------------------------------------------------ cores
    def colors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        self.ncol = 16 if curses.COLORS >= 16 else 8
        rich = self.rich = curses.COLORS >= 256
        for i in range(self.ncol):  # as cores que o servidor manda, trocadas pelas do quadro
            curses.init_pair(i + 1, logo.xterm(P.ANSI[i]) if rich else i, -1)
        self.glowp: dict[int, int] = {}  # cor xterm -> par, criados sob demanda para o brilho do logo
        self.th = {}
        for k, (name, (rgb, c8)) in enumerate(THEME.items()):
            curses.init_pair(20 + k, logo.xterm(rgb) if rich else c8, -1)
            self.th[name] = curses.color_pair(20 + k) | (0 if rich or name not in ("dim", "far") else curses.A_DIM)
        self.th[""] = 0

    def sgr(self, params: str) -> None:
        for p in (params or "0").split(";"):
            p = int(p or 0)
            if p == 0:
                self.fg, self.bold, self.rev = -1, False, False
            elif p == 1:
                self.bold = True
            elif p == 7:
                self.rev = True
            elif 30 <= p <= 37:
                self.fg = p - 30
            elif p == 39:
                self.fg = -1
        a = curses.A_REVERSE if self.rev else 0
        if self.fg < 0:
            self.attr = a | (curses.A_BOLD if self.bold else 0)
        elif self.bold and self.ncol == 16:
            self.attr = a | curses.color_pair(self.fg + 9)  # negrito vira a cor clara (0;1;30 = cinza)
        else:
            self.attr = a | curses.color_pair(self.fg + 1) | (curses.A_BOLD if self.bold else 0)

    # ------------------------------------------------------------------ rede
    def connect(self) -> None:
        self.say(f"conectando a {self.host}:{self.port}…", "dim")
        self.draw()
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=10)
        except OSError as e:
            self.say(f"✗ não conectou: {e}", "bad")
            self.open_picker()
            return
        self.sock.setblocking(False)
        keepalive(self.sock)
        self.idle_reset()
        self.tbuf, self.roomtxt, self.ingame, self.std_prompt, self.prompt_re = b"", "", False, False, None
        self.stats, self.maxstats, self.room, self.live, self.live_exits = None, [1, 1, 1], None, None, set()
        self.center, self.target, self.route = None, None, []
        self.bag, self.bag_at = {}, 0.0
        self.tr.write(f"=== NOVA CONEXÃO {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        self.tr.flush()

    def close(self, why: str) -> None:
        dropped = self.ingame and self.last_sent != "quit" and not self.quit_at  # caiu sem você ter saído
        if self.sock:
            self.sock.close()
        if self.masked:
            self.inp, self.cur = "", 0
        self.sock, self.masked, self.ingame = None, False, False
        self.say(f"— {why} —", "dim")
        if self.quit_at:
            self.running = False
            return
        if dropped:
            boot = "MUD está sendo reiniciado" in self.roomtxt  # o que veio depois do último prompt
            self.alert("⚠ o MUD está reiniciando: espere uns segundos e Enter no seletor entra de novo" if boot else
                       "⚠ a conexão caiu sem você ter saído: Enter no seletor entra de novo")
        self.open_picker()

    def recv(self) -> None:
        try:
            raw = self.sock.recv(65536)
        except BlockingIOError:
            return
        except OSError:
            raw = b""
        if not raw:
            self.close("conexão encerrada pelo servidor")
            return
        self.raw.write(raw)
        self.raw.flush()
        self.rx_at = time.time()
        data, echo, self.tbuf = telnet(self.tbuf + raw)
        if echo is not None:
            self.masked = echo
        text = data.decode("latin1")
        plain = ANSI.sub("", text)
        self.tr.write(plain.replace("\r", ""))
        self.tr.flush()
        self.feed(text.replace("\r", "").replace("\t", "    "))
        self.track(plain)
        self.idle_seen(plain)
        self.autologin()
        self.dirty = True

    def send(self, cmd: str, hidden: bool = False) -> None:
        if not self.sock:
            self.say("desconectado", "bad")
            return
        try:
            self.sock.sendall(cmd.encode("latin1", "replace") + b"\r\n")
        except OSError as e:
            self.close(f"erro ao enviar: {e}")
            return
        self.idle_reset()
        self.last_sent = cmd.strip().lower()
        hidden = hidden or bool(ASKS_PW.search("".join(t for t, _ in self.partial)))
        if self.partial:
            self.newline()
        if self.masked or hidden:  # senha: não vai para o histórico nem para o transcript
            self.push([("› ", self.th["accent"]), ("•" * 8, self.th["dim"])])
            return
        self.tr.write(f"\n>>> [{time.strftime('%H:%M:%S')}] {cmd}\n")
        self.tr.flush()
        self.push([("› ", self.th["accent"]), (cmd, self.th["dim"])])
        self.moved = mapa.DIRS.get(cmd.strip().lower())
        self.comp.learn(cmd)

    # ------------------------------------------------------------------ texto do servidor
    def track(self, plain: str) -> None:
        """Junta o texto bruto (com \\r) até o próximo prompt e, se veio uma sala, acha ela na base."""
        self.roomtxt = (self.roomtxt + plain)[-30000:]
        last = None
        for last in PROMPT.finditer(self.roomtxt):
            pass
        if not last:
            return
        done, self.roomtxt = self.roomtxt[:last.end()], self.roomtxt[last.start():]
        self.std_prompt = True
        self.digest(done)

    def settle(self) -> None:
        """Prompt fora do padrão (personalizado no jogo): sem ele para marcar o fim da resposta, o silêncio do servidor
        marca. A sala, o equipamento ou o who chegando também dizem que você já está no jogo."""
        done = self.roomtxt
        self.roomtxt = done[done.rfind("\n") + 1:]  # como no track, a linha do prompt fica: o título da sala vem nela
        entered = self.ingame or "Saídas:" in done or EQ_HEAD in done or INV_HEAD in done or who_scan(done) is not None
        tail = self.roomtxt.strip()
        known = entered and not self.masked and any(c.isdigit() for c in tail)  # a linha sem quebra no fim é o prompt
        if known:
            self.prompt_re = shape(tail)
        if self.prompt_re:
            done = self.prompt_re.sub(STD_PROMPT, done)
        self.digest(done)
        v = vitals(tail) if known else None
        if v:
            self.stats = tuple(c for c, _ in v)
            self.maxstats = [mx or max(old, c) for (c, mx), old in zip(v, self.maxstats)]
        if entered and not self.ingame and not self.masked:
            self.ingame = True
            if not v:
                self.say("não achei hp, m e mv no seu prompt: as barras ficam paradas. O cliente procura um número "
                         "seguido de hp, m e mv (84hp ou 84/84hp), em qualquer ordem.", "dim")

    def digest(self, done: str) -> None:
        """Uma resposta inteira do servidor: máximos do score, equipamento, who e a sala, se veio uma."""
        self.digest_at = time.time()
        for m in MAXES.finditer(done):  # o prompt só traz o atual; o máximo vem quando você digita score
            self.maxstats[("Vida", "Mana", "Movimento").index(m[1])] = int(m[2])
        self.bag_scan(done)
        self.who_seen(done)
        if "Saídas:" not in done:
            return
        seen = mapa.last_room(done)
        if not seen:
            return
        exits = {e.lstrip("!") for e in next(iter(seen["exits"]), "").split()}
        self.room = self.base.identify(seen["title"], seen["description"], exits, self.room, self.moved)
        self.live, self.live_exits, self.moved = seen, exits, None
        self.reroute()

    def feed(self, text: str) -> None:
        text, self.hold = self.hold + text, ""
        m = HOLD.search(text)
        if m:
            self.hold, text = text[m.start():], text[:m.start()]
        pos = 0
        for m in PROMPT.finditer(text):
            self.emit(text[pos:m.start()])
            self.stats = tuple(int(x) for x in m.groups())
            self.maxstats = [max(a, b) for a, b in zip(self.maxstats, self.stats)]
            self.ingame = True
            self.sgr("0")  # as cores do prompt somem junto com ele
            if self.partial:
                self.newline()
            if self.lines and self.lines[-1]:
                self.push([])  # uma linha em branco entre as respostas, no lugar do prompt
            pos = m.end()
        self.emit(text[pos:])

    def emit(self, text: str) -> None:
        pos = 0
        for m in ANSI.finditer(text):
            self.chunk(text[pos:m.start()])
            if m.group(2) == "m":
                self.sgr(m.group(1))
            pos = m.end()
        self.chunk(text[pos:])

    def chunk(self, text: str) -> None:
        for k, part in enumerate(text.split("\n")):
            if k:
                self.newline()
            if part:
                self.partial.append((part, self.attr))

    def newline(self) -> None:
        line, self.partial = self.partial, []
        text = "".join(t for t, _ in line)
        if not text.strip():
            if not self.lines or not self.lines[-1]:
                return
            line = []
        elif CHAT.search(text):
            self.chat.write(text + "\n")
            self.chat.flush()
            line = [(t, a | curses.A_BOLD) for t, a in line]
        if line:
            self.talk_seen(text)
        self.push(line)

    def push(self, line: list) -> None:
        self.lines.append(line)
        if self.scroll and self.chan is None:
            self.scroll += len(wrap(line, self.outw))
        self.dirty = True

    def say(self, text: str, style: str = "") -> None:
        self.push([(text, self.th[style])])

    # ------------------------------------------------------------------ comandos do cliente
    def completions(self) -> tuple[int, list[tuple[str, str]]]:
        """(coluna onde a sugestão entra, [(sugestão, descrição)]). Aparece sozinho com /comando ou 2+ letras na
        palavra; com menos, só depois do Tab."""
        text = self.inp[:self.cur]
        word = text[text.rfind(" ") + 1:]
        if self.masked or self.picking or self.chatting() or (self.hide == self.inp and not self.tab) or \
                not (self.tab or (text.startswith("/") and " " not in text) or len(word) >= 2):
            return 0, []
        live = self.live or {}
        here = completar.text_words(list(live.get("mobs", [])) + list(live.get("objects", [])))
        seen = completar.text_words("".join(t for t, _ in ln) for ln in islice(reversed(self.lines), 60))
        return self.comp.complete(text, here, seen, COMMANDS)

    def accept(self, start: int, pop: list) -> None:
        """Troca a palavra até o cursor pela sugestão; espaço depois de palavra do jogo e de /comando com argumento."""
        c, rest = pop[self.sel % len(pop)][0], self.inp[self.cur:]
        game = not self.inp.startswith("/")
        tail = "" if rest.startswith(" ") else " " if (game or c in TAKES_ARG) else ""
        self.inp = self.inp[:start] + c + tail + rest
        self.cur, self.sel, self.tab = start + len(c) + len(tail), 0, False

    def submit(self) -> None:
        start, pop = self.completions()
        if pop and self.inp.startswith("/") and " " not in self.inp and self.inp not in COMMANDS:
            self.accept(start, pop)
            if self.inp.endswith(" "):
                return
        cmd, self.inp, self.cur, self.scroll, self.sel, self.tab = self.inp, "", 0, 0, 0, False
        if cmd.strip() and not self.masked and (not self.hist or self.hist[-1] != cmd):
            self.hist.append(cmd)
        self.hpos = len(self.hist)
        if cmd.startswith("/") and not self.masked:
            self.comp.learn(cmd)
            self.slash(cmd.strip())
        elif self.chan is not None:
            self.talk_send(cmd)
        else:
            if not self.masked:
                self.door_ahead(cmd)
            self.send(cmd)

    def slash(self, line: str) -> None:
        name, _, arg = line.partition(" ")
        arg = arg.strip()
        name = name if name in COMMANDS else next((c for c in COMMANDS if c.startswith(name)), name)
        self.push([("› ", self.th["accent"]), (line, self.th["accent"])])
        if name == "/ajuda":
            self.help()
        elif name == "/mapa":
            if arg:
                hit = self.base.nearest(self.room, arg)
                if not hit:
                    return self.say(f"nenhuma sala da base casa com “{arg}”", "bad")
                self.center, self.panel = hit[0], True
                self.say(f"mapa centrado em {self.base.rooms[hit[0]]['title']}. /mapa volta a seguir você", "dim")
            elif self.center:
                self.center = None
            else:
                self.panel = not self.panel
        elif name == "/rota":
            self.cmd_rota(arg)
        elif name == "/andar":
            self.cmd_andar()
        elif name == "/sala":
            self.cmd_sala(arg)
        elif name == "/busca":
            if not arg:
                return self.say("uso: /busca <texto>", "dim")
            hits = self.base.search(arg)
            for kind, nome, onde in hits:
                self.push([(f"  {kind:<9}", self.th["dim"]), (nome, self.th["text"]),
                           (f"  {onde}" if onde else "", self.th["dim"])])
            if not hits:
                self.say(f"nada na base casa com “{arg}”", "dim")
        elif name in ("/eq", "/who"):
            self.panel, self.dock = True, "equip" if name == "/eq" else "who"
        elif name == "/recarregar":
            self.base.load()
            self.comp.reload()
            self.bag_idx = None
            self.say(f"base relida: {len(self.base.rooms)} salas, {len(self.base.data['object'])} objetos", "dim")
        elif name == "/mouse":
            self.set_mouse(not self.mouse_on)
            self.say("mouse ligado" if self.mouse_on else "mouse desligado: arrastar volta a selecionar texto", "dim")
        elif name == "/limpar":
            self.lines.clear()
        elif name == "/personagem":
            if self.sock:
                self.say("um personagem por vez: digite quit, e o seletor volta quando a conexão fechar", "dim")
            else:
                self.open_picker()
        elif name == "/sair":
            self.quit_at = time.time()
            if self.sock and self.ingame:
                self.send("quit")
            else:
                self.running = False
        else:
            self.say(f"comando desconhecido: {name}. /ajuda lista os comandos", "bad")

    def help(self) -> None:
        self.say("Comandos do cliente (todo o resto vai direto para o jogo):", "accent")
        for c, d in COMMANDS.items():
            self.push([(f"  {c:<12}", self.th["accent"]), (d, self.th["dim"])])
        self.say("Teclas: Enter envia · ↑↓ histórico (ou a lista de sugestões) · PgUp/PgDn rola · Esc fecha a lista,", "dim")
        self.say("       de novo limpa a linha · Ctrl-L redesenha · Ctrl-C limpa a linha, duas vezes seguidas sai (quit)", "dim")
        self.say("Auto-complete: Tab completa (comandos que você já usou, coisas da sala e da tela, salas para /rota)", "dim")
        self.say("       → no fim da linha aceita a sugestão cinza, tirada do seu histórico", "dim")
        self.say("Mapa: @ você · [↑] [↓] [↕] sala com escada · azul = rota · amarelo = saída que a base não percorreu", "dim")
        self.say("Mouse: passe sobre uma sala para ver a prévia e o caminho (rosa) · clique traça a rota · duplo", "dim")
        self.say("       clique vai até lá (/andar) · botão direito centraliza · roda rola o texto", "dim")
        self.say("       Shift+arrastar seleciona texto · /mouse desliga", "dim")
        self.say("Painéis: mapa, equipamento e who ao lado do texto (sem espaço, uma coluna com abas: F2 troca)", "dim")
        self.say("       mouse num item mostra o que a base sabe · ↻ eq (ou F5) manda eq e inv · ↻ who manda who", "dim")
        self.say("Conversa: abas Jogo, Global e uma por pessoa (clique no nome do who) · F3 troca · Esc volta", "dim")
        self.say("       na aba, o Enter manda chat <texto> ou tell <nome> <texto>; /comando continua valendo", "dim")
        self.say("Portas: digitar a direção de uma saída fechada (!n nas Saídas) manda open n antes do passo", "dim")
        self.say("Parado: a barra conta o tempo sem digitar e aos 6 min toca um aviso (Vazio aos 8-10, quit ~4 depois)", "dim")

    # ------------------------------------------------------------------ teclado
    def key(self, ch) -> None:
        self.dirty = True
        if ch == curses.KEY_MOUSE or (ch == "\x1b" and self.mouse_on and not WIN and self.sgr_next()):
            return self.on_mouse()
        if ch == curses.KEY_F2 and not self.picking:
            self.panel, self.dock = True, DOCKS[(DOCKS.index(self.dock) + 1) % len(DOCKS)]
            return
        if ch == curses.KEY_F3 and not self.picking:
            return self.next_chan()
        if ch == curses.KEY_F5 and not self.picking:
            return self.bag_refresh()
        if self.picking:
            return self.key_pick(ch)
        before = self.inp
        self.edit(ch)
        if self.inp != before:
            self.sel, self.tab = 0, False

    def edit(self, ch) -> None:
        start, pop = self.completions()
        if ch in ("\n", "\r", curses.KEY_ENTER):
            self.submit()
        elif ch in ("\x7f", "\b", curses.KEY_BACKSPACE):
            if self.cur:
                self.inp, self.cur = self.inp[:self.cur - 1] + self.inp[self.cur:], self.cur - 1
        elif ch == curses.KEY_DC:
            self.inp = self.inp[:self.cur] + self.inp[self.cur + 1:]
        elif ch == curses.KEY_LEFT:
            self.cur = max(0, self.cur - 1)
        elif ch == curses.KEY_RIGHT:
            ghost = self.comp.ghost(self.inp) if self.cur == len(self.inp) and not (self.masked or self.chatting()) else ""
            self.inp += ghost
            self.cur = len(self.inp) if ghost else min(len(self.inp), self.cur + 1)
        elif ch in (curses.KEY_HOME, "\x01"):
            self.cur = 0
        elif ch in (curses.KEY_END, "\x05"):
            self.cur = len(self.inp)
        elif ch == "\x15":
            self.inp, self.cur = self.inp[self.cur:], 0
        elif ch == "\x17":
            left = self.inp[:self.cur].rstrip()
            left = left[:left.rfind(" ") + 1]
            self.inp, self.cur = left + self.inp[self.cur:], len(left)
        elif ch == curses.KEY_UP:
            if pop:
                self.sel = (self.sel - 1) % len(pop)
            elif self.hpos > 0 and not self.masked:
                self.hpos -= 1
                self.inp = self.hide = self.hist[self.hpos]
                self.cur = len(self.inp)
        elif ch == curses.KEY_DOWN:
            if pop:
                self.sel = (self.sel + 1) % len(pop)
            elif self.hpos < len(self.hist):
                self.hpos += 1
                self.inp = self.hide = self.hist[self.hpos] if self.hpos < len(self.hist) else ""
                self.cur = len(self.inp)
        elif ch == "\t":
            if pop:
                self.accept(start, pop)
            elif not self.masked:
                self.tab = True
                start, pop = self.completions()
                if len(pop) == 1:
                    self.accept(start, pop)
        elif ch == curses.KEY_PPAGE:
            self.scroll += max(1, self.scr.getmaxyx()[0] - 8)
        elif ch == curses.KEY_NPAGE:
            self.scroll = max(0, self.scroll - max(1, self.scr.getmaxyx()[0] - 8))
        elif ch == "\x1b":
            if pop:
                self.hide, self.tab = self.inp, False
            elif not self.inp and self.panel and self.scr.getmaxyx()[1] < PANEL_MIN_COLS:
                self.panel = False  # o painel que cobria o texto
            elif not self.inp and self.chan is not None:
                self.set_chan(None)
            else:
                self.inp, self.cur, self.sel = "", 0, 0
        elif ch == "\x0c":
            self.scr.clear()
        elif ch == "\x03":
            if self.inp:
                self.inp, self.cur = "", 0
            elif time.time() - self.ctrlc < 2:
                self.slash("/sair")
            else:
                self.ctrlc = time.time()
        elif ch == curses.KEY_RESIZE:
            if WIN:
                curses.resize_term(0, 0)  # o PDCurses só pega o tamanho novo da janela assim
            curses.update_lines_cols()
        elif isinstance(ch, str) and ch.isprintable():
            self.inp, self.cur = self.inp[:self.cur] + ch + self.inp[self.cur:], self.cur + 1

    # ------------------------------------------------------------------ tela
    def put(self, y: int, x: int, text: str, attr: int = 0, limit: int | None = None) -> int:
        H, W = self.scr.getmaxyx()
        end = W if limit is None else min(W, limit)
        if not (0 <= y < H) or x >= end:
            return x
        text = text[:max(0, end - x)]
        try:
            self.scr.addstr(y, x, text, attr)
        except curses.error:
            pass  # última célula da tela
        return x + len(text)

    def draw(self) -> None:
        s = self.scr
        H, W = s.getmaxyx()
        s.erase()
        self.hits, self.spots = {}, {}
        if H < 12 or W < 50:
            self.put(0, 0, "terminal pequeno demais para o cliente")
            s.refresh()
            return
        full = self.completions()[1]
        n = max(1, min(len(full), H - 14))  # janela da lista em volta da seleção, sem empurrar a caixa para fora
        top = max(0, self.sel % len(full) - n + 1) if full else 0
        pop = full[top:top + n]
        opts = self.options() if self.picking else []
        foot = len(opts) + 3 + bool(self.others) if self.picking else 3 + len(pop)
        bottom = H - 1 - foot
        glowing = self.picking and self.logo and W >= self.logo_w + 4  # no seletor o logo toma a tela toda
        cols = [] if glowing else self.docks(W)
        ow = cols[0][0] if cols else W
        if ow > 0:  # com o painel cobrindo o texto, fica a última largura
            self.outw = ow - 2
        head = 0 if self.picking else 1  # faixa das abas de conversa
        if head and ow > 0:
            self.draw_tabs(0, ow)
        used = head + (self.draw_output(head, bottom - head, ow) if ow > 0 else 0)  # ow 0: o painel cobre o texto
        if glowing and bottom - used >= self.logo_h + 2:
            self.draw_logo(used + (bottom - used - self.logo_h) // 2, (W - self.logo_w) // 2)
        elif self.chan and used == head and ow > 0:
            who = "todos (chat)" if self.chan == "global" else self.talk[self.chan]["name"] + " (tell)"
            self.put(head + 1, 2, f"nada aqui ainda · o que você digitar vai para {who}", self.th["far"], ow)
        self.draw_docks(cols, bottom)
        if self.picking:
            self.draw_picker(bottom, W, opts)
        else:
            self.draw_box(bottom, W)
        cw = min(40, max((len(c) for c, _ in pop), default=0) + 2)
        for i, (c, desc) in enumerate(pop):
            on = top + i == self.sel % len(full)
            x = self.put(bottom + 3 + i, 2, ("› " if on else "  ") + f"{c:<{cw}}", self.th["accent"] if on else self.th["text"])
            self.put(bottom + 3 + i, x, desc, self.th["dim"])
        if self.hover in self.hits.values() and not self.picking and ow > 0:
            self.draw_preview(bottom, ow)
        elif self.spot_hover and self.spot_hover[0] == "item" and self.spot_hover in self.spots.values():
            self.draw_card(bottom)
        self.draw_status(H - 1, W)
        try:
            curses.curs_set(0 if self.picking else 1)
            off = max(0, self.cur - (W - self.inx - 3))
            s.move(bottom + 1, self.inx + self.cur - off)
        except curses.error:
            pass
        s.refresh()
        self.dirty = False

    def draw_output(self, top: int, rows: int, width: int) -> int:
        lines, partial = self.view()
        items = list(lines) + ([partial] if partial else [])
        need, rev = rows + self.scroll, []
        for line in reversed(items):
            rev.extend(reversed(wrap(line, self.outw)))
            if len(rev) >= need:
                break
        else:
            self.scroll = min(self.scroll, max(0, len(rev) - rows))
        view = rev[self.scroll:self.scroll + rows][::-1]
        for y, row in enumerate(view):
            x = 1
            for t, a in row:
                x = self.put(top + y, x, t, a, width)
        return len(view)

    def draw_box(self, y: int, W: int) -> None:
        b = self.th["far"]
        self.put(y, 0, "╭" + "─" * (W - 2) + "╮", b)
        self.put(y + 1, 0, "│", b)
        self.put(y + 1, W - 1, "│", b)
        self.put(y + 2, 0, "╰" + "─" * (W - 2) + "╯", b)
        label = self.chan_label()
        self.inx = self.put(y + 1, 2, f"{label} ›" if label else ">", self.th["route" if label else "accent"] | curses.A_BOLD) + 1
        field = W - self.inx - 3
        if not self.inp:
            hint = "senha (o texto fica oculto)" if self.masked else \
                "mensagem; /comando continua valendo, Esc volta ao jogo" if label else "comando do jogo, ou /ajuda"
            self.put(y + 1, self.inx, hint, self.th["far"], W - 2)
            return
        shown = "•" * len(self.inp) if self.masked else self.inp
        off = max(0, self.cur - field)
        x = self.put(y + 1, self.inx, shown[off:off + field], self.th["text"], W - 2)
        if self.cur == len(self.inp) and not (self.masked or self.chatting()):
            self.put(y + 1, x, self.comp.ghost(self.inp), self.th["far"], W - 2)

    # ------------------------------------------------------------------ laço
    def run(self) -> None:
        self.welcome()
        if not self.panel:
            self.say(f"terminal com {self.scr.getmaxyx()[1]} colunas: mapa, equipamento e who abrem por cima do texto "
                     f"(/mapa, /eq, /who ou F2; Esc volta). Com {PANEL_MIN_COLS}+ colunas ficam ao lado.", "dim")
        self.splash()
        self.set_mouse(True)
        self.open_picker()
        while self.running:
            frame = self.anim()
            if self.dirty or frame:
                self.draw()
            if self.sock in wait([self.sock] if self.sock else [], frame or 0.2):
                self.recv()
            if self.rx_at > self.digest_at and time.time() - self.rx_at > QUIET * (4 if self.std_prompt else 1):
                self.settle()  # veio texto sem o prompt padrão no fim (com o padrão, o track já cuidou)
            while True:
                try:
                    ch = self.scr.get_wch()
                except curses.error:
                    break
                self.key(ch)
            self.idle_tick()
            if self.quit_at and time.time() - self.quit_at > 4:
                self.running = False
            if self.ctrlc and time.time() - self.ctrlc > 2:
                self.ctrlc, self.dirty = 0.0, True
        if self.sock:
            self.sock.close()
        for f in (self.raw, self.tr, self.chat):
            f.close()

    def anim(self) -> float | None:
        """Intervalo do próximo quadro quando algo está animando: o equipamento que acabou de chegar, o logo no seletor."""
        if not self.rich:
            return None
        return IDLE_FRAME if self.bag_glowing() or (self.picking and self.logo) else None


def utf8_locale() -> None:
    """O curses precisa de locale UTF-8 para acentos e bordas. LANG ou LC_* apontando para um locale que não existe
    na máquina (comum no SSH vindo do macOS, que manda LC_CTYPE=UTF-8) derrubava o cliente antes de abrir."""
    for name in ("", "C.UTF-8", "C.utf8", "en_US.UTF-8", "UTF-8"):
        try:
            locale.setlocale(locale.LC_ALL, name)
        except locale.Error:
            continue
        if WIN or "utf" in locale.nl_langinfo(locale.CODESET).lower():
            return


def versao() -> int:
    """`valinor --versao`: confere sem abrir a tela que a base, o logo e o terminfo estão no lugar (teste dos binários)."""
    b, art = mapa.Base(), logo.load()
    if not WIN:
        curses.setupterm(os.environ.get("TERM") or "xterm-256color", sys.stdout.fileno())
    print(f"Valinor {VERSAO} · base: {len(b.rooms)} salas, {len(b.data['object'])} objetos · logo: "
          f"{'ok' if art else 'faltando'}")
    return 0 if b.rooms and art else 1


def main() -> None:
    if mapa.FROZEN and not WIN:  # o ncurses do binário procura o terminfo onde foi compilado; esses são os do sistema
        os.environ.setdefault("TERMINFO_DIRS", "/etc/terminfo:/lib/terminfo:/usr/share/terminfo:")
    if sys.argv[1:] == ["--versao"]:
        sys.exit(versao())
    args = [a for a in sys.argv[1:] if a not in ("--leitor", "--visual")]
    host, port = args[0] if args else HOST, int(args[1]) if len(args) > 1 else PORT
    if "--leitor" in sys.argv or ("--visual" not in sys.argv and leitor.screen_reader()):
        return leitor.Leitor(host, port).run()
    utf8_locale()
    os.environ.setdefault("ESCDELAY", "25")
    try:
        curses.wrapper(lambda scr: App(scr, host, port).run())
    finally:
        if not WIN:
            os.write(1, MOUSE_OFF)  # devolve o terminal sem o modo de mouse, mesmo se o cliente cair


if __name__ == "__main__":
    main()
