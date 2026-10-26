"""Abas de conversa e janela do who.

As linhas de chat que o servidor manda continuam no Jogo e também vão para uma aba: o (OOC) de todos para a Global,
o tell (telepático) e o sussurro de um jogador para a aba dele. Na aba, o que você digita sai como `chat <texto>` ou
`tell <nome> <texto>`: é o seu Enter, como um alias. O who só é lido quando você digita who ou clica no ↻; o cliente
não pergunta sozinho (POLICY 4). Clicar num nome do who abre a aba da pessoa sem mandar nada."""
from __future__ import annotations

import curses
import re
import time
from collections import deque

TALK_LINES = 1000
TELL_OUT = re.compile(r"^\(OOC\) Você (?:disse|perguntou|exclamou) telepaticamente para (.+?) '(.*)$")
TELL_IN = re.compile(r"^\(OOC\) (.+?) (?:disse|perguntou|exclamou) telepaticamente '(.*)$")
OOC = re.compile(r"^\(OOC\) (\[OSAY\] )?(.+?) (?:disse|perguntou|exclamou) '(.*)$")
WHISPER_OUT = re.compile(r"^Você sussurrou para (.+?) '(.*)$")
WHISPER_IN = re.compile(r"^(.+?) sussurrou para você '(.*)$")
PLAYER = re.compile(r"[A-ZÀ-Ý][a-zà-ÿ]+")  # jogador tem nome de uma palavra; "O guarda", "a professora X" não
# who em cores: [   6 Hum Gue ]  Fulano de Bri, o Aventureiro      [ DESCONECTADO ]
WHO_ROW = re.compile(r"^\[\s*(\d*)\s+(\S{3})\s+(\S{3})\s*\]\s+([^\s,]+)(.*?)(?:\[\s*(.*?)\s*\])?\s*$", re.M)
# modo aural: Fulano de Bri, o Recruta, Humano, Guerreiro nível 6, NÃO AUTORIZADO
WHO_AURAL = re.compile(r"^([^\s,]+)[ ,].*?, ([^,\n]+), ([^,\n]+?) nível (\d+)(?:, ([^\n]*?))?\s*$", re.M)
WHO_END = re.compile(r"(\d+) personage(?:m|ns) encontrados?")


def who_scan(text: str) -> list[tuple[str, str, str, str, str]] | None:
    """(nome, nível, raça, classe, situação) de cada linha do who; None se o texto não traz um who."""
    end = WHO_END.search(text)
    if not end:
        return None
    text = text[:end.start()].replace("\r", "")
    rows = [(m[4], m[1], m[2], m[3], m[6] or "") for m in WHO_ROW.finditer(text)]
    return rows or [(m[1], m[4], m[2][:3], m[3][:3], m[5] or "") for m in WHO_AURAL.finditer(text)]


def chat_of(text: str) -> tuple[str, str, str] | None:
    """(aba, quem fala, mensagem) de uma linha de chat; a aba é 'global' ou o nome do jogador."""
    for rx, out in ((TELL_OUT, True), (TELL_IN, False), (WHISPER_OUT, True), (WHISPER_IN, False)):
        m = rx.match(text)
        if m and PLAYER.fullmatch(m[1]):
            return m[1], "você" if out else m[1], m[2].rstrip("'")
    m = OOC.match(text)
    if m and "telepaticamente" not in m[2]:
        who = "você" if m[2] == "Você" else m[2] + (" (sala)" if m[1] else "")
        return "global", who, m[3].rstrip("'")
    return None


