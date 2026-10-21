#!/usr/bin/env python3
"""Extrai de logs/transcript.log arquivos por categoria: comandos, salas, itens, diálogos."""
import re
from pathlib import Path

D = Path(__file__).parent / "logs"
PROMPT = re.compile(r"<\d+hp \d+m \d+mv>\s*")
CMD = re.compile(r"^>>> \[(\d\d:\d\d:\d\d)\] ?(.*)$")
FALA = re.compile(r"^(\(OOC\) .*|.+? (falou|perguntou|exclamou|ponderou|disse|sussurrou|gritou|respondeu)\b.*)$")
ITEM = re.compile(r"^(Você (pegou|largou|deu|colocou|vestiu|empunhou|segurou) .*|.+ deu .+ para você\.|.+ colocou .+ na .+ de \w+\.)$")


def blocos(texto):
    """Quebra o log em blocos separados por prompts e comandos."""
    atual = []
    for linha in texto.splitlines():
        partes = PROMPT.split(linha)
        for i, p in enumerate(partes):
            if i > 0 or CMD.match(p):
                yield atual
                atual = []
            if p.strip():
                atual.append(p.rstrip())
    yield atual


def main():
    texto = (D / "transcript.log").read_text(errors="replace")
    linhas = texto.splitlines()

    comandos = [f"{m[1]}  {m[2]}" for m in map(CMD.match, linhas) if m]
    falas = [l for l in linhas if FALA.match(l) and not CMD.match(l)]
    itens = [l for l in linhas if ITEM.match(l)]

    salas = {}
    listas = []
    for b in blocos(texto):
        b = [l for l in b if not CMD.match(l)]
        idx = next((i for i, l in enumerate(b) if l.startswith("Saídas:")), None)
        if idx:
            titulo = b[0]
            salas[titulo] = "\n".join(b[1:idx + 1]) + "\n" + "\n".join(f"  - {l}" for l in b[idx + 1:])
        for i, l in enumerate(b):
            if l.endswith("contém:") or l.startswith("Você está carregando:") or l.startswith("Você está usando:"):
                listas.append("\n".join(b[i:]))

    # resposta de look/examine/glance/consider <alvo>, até o próximo prompt
    descricoes = {}
    alvo = None
    for l in linhas:
        m = CMD.match(l)
        if m:
            p = m[2].split(maxsplit=1)
            alvo = m[2] if len(p) == 2 and p[0].lower() in ("look", "l", "examine", "exa", "glance", "consider", "con") else None
            if alvo:
                descricoes[alvo] = []
            continue
        if alvo:
            antes = PROMPT.split(l)[0]
            if antes.strip():
                descricoes[alvo].append(antes.rstrip())
            if PROMPT.search(l):
                alvo = None

    # topologia: sala (título + saídas) --direção--> sala
    DIRS = {"n", "s", "e", "w", "u", "d", "ne", "nw", "se", "sw", "jaula", "sala", "enter", "leave"}
    arestas = {}
    sala_atual = None
    direcao = None
    ultimo_titulo = None
    for l in linhas:
        m = CMD.match(l)
        if m:
            direcao = m[2].strip().lower() if m[2].strip().lower() in DIRS else None
            ultimo_titulo = None
            continue
        texto = PROMPT.sub("", l).strip()
        if not texto:
            continue
        if ultimo_titulo is None:
            ultimo_titulo = texto
        if texto.startswith("Saídas:"):
            sala = f"{ultimo_titulo.replace('(Seguro) ', '')} [{texto[8:]}]"
            if direcao and sala_atual and sala_atual != sala:
                arestas[(sala_atual, direcao)] = sala
            sala_atual = sala
            direcao = None
        if "fugiu" in texto:
            direcao = "fuga"
    mapa = {}
    for (origem, d), destino in sorted(arestas.items()):
        mapa.setdefault(origem, []).append(f"  - {d} -> {destino}")
    (D / "mapa.md").write_text("# Mapa (sala [saídas] -> ligações)\n\n" + "".join(f"## {o}\n" + "\n".join(v) + "\n\n" for o, v in mapa.items()))

    (D / "descricoes.md").write_text("".join(f"## {a}\n" + "\n".join(t) + "\n\n" for a, t in descricoes.items() if t))
    (D / "comandos.log").write_text("\n".join(comandos) + "\n")
    (D / "dialogos.log").write_text("\n".join(falas) + "\n")
    (D / "itens.log").write_text("\n".join(itens) + "\n\n## Listagens\n\n" + "\n\n".join(listas) + "\n")
    (D / "salas.md").write_text("".join(f"## {t}\n{c}\n\n" for t, c in salas.items()))


if __name__ == "__main__":
    main()
