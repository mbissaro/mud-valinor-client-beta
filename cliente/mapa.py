"""Base do cliente: acha a sala atual em db/valinor.json, desenha o minimapa e calcula rotas.

Reaproveita o parser de salas do db/tools/minerar.py (o mesmo que gera a base a partir do raw.log)
e o posicionamento em grade do mapa do artifact (DIRV: cada saída empurra a vizinha na sua direção)."""
from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Callable

MUD = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MUD / "db" / "tools"))
from minerar import DIRS, parse_rooms, words  # noqa: E402

# mesmos vetores do DIRV do artifact, norte para cima; u/d não entram na grade
V = {"n": (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0), "ne": (1, -1), "nw": (-1, -1), "se": (1, 1), "sw": (-1, 1)}
ORDER = ["n", "ne", "e", "se", "s", "sw", "w", "nw", "u", "d"]
OPP = {"n": "s", "s": "n", "e": "w", "w": "e", "ne": "sw", "sw": "ne", "nw": "se", "se": "nw", "u": "d", "d": "u"}
Step = tuple  # (direção, id da sala de chegada)


def fold(s: str) -> str:
    return " ".join(words(s))


def matches(query: str, *texts: str) -> bool:
    """Cada palavra da busca é começo de alguma palavra do texto, sem acento: 'taver tronco' acha a taverna."""
    ws = [w for t in texts for w in words(t)]
    return all(any(w.startswith(q) for w in ws) for q in words(query))


def exits_of(room: dict) -> set[str]:
    return {e.lstrip("!") for e in room.get("exits", []) if e.lstrip("!") in DIRS.values()}


def sort_dirs(ds) -> list[str]:
    return sorted(ds, key=lambda d: ORDER.index(d) if d in ORDER else 99)


def last_room(raw: str) -> dict | None:
    """Última sala do trecho bruto (com \\r), no formato do SMAUG; None se não houver."""
    rooms, visits, _ = parse_rooms(raw, set())
    return rooms[visits[-1]] if visits else None


def speedwalk(dirs: list[str]) -> str:
    out: list[list] = []
    for d in dirs:
        if out and out[-1][0] == d:
            out[-1][1] += 1
        else:
            out.append([d, 1])
    return " ".join(f"{n}{d}" if n > 1 else d for d, n in out)


