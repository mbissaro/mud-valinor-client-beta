"""Aviso antes da desconexão por inatividade, e sinal quando a conexão cai.

O Valinor (SMAUG) põe no Vazio quem passa 8 ticks sem digitar nada e tira do jogo 4 ticks depois. Medido no transcript:
o tick dura de 60 a 80 s, então o Vazio vem por volta dos 8-10 min parado e o quit uns 4-5 min depois. O cliente só
avisa (linha na tela, sino e notificação da área de trabalho): quem volta é você, digitando. Mandar comando sozinho
para segurar a conexão é automação, e a POLICY 4 proíbe."""
from __future__ import annotations

import curses
import math
import shutil
import socket
import subprocess
import time

TICK = 70  # segundos: média entre as mensagens de fome do transcript (60 a 80)
VOID_TICKS, QUIT_TICKS = 8, 4
SHOW, WARN = 3 * 60, 6 * 60  # o contador aparece na barra; o aviso toca (o Vazio vem a partir de ~7,5 min)
VOID = "Você desapareceu no Vazio."


def keepalive(sock: socket.socket) -> None:
    """Sonda TCP vazia depois de 1 min sem tráfego: roteador e NAT não derrubam a conexão parada, e uma queda de verdade
    aparece em ~2 min em vez de ficar muda. Fica abaixo do telnet: o jogo não vê comando nenhum."""
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    for opt, v in (("TCP_KEEPIDLE", 60), ("TCP_KEEPINTVL", 20), ("TCP_KEEPCNT", 4)):
        if hasattr(socket, opt):
            sock.setsockopt(socket.IPPROTO_TCP, getattr(socket, opt), v)


def notify(text: str) -> None:
    exe = shutil.which("notify-send")
    if exe:
        subprocess.Popen([exe, "-a", "Valinor", "Valinor", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class Vigia:
    """Parte do App que conta o tempo parado; usa say, ingame e dirty dele."""

    def idle_reset(self) -> None:
        """Você mandou uma linha: o servidor zera o contador de inatividade."""
        self.typed_at, self.void_at, self.warned = time.time(), 0.0, False
        self.idle_shown: tuple | None = None

    def idle_seen(self, text: str) -> None:
        if VOID in text and not self.void_at:
            self.void_at = time.time()
            self.alert(f"⚠ você foi para o Vazio por estar parado: o servidor tira você do jogo em ~{QUIT_TICKS * TICK // 60}-"
                       f"{math.ceil(QUIT_TICKS * TICK / 60)} min. "
                       "Digite um comando para voltar.")

    def idle_tick(self) -> None:
        if self.ingame and not self.void_at and not self.warned and time.time() - self.typed_at >= WARN:
            self.warned = True
            self.alert(f"⏰ parado há {WARN // 60} min: lá pelos 8-10 min o servidor põe você no Vazio e uns 4 min depois "
                       "desconecta. Digite um comando para continuar.")
        label = self.idle_label()
        if label != self.idle_shown:
            self.idle_shown, self.dirty = label, True

    def idle_label(self) -> tuple[str, str] | None:
        """(texto, estilo) do contador da barra de baixo, ou None enquanto não importa."""
        if not self.ingame:
            return None
        now = time.time()
        if self.void_at:
            left = math.ceil(max(0.0, self.void_at + QUIT_TICKS * TICK - now) / 60)
            return f"◷ no Vazio · quit em ~{left} min", "bad"
        idle = now - self.typed_at
        if idle < SHOW:
            return None
        left = max(1, math.ceil((VOID_TICKS * TICK - idle) / 60))
        return f"◷ parado {int(idle // 60)} min · Vazio em ~{left} min", "new" if self.warned else "dim"

    def alert(self, text: str) -> None:
        self.say(text, "new")
        try:
            curses.beep()
        except curses.error:
            pass
        notify(text)
