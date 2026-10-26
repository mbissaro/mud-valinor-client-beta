"""Auto-complete do cliente: comandos que você já usou (logs/transcript.log), palavras da sala e do texto recente,
nomes da base para os argumentos de /rota, /mapa, /sala e /busca.

Senha nunca vira sugestão: ignora todo comando que contém uma senha do .credenciais e todo comando digitado logo
depois de um pedido de senha (cobre senhas antigas que ficaram no transcript)."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import mapa

CMD = re.compile(r"^>>> \[\d\d:\d\d:\d\d\] (.*)$")
EMAIL = re.compile(r"\S+@\S+\.\w")
WORD = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]{2,}")
STOP = set("""uma umas uns para com que está estão aqui seu sua seus suas dos das nos nas pelo pela pelos pelas mais
muito muita como sobre entre este esta esse essa isso isto aquele aquela você não sim tem foi ser são pode bem ainda
onde quando também outro outra outros outras todo toda todos todas cada ele ela eles elas lhe por num numa até sem
the and""".split())
BASIC = """n s e w ne nw se sw u d look examine get drop put give wear remove wield hold eat drink fill sleep wake rest
stand inventory equipment score who say tell chat ooc kill flee consider list buy sell value open close search cook
recall recite quit help areas time weather practice train sneak hide slice""".split()
MAX = 6
ROOM_ARG = {"/rota", "/mapa", "/sala"}
KINDS = (("region", "name", "região"), ("location", "name", "local"), ("room", "title", "sala"), ("npc", "name", "npc"),
         ("creature", "name", "criatura"), ("item", "name", "item"), ("object", "name", "objeto"))


class Completer:
    def __init__(self, base: mapa.Base, transcript: Path, secrets: list[str]) -> None:
        self.base = base
        self.secrets = [s for s in secrets if s]
        self.first = Counter({c: 0 for c in BASIC})  # primeira palavra -> vezes usada
        self.args: Counter = Counter()
        self.recent: dict[str, None] = {}  # comandos inteiros, o mais recente por último
        try:
            lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            lines = []
        asked = False
        for ln in lines:
            m = CMD.match(ln)
            if m:
                if not asked:
                    self.learn(m.group(1))
                asked = False
            elif ln.strip():
                asked = "senha" in ln.lower()
        self.reload()

    def reload(self) -> None:
        """Pools (texto, texto sem acento, descrição): salas e regiões para /rota, tudo da base para /busca."""
        b = self.base
        rooms: dict[str, list[str]] = {}
        for rid, r in b.rooms.items():
            rooms.setdefault(r["title"], []).append(rid)
        titles = {t: b.region(ids[0]) if len(ids) == 1 else f"{len(ids)} salas" for t, ids in rooms.items()}
        titles.update({n: "região" for n in b.regions.values()})
        names = {e[key]: label for kind, key, label in KINDS for e in b.data.get(kind, []) if e.get(key)}
        self.titles = [(t, mapa.fold(t), d) for t, d in sorted(titles.items())]
        self.names = [(t, mapa.fold(t), d) for t, d in sorted(names.items())]

    def learn(self, cmd: str) -> None:
        cmd = cmd.strip()
        if not cmd or any(s in cmd for s in self.secrets) or EMAIL.search(cmd):
            return
        self.recent.pop(cmd, None)
        self.recent[cmd] = None
        if cmd.startswith("/"):
            return
        ws = cmd.split()
        self.first[ws[0].lower()] += 1
        self.args.update(w.lower() for w in ws[1:] if len(w) >= 3)

    def ghost(self, inp: str) -> str:
        """Resto do comando mais recente que começa com o que já foi digitado (aceita com → no fim da linha)."""
        if len(inp) < 2:
            return ""
        return next((c[len(inp):] for c in reversed(self.recent) if c.startswith(inp) and len(c) > len(inp)), "")

    def words(self, prefix: str, first: bool, here: list[str], seen: list[str]) -> list[tuple[str, str]]:
        p = mapa.fold(prefix)
        if first:
            pool = [(w, f"{n}×" if n else "comando") for w, n in self.first.most_common()]
        else:
            pool = [(w, "na sala") for w in here] + [(w, "na tela") for w in seen] + \
                   [(w, f"usado {n}×") for w, n in self.args.most_common()]
        out, got = [], set()
        for w, d in pool:
            k, f = w.lower(), mapa.fold(w)
            if k not in got and f.startswith(p) and f != p:
                got.add(k)
                out.append((k, d))
                if len(out) == MAX:
                    break
        return out

    def phrases(self, arg: str, pool: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
        """Títulos/nomes que começam com o argumento; depois os que casam palavra por palavra ('taver rama')."""
        q = mapa.fold(arg)
        qs = q.split()
        head = [(t, d) for t, f, d in pool if f.startswith(q) and f != q]
        rest = [(t, d) for t, f, d in pool if not f.startswith(q) and all(any(w.startswith(x) for w in f.split())
                                                                           for x in qs)]
        return (head + rest)[:MAX]

    def complete(self, text: str, here: list[str], seen: list[str],
                 commands: dict[str, str]) -> tuple[int, list[tuple[str, str]]]:
        """(coluna onde a sugestão entra, [(sugestão, descrição)]) para o texto até o cursor."""
        if text.startswith("/"):
            name, sp, arg = text.partition(" ")
            if not sp:
                return 0, [(c, d) for c, d in commands.items() if c.startswith(name)]
            name = name if name in commands else next((c for c in commands if c.startswith(name)), name)
            pool = self.titles if name in ROOM_ARG else self.names if name == "/busca" else []
            return len(text) - len(arg), self.phrases(arg, pool)
        start = text.rfind(" ") + 1
        return start, self.words(text[start:], start == 0, here, seen)


def text_words(lines: list[str]) -> list[str]:
    """Palavras úteis (3+ letras, sem artigos e preposições) na ordem em que aparecem, sem repetir."""
    out: dict[str, None] = {}
    for ln in lines:
        for w in WORD.findall(ln):
            if w.lower() not in STOP:
                out[w.lower()] = None
    return list(out)
