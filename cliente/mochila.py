"""Painel de equipamento e inventário, fixo ao lado do mapa.

Mostra o que o servidor já mandou (o último eq, o último inv e, do score, itens, peso e ouro) cruzado com a base;
passar o mouse num item abre o cartão com descrição, peso, estado, onde vestir e lojas. O ↻ (ou F5) manda eq e inv
porque você clicou, como um alias; nada sai sozinho (POLICY 4)."""
from __future__ import annotations

import curses
import math
import re
import textwrap
import time
from functools import lru_cache

import logo
import mapa
import paleta as P
from painel import bar

EQ_HEAD, INV_HEAD = "Você está usando:", "Você está carregando:"
SLOT = re.compile(r"<([^>]+)>\s+(.+)")
TAG = re.compile(r"\((\d+)x\)\s*|\(([^)]+)\)\s*")  # (8x) quantidade, (Brilhando) (Queimado) estado
PROMPT_LINE = re.compile(r"<-?\d+hp ")
CARRY = {"items": re.compile(r"Carregando (\d+) itens? de um máximo de (\d+)|Itens:\s+(\d+)/(\d+)"),
         "kg": re.compile(r"Carregando ([\d.]+) kg de um máximo de ([\d.]+) kg|Carreg\.:\s+([\d.]+)/([\d.]+) kg")}
GOLD = re.compile(r"Ouro:\s+([\d.]+)")
# as posições que a dica de vestir do próprio servidor lista, de cima para baixo, e as das mãos que já vieram no eq
BODY = ("cabeça", "olhos", "rosto", "orelhas", "pescoço", "ombros", "sobre o corpo", "corpo", "costas", "braços",
        "pulsos", "mãos", "dedos", "cintura", "pernas", "tornozelos", "pés", "empunhando", "como escudo", "segurando",
        "como luz")
SHORT = {"sobre o corpo": "sobre corpo", "como escudo": "escudo", "empunhando": "arma", "como luz": "luz"}
WHOLE = {"sobre o corpo", "empunhando", "como escudo", "segurando", "como luz"}  # rótulos que valem inteiros
HAND = {"empunhando": ("†", "red"), "como escudo": ("◈", "steel"), "como luz": ("☼", "gold"), "segurando": ("≡", "sky")}
KIND = {"equipamento": ("◆", "steel"), "comida e bebida": ("●", "green"), "pergaminho": ("≡", "sky"),
        "livro": ("≡", "sky"), "mapa": ("▦", "sky")}
CAT = {"food": "comida e bebida", "map": "mapa", "book": "livro", "scroll": "pergaminho", "light": "equipamento",
       "clothing": "equipamento", "armor": "equipamento"}  # a coleção de itens da base usa nomes em inglês
RGB = {"text": P.MIST, "dim": P.STREET, "far": P.LILAC, "accent": P.SUNSET, "gold": P.SUN, "green": P.LIME,
       "red": P.CRIMSON, "steel": P.TEAL, "sky": P.HOUSE}  # do FC-pallete.png
TONE = {"text": "text", "dim": "dim", "far": "far", "accent": "accent", "gold": "new", "green": "ok", "red": "bad",
        "steel": "peek", "sky": "peek"}  # a mesma cor no tema de 8/16 cores
GLOW = 4.0  # segundos que o título e as barras brilham depois que chega um eq ou inv
DETAIL = 6  # linhas do cartão do item
TITLE = "✦ EQUIPAMENTO"


def item(text: str) -> tuple[int, tuple[str, ...], str]:
    """'(8x) (Brilhando) uma maçã' -> (8, ('Brilhando',), 'uma maçã')."""
    qty, tags, rest = 1, [], text.strip()
    m = TAG.match(rest)
    while m:
        if m[1]:
            qty = int(m[1])
        else:
            tags.append(m[2])
        rest = rest[m.end():]
        m = TAG.match(rest)
    return qty, tuple(tags), rest