class Base:
    def __init__(self, path: Path = MUD / "db" / "valinor.json") -> None:
        self.path = path
        self.load()

    def load(self) -> None:
        d = json.loads(self.path.read_text())
        self.data = d
        self.rooms = {r["id"]: r for r in d["room"]}
        self.regions = {r["id"]: r["name"] for r in d["region"]}
        self.by_text = {(r["title"], fold(r["description"])): r["id"] for r in d["room"]}
        self.by_title: dict[str, list[str]] = defaultdict(list)
        for r in d["room"]:
            self.by_title[r["title"]].append(r["id"])
        # a base só guarda a ligação no sentido percorrido; a volta vale se a sala de chegada tem a saída oposta
        self.links = {k: dict(r.get("links", {})) for k, r in self.rooms.items()}
        for a, r in self.rooms.items():
            for d, b in r.get("links", {}).items():
                back = OPP.get(d)
                if b in self.rooms and back in exits_of(self.rooms[b]):
                    self.links[b].setdefault(back, a)

    def region(self, rid: str | None) -> str:
        r = self.rooms.get(rid or "")
        return self.regions.get(r["region"], r["region"]) if r else ""

    def identify(self, title: str, desc: str, exits: set[str], prev: str | None = None,
                 moved: str | None = None) -> str | None:
        """Texto exato primeiro; depois a saída tomada a partir da sala anterior; depois título + saídas."""
        rid = self.by_text.get((title, fold(desc)))
        if rid:
            return rid
        cands = self.by_title.get(title, [])
        via = self.links.get(prev or "", {}).get(moved or "")
        if via in cands:
            return via
        same = [c for c in cands if exits_of(self.rooms[c]) == exits]
        if len(same) == 1:
            return same[0]
        return cands[0] if len(cands) == 1 else None

    def route(self, src: str, goal: Callable[[str], bool]) -> list[Step] | None:
        """BFS pelas ligações percorridas em jogo (como o findRoute do artifact). [] = já está lá."""
        prev: dict[str, Step | None] = {src: None}
        q = deque([src])
        while q:
            a = q.popleft()
            if goal(a):
                path = []
                while prev[a]:
                    b, d = prev[a]
                    path.append((d, a))
                    a = b
                return path[::-1]
            for d, b in self.links[a].items():
                if b in self.rooms and b not in prev:
                    prev[b] = (a, d)
                    q.append(b)
        return None

    def nearest(self, src: str | None, query: str) -> tuple[str, list[Step]] | None:
        """Sala mais próxima cujo título, região ou id casa com a busca; sem posição, a primeira que casar."""
        ok = lambda r: matches(query, self.rooms[r]["title"], self.region(r), r)  # noqa: E731
        if src in self.rooms:
            path = self.route(src, ok)
            if path is not None:
                return (path[-1][1] if path else src), path
        rid = next((r for r in self.rooms if ok(r)), None)
        return (rid, []) if rid else None

    def search(self, query: str, limit: int = 30) -> list[tuple[str, str, str]]:
        """(tipo, nome, onde) de salas, NPCs, criaturas, itens, objetos, locais e regiões."""
        out = []
        for kind, key, label in (("region", "name", "região"), ("location", "name", "local"), ("room", "title", "sala"),
                                 ("npc", "name", "npc"), ("creature", "name", "criatura"), ("item", "name", "item"),
                                 ("object", "name", "objeto")):
            for e in self.data.get(kind, []):
                if matches(query, e.get(key, "")):
                    where = e.get("region") or (e.get("regions") or [""])[0]
                    if kind == "object" and e.get("rooms"):
                        where = self.rooms.get(e["rooms"][0], {}).get("title", "")
                    out.append((label, e.get(key, ""), self.regions.get(where, where)))
        return out[:limit]

    def minimap(self, center: str, cols: int, rows: int, route: frozenset = frozenset(), peek: frozenset = frozenset(),
                here: str | None = None) -> tuple[list[list[tuple]], dict[tuple[int, int], str]]:
        """(grade de (caractere, estilo), {(linha, coluna): sala} das células [x] para o clique). Sala a cada 4 colunas
        e 2 linhas; a BFS a partir do centro põe cada vizinha na direção da saída e pula as que cairiam numa célula
        ocupada (o mapa do MUD não é euclidiano). here = onde você está (o @); sem ele, o centro."""
        here = center if here is None else here
        W, H = max(1, cols // 4), max(1, (rows + 1) // 2)
        ox, oy = W // 2, H // 2
        pos, taken, q = {center: (0, 0)}, {(0, 0)}, deque([center])
        while q:
            a = q.popleft()
            ax, ay = pos[a]
            for d, b in self.links[a].items():
                if d not in V or b in pos or b not in self.rooms:
                    continue
                p = (ax + V[d][0], ay + V[d][1])
                if p in taken or not (0 <= p[0] + ox < W and 0 <= p[1] + oy < H):
                    continue
                pos[b] = p
                taken.add(p)
                q.append(b)
        grid = [[(" ", "")] * cols for _ in range(rows)]
        cells: dict[tuple[int, int], str] = {}

        def put(y: int, x: int, ch: str, st: str) -> None:
            if 0 <= y < rows and 0 <= x < cols:
                if {grid[y][x][0], ch} == {"╱", "╲"}:
                    ch = "╳"
                grid[y][x] = (ch, st)

        for a, (x, y) in pos.items():
            cx, cy = (x + ox) * 4 + 1, (y + oy) * 2
            r = self.rooms[a]
            ex, links = exits_of(r), self.links[a]
            for d in ex & V.keys():
                dx, dy = V[d]
                b = links.get(d)
                st = "new" if b is None else "link" if pos.get(b) == (x + dx, y + dy) else "far"
                put(cy + dy, cx + 2 * dx, "─" if dy == 0 else "│" if dx == 0 else "╱" if dx * dy < 0 else "╲", st)
            st = "cur" if a == here else "route" if a in route else "peek" if a in peek else "room"
            mid = "@" if a == here else "↕" if {"u", "d"} <= ex else "↑" if "u" in ex else "↓" if "d" in ex else " "
            for i, ch in enumerate(("[", mid, "]")):
                put(cy, cx - 1 + i, ch, st)
                cells[(cy, cx - 1 + i)] = a
        return grid, cells
