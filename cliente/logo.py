"""Logo do MUD Valinor em braille para a tela de abertura do cliente.

O cliente só lê o logo.txt. `python3 logo.py` regera o logo.txt a partir do Logo.png (precisa do Pillow)."""
from __future__ import annotations

import curses
import math
import select
import sys
import time
from functools import lru_cache
from pathlib import Path

import mapa
import paleta as P
from conexao import LOGS

HERE = Path(__file__).parent
TXT = HERE / "logo.txt"
STAR = "✦"  # as sete estrelas da Valacirca, dentro do anel
TAGLINE = "Onde a Luz do Antigo Oeste Ainda Vive"
COLS = 96
BOX = (30, 14, 677, 152)  # recorte do Logo.png sem a margem e sem o cursor de texto que ficou depois do "Valinor"
RING_X, TAG_Y, TAG_MID = 180, 118, 133  # fim do anel; a frase fica abaixo de TAG_Y, à direita do anel
INTRO = 2.4  # segundos da abertura animada
FRAME, IDLE_FRAME = 1 / 30, 1 / 12  # quadro da animação na abertura e, mais leve, parada no seletor
SILVER, GOLD, WHITE = P.HOUSE, P.SUNSET, P.GLARE  # Telperion, Laurelin e as duas luzes juntas, nas cores do quadro
STONE, SKY, DARK, NIGHT = P.CURB, P.PINK, P.POLE, P.LILAC
DUSK = (P.SUN, P.SUNSET, P.CRIMSON, P.PINK, P.HOUSE)  # o céu do quadro de baixo para cima, até a casa: misturar
# o laranja direto com o azul passa por um verde-oliva sujo
TWINKLE = "⋆✧✦"  # estrela apagando -> acesa
CUBE = (0, 95, 135, 175, 215, 255)  # níveis do cubo 6x6x6 do xterm-256
DOTS = ((0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (1, 0, 0x08), (1, 1, 0x10), (1, 2, 0x20), (0, 3, 0x40), (1, 3, 0x80))


def load() -> list[str]:
    try:
        return TXT.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def cells(art: list[str]) -> list[tuple[int, int, str, str]]:
    """Células visíveis (linha, coluna, caractere, tom): 'ring' o anel de pedra, 'star' as estrelas, 'title' o nome,
    'tag' a frase. O nome começa na mesma coluna da frase, como no Logo.png."""
    split = next((ln.find(TAGLINE) for ln in art if TAGLINE in ln), 0)
    return [(y, x, c, "star" if c == STAR else "tag" if not "⠀" <= c <= "⣿" else "ring" if x < split
             else "title") for y, ln in enumerate(art) for x, c in enumerate(ln) if c != " "]


def mix(a: tuple, b: tuple, w: float) -> tuple:
    return tuple(p + (q - p) * w for p, q in zip(a, b))


def ramp(stops: tuple, w: float) -> tuple:
    """Cor no ponto w (0 a 1) do degradê que passa por todas as stops."""
    k = max(0.0, min(1.0, w)) * (len(stops) - 1)
    i = min(len(stops) - 2, int(k))
    return mix(stops[i], stops[i + 1], k - i)


def near(angle: float, width: float = 0.6) -> float:
    """1 no ângulo 0, caindo em sino até ~0 a alguns `width` de distância (dá a volta no círculo)."""
    return math.exp(-(((angle + math.pi) % (2 * math.pi) - math.pi) / width) ** 2)


def frame(cs: list[tuple[int, int, str, str]], t: float) -> list[tuple[int, int, str, tuple, str]]:
    """Quadro da animação t segundos depois da abertura: (linha, coluna, caractere, cor rgb, tom).
    O céu do quadro corre em onda pelo nome, a luz de Telperion (o azul da casa) e a de Laurelin (o laranja do céu) giram
    pelo anel em lados opostos, um brilho branco varre o nome, as sete estrelas cintilam e a frase acende letra por letra."""
    ring = [(y, x) for y, x, _, tone in cs if tone == "ring"] or [(0, 0)]
    cy, cx = sum(y for y, _ in ring) / len(ring), sum(x for _, x in ring) / len(ring)
    width = max((x for _, x, _, _ in cs), default=0) + 1
    tag0 = min((x for _, x, _, tone in cs if tone == "tag"), default=0)
    up = min(1.0, t / 0.6)
    fade = up * up * (3 - 2 * up)  # sobe suave do escuro
    sweep = (t % 2.6) / 2.6 * (width + 40) - 20
    out, star = [], 0
    for y, x, c, tone in cs:
        if tone == "title":
            col = ramp(DUSK, (math.sin(x * 0.11 - t * 2.0 + y * 0.45) + 1) / 2)
            col = mix(col, WHITE, 0.85 * math.exp(-((x - y * 1.2 - sweep) / 3) ** 2))
        elif tone == "ring":
            a = math.atan2((y - cy) * 2, x - cx) - t * 2.4  # célula 1:2, então o y conta em dobro
            col = mix(mix(STONE, GOLD, 0.8 * near(a)), SILVER, 0.8 * near(a + math.pi))
        elif tone == "star":
            b = 0.5 + 0.5 * math.sin(t * 4.2 + star * 2.39)  # ângulo de ouro: cada estrela no seu tempo
            col, c, star = mix(NIGHT, WHITE, b), TWINKLE[min(2, int(b * 3))], star + 1
        else:
            k = x - tag0
            on = min(1.0, max(0.0, (t - 0.7 - k * 0.035) / 0.3))
            col = mix(mix(DARK, SKY, on), WHITE, 0.6 * on * math.exp(-((k - (t * 14) % 90) / 2.5) ** 2))
        out.append((y, x, c, tuple(round(v) for v in mix(DARK, col, fade)), tone))  # inteiro: o xterm() cacheia
    return out


@lru_cache(maxsize=4096)
def xterm(rgb: tuple) -> int:
    """Cor mais próxima da paleta xterm-256 (cubo 6x6x6 ou rampa de cinza)."""
    r, g, b = (max(0, min(255, round(v))) for v in rgb)
    q = [0 if v < 48 else 1 if v < 115 else (v - 35) // 40 for v in (r, g, b)]  # nível do CUBE mais próximo
    k = max(0, min(23, round(((r + g + b) / 3 - 8) / 10)))

    def dist(c: tuple) -> int:
        return sum((u - v) ** 2 for u, v in zip(c, (r, g, b)))
    return 232 + k if dist((8 + 10 * k,) * 3) < dist(tuple(CUBE[i] for i in q)) else 16 + 36 * q[0] + 6 * q[1] + q[2]


def render() -> list[str]:
    from PIL import Image

    im = Image.open(HERE / "Logo.png").convert("RGB").crop(BOX)
    W, H = im.size
    dw = COLS * 2
    dh = round(H * dw / W / 4) * 4  # célula 1:2 com 2x4 pontos: ponto quadrado
    sx, sy = W / dw, H / dh
    g = im.resize((dw, dh), Image.BOX).load()
    src = im.load()

    def lum(p: tuple) -> float:
        return 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]

    def dot(x: int, y: int) -> bool:
        r, gr, b = p = g[x, y]
        if (x * sx + BOX[0]) >= RING_X:
            return (y * sy + BOX[1]) < TAG_Y and lum(p) > 95  # nome
        return 65 < lum(p) < 200 and b - (r + gr) / 2 < 18  # pedra cinza; o brilho azul do céu fica de fora

    rows = [[" "] * COLS for _ in range(dh // 4)]
    for cy, row in enumerate(rows):
        for cx in range(COLS):
            v = sum(bit for dx, dy, bit in DOTS if dot(cx * 2 + dx, cy * 4 + dy))
            row[cx] = chr(0x2800 + v) if v else " "
    stars: list[list[tuple[int, int]]] = []
    for y in range(H):
        for x in range(int(RING_X - BOX[0])):
            p = src[x, y]
            if lum(p) > 225 and abs(p[2] - p[0]) < 60:
                near = next((s for s in stars if any(abs(x - a) <= 3 and abs(y - b) <= 3 for a, b in s)), None)
                (near if near is not None else stars.append([]) or stars[-1]).append((x, y))
    for s in stars:
        x, y = sum(a for a, _ in s) / len(s), sum(b for _, b in s) / len(s)
        rows[int(y / sy / 4)][int(x / sx / 2)] = STAR
    ty = int((TAG_MID - BOX[1]) / sy / 4)
    tx = int((RING_X + 13 - BOX[0]) / sx / 2)
    rows[ty][tx:tx + len(TAGLINE)] = list(TAGLINE)
    return ["".join(r).rstrip() for r in rows]


class Abertura:
    """Parte do App da abertura (logo e caixa de boas-vindas): usa scr, th, put, push, base, host, port, rich, logo,
    logo_h, logo_w, t0 e glowp dele."""

    def glow(self, rgb: tuple) -> int:
        n = xterm(rgb)
        if n not in self.glowp:
            pair = 40 + len(self.glowp)  # pares 1-16 e 20+ são do tema
            if pair >= min(256, curses.COLOR_PAIRS):
                return self.th["text"]
            curses.init_pair(pair, n, -1)
            self.glowp[n] = curses.color_pair(pair)
        return self.glowp[n]

    def draw_logo(self, top: int, left: int) -> None:
        italic = getattr(curses, "A_ITALIC", 0)
        extra = {"star": curses.A_BOLD, "title": curses.A_BOLD, "tag": italic, "ring": 0}
        if not self.rich:  # 8/16 cores: logo parado nas cores do tema
            look = {"ring": self.th["dim"], "star": self.th["peek"], "title": self.th["text"], "tag": self.th["peek"]}
            for y, x, c, tone in self.logo:
                self.put(top + y, left + x, c, look[tone] | extra[tone])
            return
        for y, x, c, rgb, tone in frame(self.logo, time.time() - self.t0):
            self.put(top + y, left + x, c, self.glow(rgb) | extra[tone])

    def splash(self) -> None:
        """Logo do Valinor acendendo no meio da tela ao abrir. Some com qualquer tecla ou depois de INTRO s."""
        H, W = self.scr.getmaxyx()
        if not self.logo or self.logo_w + 4 > W or self.logo_h + 4 > H:
            return  # terminal pequeno demais: vai direto para o seletor
        self.t0 = time.time()
        while True:
            self.scr.erase()
            self.draw_logo((H - self.logo_h) // 2, (W - self.logo_w) // 2)
            self.scr.refresh()
            left = INTRO - (time.time() - self.t0)
            if left <= 0 or select.select([sys.stdin], [], [], min(left, FRAME))[0]:
                break
        try:
            while True:
                self.scr.get_wch()  # descarta a tecla que pulou a abertura
        except curses.error:
            pass
        self.dirty = True

    def welcome(self) -> None:
        a, d = self.th["accent"], self.th["dim"]
        rows = [("✻ ", a | curses.A_BOLD), ("Valinor", curses.A_BOLD)], [], \
            [(f"  {self.host}:{self.port}", d)], \
            [(f"  base: {len(self.base.rooms)} salas · {len(self.base.regions)} regiões · {len(self.base.data['object'])} objetos", d)], \
            [("  logs em " + (str(LOGS.relative_to(mapa.MUD)) if mapa.MUD in LOGS.parents else "…" + str(LOGS)[-40:]), d)], \
            [("  /ajuda para os comandos do cliente", d)]
        w = 2 + max(len("".join(t for t, _ in r)) for r in rows)
        self.push([("╭" + "─" * w + "╮", a)])
        for r in rows:
            n = len("".join(t for t, _ in r))
            self.push([("│ ", a)] + list(r) + [(" " * (w - n - 1) + "│", a)])
        self.push([("╰" + "─" * w + "╯", a)])
        self.push([])


if __name__ == "__main__":
    art = render()
    TXT.write_text("\n".join(art) + "\n", encoding="utf-8")
    print("\n".join(art))