def block(text: str, head: str) -> list[str] | None:
    """Linhas do último bloco `head` (até a linha vazia ou o prompt); None se ele não veio."""
    at = text.rfind(head)
    if at < 0:
        return None
    out = []
    for ln in text[at + len(head):].split("\n")[1:]:
        if not ln.strip() or PROMPT_LINE.match(ln):
            break
        out.append(ln)
    return out


def scan(text: str) -> dict:
    """O que veio de eq, inv e score num pedaço de texto já sem cores."""
    text, got = text.replace("\r", ""), {}
    eq = block(text, EQ_HEAD)
    if eq is not None:
        got["equip"] = [(m[1], *item(m[2])) for m in map(SLOT.match, eq) if m]
    inv = block(text, INV_HEAD)
    if inv is not None:
        got["inv"] = [item(ln) for ln in inv if ln.strip() != "Nada."]
    for key, rx in CARRY.items():
        for m in rx.finditer(text):
            got[key] = tuple(float(g) for g in m.groups() if g is not None)
    for m in GOLD.finditer(text):
        got["gold"] = int(m[1].replace(".",""))
    return got


def _key(s: str) -> str:
    f = mapa.fold(s)
    return f if f in {mapa.fold(w) for w in WHOLE} else f.split()[-1].rstrip("s")


@lru_cache(maxsize=None)
def spot(label: str) -> str:
    """Posição do corpo para um rótulo do eq: 'nos pés' -> 'pés', 'no pulso' -> 'pulsos'."""
    k = _key(label)
    return next((p for p in BODY if _key(p) == k), label)


def index(base: mapa.Base) -> dict[str, dict]:
    """Nome sem acento -> o que a base sabe do item: o objeto examinado e, por cima, a ficha da coleção de itens."""
    out: dict[str, dict] = {}
    for e in [o for o in base.data.get("object", []) if o.get("kind") == "item"] + base.data.get("item", []):
        cur = out.setdefault(mapa.fold(e["name"]), {})
        for k, v in e.items():
            cur.setdefault("note" if k == "description" and "description" in cur else k, v)
        cur["category"] = CAT.get(cur["category"], cur["category"])
    return out


def price(e: dict | None) -> int | None:
    return min((s["price"] for s in (e or {}).get("shops", []) if s.get("price") is not None), default=None)


