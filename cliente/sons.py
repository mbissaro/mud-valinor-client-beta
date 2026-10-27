"""Sons do Fantasy Chess no modo leitor de tela: golpe dado, golpe levado, esquiva, bloqueio, morte, nível, item, porta,
comida, conversa, vida baixa e Vazio, cada um com o seu som, para quem não vê saber o que aconteceu antes da fala.

Os .wav de sons/ vêm de fantasychess/static/data/sfx: mono, 22 kHz, com o volume (gain x categoria) e o corte (maxMs)
do CATALOG do sfx-core.js do Fantasy Chess, assim:
ffmpeg -i <id>.mp3 -ac 1 -ar 22050 -t <maxMs> -af volume=<gain>,afade=t=out:st=<maxMs-0.03>:d=0.03 sons/<id>.wav
Tocam pelo winsound no Windows, afplay no macOS e paplay, pw-play ou aplay no Linux; sem nenhum deles, conversa e aviso
tocam o sino do terminal. O som só toca: nada é mandado ao jogo (POLICY 4)."""
from __future__ import annotations

import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

from conexao import WIN

DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / "sons"  # no binário os sons vão dentro dele
UP = "A-ZÁÉÍÓÚÂÊÔÃÕÇ"
CUES = [  # (linha do jogo, sons possíveis): vale a primeira que casar, e o som sai ao acaso entre os da linha
    (re.compile(r"^PARABÉNS! Você atingiu"), ("levelup1",)),
    (re.compile(r"\b(lobo|loba|cão|cachorro|lobos)\b.* está MORT[OA]!!"), ("wolf2",)),
    (re.compile(r" está MORT[OA]!!"), ("bandit-death", "bandit-death2")),
    (re.compile(rf"^Você [{UP}]{{3,}} |^Seu golpe "), ("sword-stroke",)),  # Você MASSACRA, Seu golpe arranha
    (re.compile(rf"[{UP}]{{4,}} você"), ("punch4-exagered", "punch5-exagered")),  # X DESTRUIU você
    (re.compile(r"acertou você|machucou muito você|você levemente"), ("punch1", "punch3", "punch2-slow")),
    (re.compile(r"^Você se esquivou"), ("miss1",)),
    (re.compile(r"impediu seu ataque"), ("impact-sword-shield", "impact-sword-shield-02")),
    (re.compile(r"^Você (pegou|comprou) "), ("item-take",)),
    (re.compile(r"^Você (usa|veste|empunha|segura) "), ("item-equip",)),
    (re.compile(r"^Você (abriu|fechou|destrancou|trancou) "), ("container-open",)),
    (re.compile(r"^Você comeu "), ("cook-plop",)),
    (re.compile(r"^Você bebeu "), ("cook-bubble",)),
    (re.compile(r"^Você desapareceu no Vazio"), ("cook-dubious",)),
]
TELL, CHAT, LOWHP, IDLE = "cook-done", "spin-full", "lowhp", "cook-dubious"


def cue(line: str) -> str | None:
    """Som de uma linha do jogo, ou None."""
    for rx, names in CUES:
        if rx.search(line):
            return random.choice(names)
    return None


def player() -> list[str] | None:
    """Comando que toca um .wav sem abrir janela, fora do Windows."""
    for exe in ("afplay", "paplay", "pw-play", "aplay"):
        path = shutil.which(exe)
        if path:
            return [path, "-q"] if exe == "aplay" else [path]
    return None


class Som:
    def __init__(self) -> None:
        self.cmd = None if WIN else player()
        self.ok = WIN or self.cmd is not None
        self.max = 1 if WIN else 3  # sons de uma vez: no Windows o novo corta o anterior

    def play(self, name: str) -> bool:
        """Toca sem esperar o fim; False quando não há como tocar."""
        f = DIR / f"{name}.wav"
        if not self.ok or not f.exists():
            return False
        try:
            if WIN:
                import winsound  # um som por vez: o novo corta o anterior
                winsound.PlaySound(str(f), winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
            else:
                subprocess.Popen(self.cmd + [str(f)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        except (OSError, RuntimeError):
            return False
        return True