class Conversa:
    """Parte do App das abas e do who; usa th, put, send, say, sock, ingame, char, scroll e dirty dele."""

    def talk_init(self) -> None:
        self.talk: dict[str, dict] = {"global": {"name": "Global", "lines": deque(maxlen=TALK_LINES), "unread": 0}}
        self.chan: str | None = None  # aba aberta: None é o Jogo
        self.who: list = []
        self.who_at = 0.0

    def who_seen(self, text: str) -> None:
        rows = who_scan(text)
        if rows is not None:
            self.who, self.who_at, self.dirty = rows, time.time(), True

    def tab_for(self, name: str) -> str:
        key = name.casefold() if name != "global" else name
        self.talk.setdefault(key, {"name": name, "lines": deque(maxlen=TALK_LINES), "unread": 0})
        return key

    def talk_seen(self, text: str) -> None:
        got = chat_of(text)
        if not got:
            return
        key = self.tab_for(got[0])
        tab = self.talk[key]
        tab["lines"].append([(time.strftime("%H:%M "), self.th["far"]),
                             (got[1], self.th["accent" if got[1] == "você" else "route"] | curses.A_BOLD),
                             ("  " + got[2], self.th["text"])])
        if key == self.chan:
            if self.scroll:
                self.scroll += 1
        else:
            tab["unread"] += 1
            if key != "global" and got[1] != "você":
                try:
                    curses.beep()  # tell chegando com a aba fechada
                except curses.error:
                    pass

    def set_chan(self, key: str | None) -> None:
        self.chan, self.scroll, self.dirty = key, 0, True
        if key:
            self.talk[key]["unread"] = 0

    def next_chan(self) -> None:
        keys = [None] + list(self.talk)
        self.set_chan(keys[(keys.index(self.chan) + 1) % len(keys)])

    def close_tab(self, key: str) -> None:
        if key != "global":
            self.talk.pop(key, None)
            if self.chan == key:
                self.set_chan(None)

    def view(self) -> tuple:
        """(linhas, linha incompleta) da aba aberta."""
        return (self.lines, self.partial) if self.chan is None else (self.talk[self.chan]["lines"], [])

    def chan_label(self) -> str | None:
        if self.chan is None:
            return None
        return "chat" if self.chan == "global" else "tell " + self.talk[self.chan]["name"]

    def chatting(self) -> bool:
        """Na aba de conversa o texto é mensagem: sem autocompletar comandos do jogo."""
        return self.chan is not None and not self.inp.startswith("/")

    def talk_send(self, text: str) -> None:
        """O que você digitou numa aba de conversa vira o comando dela."""
        if text.strip():
            self.send(f"{self.chan_label()} {text}")

    def who_refresh(self) -> None:
        if not (self.sock and self.ingame):
            return self.say("entre no jogo para ver quem está online", "bad")
        self.send("who")  # você clicou: um alias, não um gatilho

    def spot_click(self, spot: tuple) -> None:
        kind, val = spot
        if kind == "tab":
            self.set_chan(val)
        elif kind == "close":
            self.close_tab(val)
        elif kind == "who" and val != self.char:
            self.set_chan(self.tab_for(val))
        elif kind == "who-refresh":
            self.who_refresh()
        elif kind == "dock":
            self.dock = val
        elif kind == "bag-refresh":
            self.bag_refresh()
        self.dirty = True

    # ------------------------------------------------------------------ desenho
    def draw_tabs(self, y: int, end: int) -> None:
        """Faixa das abas em cima do texto: Jogo, Global e uma por pessoa, com as mensagens não lidas."""
        x = 1
        for key, name, unread in [(None, "Jogo", 0)] + [(k, t["name"], t["unread"]) for k, t in self.talk.items()]:
            on = key == self.chan
            x0 = x
            x = self.put(y, x, f" {name} ", (self.th["accent"] | curses.A_BOLD | curses.A_REVERSE) if on
                         else self.th["dim"], end)
            if unread:
                x = self.put(y, x, f"{unread} ", self.th["new"] | curses.A_BOLD, end)
            self.spots[(y, x0, x)] = ("tab", key)
            if key not in (None, "global"):
                self.spots[(y, x, x + 2)] = ("close", key)
                x = self.put(y, x, "× ", self.th["far"], end)
            x += 1
        hint = "F3 troca de aba · Esc volta ao jogo" if self.chan else "F3 troca de aba"
        if end - len(hint) - 1 > x:
            self.put(y, end - len(hint) - 1, hint, self.th["far"])

    def draw_who(self, x: int, top: int, rows: int, w: int) -> None:
        end = x + w
        cx = self.put(top, x, "ONLINE", self.th["accent"] | curses.A_BOLD, end)
        if self.who_at:
            cx = self.put(top, cx, f" {len(self.who)}", self.th["new"] | curses.A_BOLD, end)
        self.spots[(top, end - 6, end)] = ("who-refresh", None)
        self.put(top, end - 6, "↻ who", self.th["route"] | curses.A_BOLD, end)
        if not self.who_at:
            self.put(top + 2, x + 2, "digite who ou clique ↻", self.th["far"], end)
            return
        fit = rows - 1 if len(self.who) <= rows - 1 else rows - 2
        nw = min(w // 2, max((len(r[0]) for r in self.who[:fit]), default=0))  # nomes alinhados em coluna
        for i, (name, lvl, race, cls, status) in enumerate(self.who[:fit]):
            y = top + 1 + i
            me = name == self.char
            tab = self.talk.get(name.casefold())
            hover = self.spot_hover == ("who", name)
            attr = self.th["accent" if me else "text"] | curses.A_BOLD | (curses.A_REVERSE if hover and not me else 0)
            cx = self.put(y, x, "●" if tab else "·", self.th["route" if tab else "far"], end)
            self.put(y, cx + 1, name[:nw], attr, end)
            cx = self.put(y, cx + 1 + nw, f" {lvl or '—':>3} {race} {cls}", self.th["dim"], end)
            if tab and tab["unread"]:
                cx = self.put(y, cx, f"  {tab['unread']} nova" + ("s" if tab["unread"] > 1 else ""), self.th["new"], end)
            note = "você" if me else status.lower()
            if note and end - len(note) > cx + 1:
                self.put(y, end - len(note), note, self.th["bad" if "desconect" in note else "dim"], end)
            if not me:
                self.spots[(y, x, end)] = ("who", name)
        if len(self.who) > fit:
            self.put(top + rows - 1, x + 2, f"… +{len(self.who) - fit}", self.th["far"], end)