def num(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else str(v)


def ago(at: float) -> str:
    s = time.time() - at
    return "agora" if s < 5 else f"há {int(s)} s" if s < 60 else f"há {int(s // 60)} min" if s < 3600 else \
        f"há {int(s // 3600)} h"




class Mochila:
    """Parte do App do painel de equipamento e inventário; usa base, th, put, say, send, sock, ingame, rich, glow,
    spots, spot_hover e hover_y dele."""

    def bag_init(self) -> None:
        self.bag: dict = {}  # equip, inv, items, kg, gold: o que já veio do servidor
        self.bag_at = 0.0
        self.bag_x = 0  # coluna do painel: o cartão do item abre à esquerda dela
        self.bag_idx: dict | None = None

    def bag_scan(self, text: str) -> None:
        got = scan(text)
        if got:
            self.bag.update(got)
            if "equip" in got or "inv" in got:
                self.bag_at = time.time()
            self.dirty = True

    def bag_rows(self) -> tuple[list, list]:
        """Equipado em ordem do corpo e o que está na mochila: (posição ou None, quantidade, marcas, nome)."""
        order = {p: i for i, p in enumerate(BODY)}
        left = sorted(((spot(lb), q, t, n) for lb, q, t, n in self.bag.get("equip", [])),
                      key=lambda r: order.get(r[0], len(BODY)))
        return left, [(None, q, t, n) for q, t, n in self.bag.get("inv", [])]

    def bag_refresh(self) -> None:
        if not (self.sock and self.ingame):
            return self.say("entre no jogo para atualizar o equipamento", "bad")
        for cmd in ("eq", "inv"):  # você clicou no ↻ ou apertou F5: um alias, não um gatilho
            self.send(cmd)

    def bag_glowing(self) -> bool:
        return self.rich and time.time() - self.bag_at < GLOW

    # ------------------------------------------------------------------ desenho
    def ink(self, name: str, rgb: tuple | None = None) -> int:
        if self.rich:
            return self.glow(tuple(round(v) for v in (rgb or RGB[name])))
        return self.th[TONE[name]]

    def shine(self, y: int, x: int, text: str, name: str, t: float, end: int, attr: int = 0) -> int:
        """Texto com um reflexo branco correndo pelas letras."""
        if not self.rich:
            return self.put(y, x, text, self.ink(name) | attr, end)
        pos = (t * 16) % (len(text) + 26) - 13
        for i, c in enumerate(text):
            w = 0.85 * math.exp(-((i - pos) / 2.2) ** 2) if abs(i - pos) < 8 else 0
            x = self.put(y, x, c, self.ink(name, logo.mix(RGB[name], logo.WHITE, w) if w else None) | attr, end)
        return x

    def draw_bag(self, x: int, top: int, rows: int, w: int) -> None:
        if self.bag_idx is None:
            self.bag_idx = index(self.base)
        t, end, self.bag_x = time.time(), x + w, x
        if self.bag_glowing():  # acabou de chegar eq ou inv: o título brilha uns segundos
            cx = x
            for i, c in enumerate(TITLE):
                rgb = logo.ramp(logo.DUSK, (math.sin(i * 0.5 - t * 3) + 1) / 2)
                cx = self.put(top, cx, c, self.ink("text", rgb) | curses.A_BOLD, end)
        else:
            cx = self.put(top, x, TITLE, self.ink("accent") | curses.A_BOLD, end)
        if self.bag_at:
            self.put(top, cx + 2, ago(self.bag_at), self.ink("far"), end - 6)
        self.spots[(top, end - 4, end)] = ("bag-refresh", None)
        self.put(top, end - 4, "↻ eq", self.th["route"] | curses.A_BOLD, end)
        left_rows, right_rows = self.bag_rows()
        y = self.draw_stats(top + 1, x, end, left_rows, right_rows, t)
        body = top + rows - y - 2  # menos os dois cabeçalhos
        if body < 2:
            return
        n_eq, n_inv = max(1, len(left_rows)), max(1, len(right_rows))
        a = n_eq if n_eq + n_inv <= body else min(n_eq, max(body // 2, body - n_inv))
        y = self.section(y, x, end, f"EQUIPADO {len(left_rows)}")
        y = self.draw_list(0, left_rows, y, x, end, a, t)
        y = self.section(y, x, end, f"CARREGANDO {sum(r[1] for r in right_rows)}")
        self.draw_list(1, right_rows, y, x, end, body - a, t)

    def section(self, y: int, x: int, end: int, label: str) -> int:
        cx = self.put(y, x, label + " ", self.ink("accent") | curses.A_BOLD, end)
        self.put(y, cx, "─" * (end - cx), self.ink("far"), end)
        return y + 1

    def meter(self, y: int, x: int, end: int, label: str, v: float, mx: float, unit: str, good: bool,
              t: float) -> int:
        """Barra com degradê: cheia é bom (posições ocupadas) ou cheia é ruim (peso, itens na mão)."""
        x = self.put(y, x, label + " ", self.ink("dim"), end)
        full, empty = bar(v, mx, 10)
        ratio = v / max(mx, 1)
        for i, c in enumerate(full):
            if good:
                rgb = logo.ramp(logo.DUSK[::-1], i / 9)
                if self.bag_glowing():
                    rgb = logo.mix(rgb, logo.WHITE, 0.6 * math.exp(-((i - (t * 6) % 16 + 3) / 1.5) ** 2))
            else:
                rgb = logo.mix(RGB["green"], RGB["gold"], min(1, ratio * 1.6)) if ratio < 0.75 else RGB["red"]
            x = self.put(y, x, c, self.ink("gold" if good else "green" if ratio < 0.75 else "red", rgb), end)
        x = self.put(y, x, empty, self.ink("far"), end)
        return self.put(y, x, f" {num(v)}/{num(mx)}{unit}", self.ink("text"), end)

    def draw_stats(self, y: int, x0: int, end: int, left_rows: list, right_rows: list, t: float,
                   lines: int = 2) -> int:
        """Medidores e números em até `lines` linhas; cada pedaço só entra inteiro. Devolve a linha seguinte."""
        worn = len({r[0] for r in left_rows if r[0] in BODY})
        meters = [("posições", worn, len(BODY), "", True)]
        meters += [("itens", *self.bag["items"], "", False)] if "items" in self.bag else []
        meters += [("peso", *self.bag["kg"], " kg", False)] if "kg" in self.bag else []
        parts = [(len(m[0]) + 12 + len(f"{num(m[1])}/{num(m[2])}{m[3]}"), m) for m in meters]
        worth = sum(r[1] * (price(self.bag_idx.get(mapa.fold(r[3]))) or 0) for r in left_rows + right_rows)
        rest = [[("ouro ", "dim"), (str(self.bag["gold"]), "gold")]] if "gold" in self.bag else []
        rest += [[("score mostra itens, peso e ouro", "far")]] if not {"items", "kg", "gold"} & set(self.bag) else []
        rest += [[("vale ≈ ", "dim"), (f"{worth} moedas", "gold")]] if worth else []
        parts += [(sum(len(text) for text, _ in seg), seg) for seg in rest]
        x, last = x0, y + lines - 1
        for width, part in parts:
            if x > x0 and x + width > end and y < last:
                y, x = y + 1, x0
            if x + width > end:
                continue
            if isinstance(part, tuple):
                x = self.meter(y, x, end, *part, t) + 3
            else:
                for text, ink in part:
                    x = self.put(y, x, text, self.ink(ink) | (curses.A_BOLD if ink == "gold" else 0), end)
                x += 3
        return y + 1

    def look(self, where: str | None, e: dict | None) -> tuple[str, str]:
        if where in HAND:
            return HAND[where]
        if e is None:
            return "?", "gold"
        return KIND.get(e.get("category"), ("•", "dim"))

    def draw_list(self, col: int, rows: list, y: int, x0: int, end: int, n: int, t: float) -> int:
        if n <= 0:
            return y
        if not rows:
            empty = ("nada vestido" if self.bag.get("equip") == [] else "digite eq ou clique ↻",
                     "mochila vazia" if self.bag.get("inv") == [] else "digite inv ou clique ↻")[col]
            self.put(y, x0 + 2, empty, self.ink("far"), end)
            return y + n
        shown = rows if len(rows) <= n else rows[:n - 1]
        lw = min(11, (end - x0) // 4) if col == 0 else 0
        for k, row in enumerate(shown):
            self.spots[(y + k, x0, end)] = ("item", row)
            self.draw_row(y + k, x0, end, self.spot_hover == ("item", row), row, lw, t)
        if len(shown) < len(rows):
            self.put(y + n - 1, x0 + 2, f"… +{len(rows) - len(shown)}", self.ink("far"), end)
        return y + n

    def draw_row(self, y: int, x0: int, end: int, on: bool, row: tuple, lw: int, t: float) -> None:
        where, qty, tags, name = row
        e = self.bag_idx.get(mapa.fold(name))
        glyph, tone = self.look(where, e)
        if on:
            self.put(y, x0, "❯", self.ink("accent") | curses.A_BOLD)
        x = x0 + 2
        if lw:
            pos = where if len(where) <= lw else SHORT.get(where, where)[:lw]
            x = self.put(y, x, f"{pos:>{lw}} ", self.ink("text" if on else "dim"), end)
        x = self.put(y, x, glyph + " ", self.ink(tone) | curses.A_BOLD, end)
        badge = f" ×{qty}" if qty > 1 else ""
        room = end - x - len(badge) - 1
        label = name if len(name) <= room else name[:max(0, room - 1)] + "…"
        bold = curses.A_BOLD if on else 0
        if "Brilhando" in tags:
            x = self.shine(y, x, label, "gold", t + y * 0.3, end, bold)
        else:
            x = self.put(y, x, label, self.ink("text" if e else "dim") | bold, end)
        for tag in tags:
            if tag != "Brilhando" and x + len(tag) + 3 < end - len(badge):
                x = self.put(y, x + 1, f"{tag.lower()}", self.ink("red" if tag == "Queimado" else "dim"), end)
        if badge:
            self.put(y, end - len(badge), badge, self.ink("accent") | curses.A_BOLD, end + 1)

    def chip(self, y: int, x: int, end: int, text: str, name: str) -> int:
        if x + len(text) + 3 > end:
            return x
        x = self.put(y, x, f" {text} ", self.ink(name) | curses.A_REVERSE, end)
        return x + 1

    def draw_card(self, bottom: int) -> None:
        """Cartão do item sob o mouse, flutuando à esquerda do painel, na altura dele."""
        bw = min(66, self.bag_x - 3)
        if bw < 30:
            return
        bh = DETAIL + 2
        y0, x0 = max(0, min(self.hover_y - 1, bottom - bh)), self.bag_x - bw - 2
        edge = self.th["accent"]
        self.put(y0, x0, "╭" + "─" * (bw - 2) + "╮", edge)
        for i in range(1, bh - 1):
            self.put(y0 + i, x0, "│" + " " * (bw - 2) + "│", edge)
        self.put(y0 + bh - 1, x0, "╰" + "─" * (bw - 2) + "╯", edge)
        self.draw_detail(y0 + 1, x0 + 2, x0 + bw - 2, self.spot_hover[1], time.time())

    def draw_detail(self, y: int, x0: int, end: int, pick: tuple, t: float) -> None:
        where, qty, tags, name = pick
        e = self.bag_idx.get(mapa.fold(name))
        glyph, tone = self.look(where, e)
        x = self.put(y, x0, glyph + " ", self.ink(tone) | curses.A_BOLD, end)
        x = self.shine(y, x, name, "gold" if "Brilhando" in tags else "text", t, end, curses.A_BOLD)
        if qty > 1:
            x = self.put(y, x, f"  ×{qty}", self.ink("accent") | curses.A_BOLD, end)
        x += 2
        chips = [((e or {}).get("category"), tone), (where, "accent")] + [(tg.lower(), "gold") for tg in tags]
        for text, ink in chips:
            if text:
                x = self.chip(y, x, end, text, ink)
        facts = []
        if e:
            facts += [f"peso {e['weight']}"] if e.get("weight") else []
            facts += [e["condition"]] if e.get("condition") else []
            facts += [f"veste: {', '.join(e.get('wear') or e.get('worn_at'))}"] if e.get("wear") or e.get("worn_at") else []
            facts += [f"luz {e['light']}"] if e.get("light") else []
            facts += [f"cabe {e['capacity']}"] if e.get("capacity") else []
        self.put(y + 1, x0 + 2, " · ".join(facts) or "—", self.ink("dim"), end)
        self.put(y + 2, x0 + 2, self.shop_line(e), self.ink("gold" if price(e) is not None else "far"), end)
        text = " ".join(((e or {}).get("description") or "").split())
        lines = textwrap.wrap(text, end - x0 - 2)[:DETAIL - 3]
        for k, line in enumerate(lines):
            self.put(y + 3 + k, x0 + 2, line, self.ink("text"), end)
        if len(lines) < DETAIL - 3:
            nudge = "✧ fora da base: examine o item para documentar" if e is None else \
                "✧ ainda não examinado: examine o item para documentar a descrição" if not lines else ""
            if nudge:
                self.put(y + 3 + len(lines), x0 + 2, nudge, self.ink("gold"), end)

    def shop_line(self, e: dict | None) -> str:
        shops = sorted((e or {}).get("shops", []), key=lambda s: s.get("price") or 0)
        if not shops:
            return "nenhuma loja conhecida vende"
        s = shops[0]
        where = self.base.rooms.get(s.get("room"), {}).get("title", "?")
        more = f" · +{len(shops) - 1} loja" + ("s" if len(shops) > 2 else "") if len(shops) > 1 else ""
        return f"loja: {s.get('price')} moedas em {where} ({self.base.region(s['room'])}){more}"
