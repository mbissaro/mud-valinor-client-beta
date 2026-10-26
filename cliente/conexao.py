"""Telnet, credenciais e checagem de outras conexões abertas com o Valinor."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import mapa

CRED = Path(os.environ.get("VALINOR_CRED", mapa.MUD / ".credenciais"))  # Personagem<X>: nome / Senha<X>: senha
LOGS = Path(os.environ.get("VALINOR_LOGS", mapa.MUD / "logs"))  # VALINOR_LOGS=<pasta> nos testes
LABELS = {"": "humano guerreiro · Bri", "Anao": "anão clérigo · Esgaroth", "Hobbit": "hobbit ladino · Bri"}
IAC, DONT, DO, WONT, WILL, SB, SE, ECHO = 255, 254, 253, 252, 251, 250, 240, 1


def telnet(buf: bytes) -> tuple[bytes, bool | None, bytes]:
    """Tira as sequências IAC. Devolve (dados, servidor_ecoa, resto incompleto para o próximo pacote).
    WILL ECHO = o servidor vai cuidar do eco (pedido de senha), então a caixa de entrada esconde o texto."""
    out, echo, i = bytearray(), None, 0
    while i < len(buf):
        if buf[i] != IAC:
            out.append(buf[i])
            i += 1
            continue
        if i + 1 >= len(buf):
            break
        c = buf[i + 1]
        if c == IAC:
            out.append(IAC)
            i += 2
        elif c in (WILL, WONT, DO, DONT):
            if i + 2 >= len(buf):
                break
            if buf[i + 2] == ECHO and c in (WILL, WONT):
                echo = c == WILL
            i += 3
        elif c == SB:
            j = buf.find(bytes([IAC, SE]), i)
            if j < 0:
                break
            i = j + 2
        else:
            i += 2
    return bytes(out), echo, buf[i:]


def _rows() -> list[tuple[str, str]]:
    try:
        return [tuple(l.split(": ", 1)) for l in CRED.read_text().splitlines() if ": " in l]
    except OSError:
        return []


def load_chars() -> list[tuple[str, str, str]]:
    """(nome, descrição, sufixo) de cada par Personagem<X>/Senha<X> do .credenciais; a senha só é lida no login."""
    rows = _rows()
    keys = {k for k, _ in rows}
    return [(v.strip(), LABELS.get(k[10:], ""), k[10:]) for k, v in rows
            if k.startswith("Personagem") and "Senha" + k[10:] in keys]


def secret(key: str) -> str:
    return next((v.strip() for k, v in _rows() if k == key), "")


def secrets() -> list[str]:
    """Todas as senhas do .credenciais, só para o auto-complete nunca sugerir nenhuma."""
    return [v.strip() for k, v in _rows() if k.startswith("Senha") and v.strip()]


def other_connections() -> list[str]:
    """Outras conexões desta máquina com o Valinor: o mud.sh ou outro cliente aberto."""
    out = []
    try:
        if subprocess.run(["pgrep", "-f", "[s]ocat - TCP:mud.valinor"], capture_output=True).stdout.strip():
            out.append("mud.sh")
        pids = subprocess.run(["pgrep", "-f", r"^(\S*/)?python[0-9.]* \S*valinor\.py"], capture_output=True,
                              text=True).stdout.split()
        if {int(p) for p in pids} - {os.getpid(), os.getppid()}:
            out.append("outro cliente")
    except OSError:
        pass
    return out
