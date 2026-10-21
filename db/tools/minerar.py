#!/usr/bin/env python3
"""Minera logs/raw.log + logs/transcript.log e gera a camada BRUTA da base:

  db/data/rooms.yaml  todas as salas vistas (titulo, descricao real, saidas, mobs, objetos)
  db/data/texts.yaml  ajudas, descricoes examinadas, falas de NPC, listas de loja, dicas, criacao

Os dois arquivos sao GERADOS: nunca editar a mao, rodar de novo. Pra corrigir a regiao
de uma sala, ajuste REGION_SEEDS (a regiao das outras salas e herdada da ultima sala
conhecida na sequencia de visitas). A senha de .credenciais e emails sao redigidos.

Uso: minerar.py            gera os YAML
     minerar.py regioes    lista sala -> regiao inferida (pra revisar)
"""
from __future__ import annotations

import re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import yaml

MUD = Path(__file__).resolve().parent.parent.parent
DATA = MUD / "db" / "data"
RAW, TRANSCRIPT = MUD / "logs" / "raw.log", MUD / "logs" / "transcript.log"

# (regex do titulo, [regex da descricao,] regiao). Primeira que casar vence; sala sem seed herda a
# regiao da ultima sala visitada antes dela.
REGION_SEEDS = [
    (r"^Sala de Doações$", "region:valfenda"),
    (r"^(Seja bem-vindo ao MUD Valinor|As Regras do Jogo|O Corredor Silencioso|A Sala d[aeo]s? |Sala de |"
     r"Iniciantes e Experientes|Fim do Treinamento|Provisões para Jovens|O Refeitório|A Academia de Aventureiros$|"
     r"O (Centro|Leste|Oeste) do Jardim$)", "region:academia"),
    (r"^Os Salões de Espera$", "region:saloes-espera"),
    (r"^(O Amplo Bosque|A Academia de Combate|A Torre Mágica|O Acampamento dos Rangers|A Gruta Profunda|"
     r"A Trilha de Pedras Claras)$", "region:bosque"),
    (r"^(Um Ponto de Junção sob o Portão Sul|Outra Interseção|Uma Junção na Galeria|(Uma|A) Curva no Túnel da Galeria)$", "region:bosque.formigueiro"),
    (r"^Rua do Mercado$", "region:bri.mercado"),
    (r"^Rua da Águia$", "region:bri.aguia"),
    (r"^Avenida da Lei$", "region:bri.lei"),
    (r"(Biblioteca de Bri|O Saguão de Entrada da Biblioteca|A Antecâmara da Biblioteca|A Nave Principal da Biblioteca)", "region:bri.biblioteca"),
    (r"Pônei Saltitante", "region:bri.ponei"),
    (r"^(Contornando a Colina de Bri|Um Caminho Arborizado|A Entrada da Mina Abandonada)$", "region:bri.colina"),
    (r"(do Sítio|^Os Alojamentos dos Cavalos$|^O Portão Principal$)", "region:bri.mansao-knob"),
    (r"^Entrada para a Academia$", "Estrada Horizonte", "region:bri"),
    (r"^Entrada para a Academia$", "movimentada rua", "region:archet"),
    (r"^Entrada para a Academia$", "alameda", "region:valfenda"),
    (r"^(A Praça de Bri|Dentro do Portão|Fora do Portão|A Guarita do Portão|Próximo ao Portão Sul|A Grande Estrada Leste$|"
     r"Avenida Zênite|Rua do Xaxim|A Casa-Mathom|No Alto da Macieira|Estrada Horizonte$)", "region:bri"),
    (r"^Na Interseção$", "region:eriador.intersecao"),
    (r"^A Velha Estrada Norte", "region:eriador.estrada-norte"),
    (r"^(Antes do Cemitério|Entrada para o Cemitério|Ao Longo da Cerca de Ferro|O Caixão de Thomas|A Lápide Caída|"
     r"O Túmulo do Guerreiro Desconhecido|As Profanas Terras da Morte|A Morte de uma Criança|Um Túmulo Subterrâneo)$", "region:eriador.cemiterio"),
    (r"^O Caminho Verde", "region:eriador.caminho-verde"),
    (r"^(A Entrada de Archet|Rua dos Ofícios|Rua das Distrações|Rua das Batalhas|Hospedaria Sono Cerrado|A Torre N|A Torre S|Os Saguões de)", "region:archet"),
    (r"^(A Grande Estrada do Leste|A Última Ponte|Nos Limites de uma Floresta Sombria|O Vau do Bruinen)$", "region:estrada-leste"),
    (r"^(Em Uma Pequena Lagoa|Uma Pequena Clareira|Um Caminho Através da Floresta|Uma Junção no Caminho da Floresta|"
     r"Uma Clareira Escura Fora da Caverna|Uma Interseção no Caminho|Uma Curva no Caminho|Uma Ladeira de Pedras|"
     r"Um Caminho Através da Espessa Folhagem|Sob um Teto de Folhas)$", "region:valfenda.floresta-pinheiros"),
    (r"^(O Bosquepraça|A Ponte sobre o Bruinen|Na Entrada do Jardim de Imladris|O Salão do Fogo|A Nave Superior|"
     r"Uma Passagem Bem Guardada|O Cartógrafo|No Empório das Casas|Um Círculo Florido|Os Salões de Elrond|"
     r"Uma Alameda de|Encontro das Alamedas|Entre as Alamedas|Às Margens da Floresta$|Olhos para o Vale$|A Estrada Rochosa$|"
     r"A Casa de Descanso$|A Recepção$|Uma Sala de Espera$)", "region:valfenda"),
]

PROMPT = re.compile(r"<\d+hp \d+m \d+mv> ?")
CMD = re.compile(r"^>>> \[(\d\d:\d\d:\d\d)\] ?(.*)$")
SPEECH = re.compile(r"^(.+?) (falou|perguntou|exclamou|ponderou|disse|sussurrou|gritou|respondeu)\b(.*)$")
PLAYER = re.compile(r"^[A-Z]\w+ de [A-Z]\w+, ")
WHO = re.compile(r"^([A-Z]\w+)( de [A-Z][\w-]+)?, .+ nível \d+")
REMAINS = re.compile(r"^(O corpo|A cabeça|O rabo|A orelha|O olho|O coração|O cérebro|A língua|A pata|O braço|A perna|"
                     r"O fígado|As tripas|.*poça de sangue)")
MOB_POS = re.compile(r"(está (em pé|sentad[oa]|dormindo|descansando|deitad[oa])|está aqui, (sentad|lutando|montad)|"
                     r"brilha sob uma aura|está sob uma)")
FAIL = re.compile(r"^(Você não (vê|encontra|consegue)|Não (há|existe|vejo)|Esta pessoa não|Isto não|Hã\?|Huh\?|"
                  r"Você não está|Você não tem|Não foi possível|Ninguém)")
# mensagens assincronas que caem no meio da resposta de um comando (so tiramos as do comeco)
NOISE = re.compile(r"( foi para o | foi para a | voou para | chegou\.| chegou d| saltitou | partiu)|^(Começa um novo dia|"
                   r"A noite começa|O sol |A lua |Murmúrios ecoam|Uma paz benfazeja|O dia |Você está com (fome|sede))")
LOOKV = {"look", "l", "examine", "exa", "glance", "consider", "con", "read", "ler", "listen", "search", "vasculhar"}
HELPV = {"help", "ajuda", "policy", "book", "news", "commands", "socials", "time", "weather"}


def secret() -> str | None:
    cred = MUD / ".credenciais"
    if not cred.exists():
        return None
    return next((l[7:].strip() for l in cred.read_text().splitlines() if l.startswith("Senha: ")), None)


SENHA = secret()


def redact(s: str) -> str:
    if SENHA:
        s = s.replace(SENHA, "[REDACTED]")
    return re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[EMAIL]", s)


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48] or "x"


def clean_content(t: str) -> str:
    return re.sub(r"^\(\d+x\) ", "", t)


# ---------------------------------------------------------------- salas (raw.log)
def parse_rooms(raw: str, players: set[str]):
    """Usa o formato do SMAUG: titulo termina em \\r\\n, descricao em \\n\\r, objetos em \\r\\n, mobs em \\n\\r."""
    lines = raw.split("\n")
    rooms: dict[tuple, dict] = {}
    visits: list[tuple] = []
    remains = Counter()
    for i, l in enumerate(lines):
        if not l.lstrip("\r").startswith("Saídas:"):
            continue
        j, desc = i - 1, []
        while j >= 0 and lines[j].startswith("\r") and not lines[j].endswith("\r") and not PROMPT.search(lines[j]):
            desc.append(lines[j][1:])
            j -= 1
        if j < 1 or lines[j].endswith("\r") or PROMPT.search(lines[j]):
            continue
        desc.append(lines[j])
        title = PROMPT.split(lines[j - 1].strip("\r"))[-1].strip()
        if not title or len(title) > 70:
            continue
        safe = title.startswith("(Seguro) ")
        title = title.replace("(Seguro) ", "")
        desc_txt = "\n".join(reversed(desc)).strip()
        mobs, objs, seen_mob = [], [], False
        for c in lines[i + 1:i + 60]:
            t = c.strip("\r").strip()
            if not t or PROMPT.search(c):
                break
            t = clean_content(t)
            if SPEECH.match(t) or t.startswith("Você ") or "lutando com você" in t or t.startswith("O golpe"):
                break
            bare = re.sub(r"^(\([^)]*\) )+", "", t)
            if PLAYER.match(bare) or bare.split()[0].strip(",") in players or NOISE.search(t):
                continue
            if REMAINS.match(t):
                remains[t] += 1
                continue
            if c.endswith("\r") and not MOB_POS.search(t):
                if seen_mob:
                    break  # depois dos mobs, linha \r\n e evento (fala de mobprog etc.)
                objs.append(t)
            else:
                mobs.append(t)
                seen_mob = True
        key = (title, desc_txt)
        r = rooms.setdefault(key, {"title": title, "description": desc_txt, "safe": safe, "exits": Counter(),
                                   "mobs": Counter(), "objects": Counter(), "visits": 0, "line": i + 1})
        r["exits"][l.strip("\r")[len("Saídas:"):].strip()] += 1
        r["visits"] += 1
        r["mobs"].update(set(mobs))
        r["objects"].update(set(objs))
        visits.append(key)
    return rooms, visits, remains


def assign_regions(rooms: dict, visits: list) -> None:
    seeds = [(re.compile(s[0]), re.compile(s[1] if len(s) == 3 else ""), s[-1]) for s in REGION_SEEDS]
    votes: dict[tuple, Counter] = defaultdict(Counter)
    current = None
    for key in visits:
        seeded = next((reg for t, d, reg in seeds if t.search(key[0]) and d.search(key[1])), None)
        current = seeded or current
        votes[key][(current or "region:academia", bool(seeded))] += 1
    for key, r in rooms.items():
        (reg, seeded), _ = votes[key].most_common(1)[0]
        r["region"], r["confidence"] = reg, "confirmed" if seeded else "inferred"


# ---------------------------------------------------------------- textos (transcript.log)
def room_index(rooms: dict) -> dict[str, list[tuple]]:
    idx = defaultdict(list)
    for key, r in rooms.items():
        idx[r["description"].splitlines()[-1].strip()].append(key)
    return idx


def parse_texts(tr: str, rooms: dict, ids: dict, players: set[str]):
    lines = [PROMPT.split(l)[-1] if not CMD.match(l) else l for l in tr.splitlines()]
    idx = room_index(rooms)
    here = None
    looks: dict[tuple, set] = {}
    helps: dict[str, str] = {}
    shops: dict[str, set] = {}
    speech: dict[str, dict[str, set]] = defaultdict(dict)
    tips: dict[str, set] = {}
    cmd, out, closed = None, [], False

    def flush():
        if not cmd or not out:
            return
        p = cmd.split(maxsplit=1)
        body = list(out)
        while body and NOISE.search(body[0]):
            body.pop(0)
        v, txt = p[0].lower(), "\n".join(body).strip()
        if not txt or FAIL.match(txt):
            return
        if v in LOOKV and len(p) == 2:
            looks.setdefault((f"{v} {p[1].lower()}", txt), set()).add(here)
        elif v in HELPV:
            helps.setdefault(cmd.lower(), txt)
        elif v in ("list", "listar") and "Núm" in txt and len(txt[txt.index("Núm"):].splitlines()) > 1:
            shops.setdefault(txt[txt.index("Núm") - 1 if txt.index("Núm") else 0:].strip("\n"), set()).add(here)

    raw_lines = tr.splitlines()
    for n, l in enumerate(lines):
        m = CMD.match(l)
        if m:
            flush()
            cmd, out, closed = m[2].strip(), [], False
            continue
        t = l.strip()
        if t.startswith("Saídas:") and n > 0:
            for key in idx.get(lines[n - 1].strip(), []):
                d = rooms[key]["description"].splitlines()
                if [x.strip() for x in lines[n - len(d):n]] == [x.strip() for x in d]:
                    here = ids[key]
                    break
        if t.startswith("Dica:"):
            tips.setdefault(t, set()).add(here)
        sm = SPEECH.match(t)
        if sm and "'" in t and not t.startswith("(OOC)") and not t.startswith("Você ") and sm[1].split()[0] not in players \
                and len(sm[1]) < 50:
            speech[sm[1]].setdefault(t, set()).add(here)
        if cmd is not None and not closed:
            if t:
                out.append(l.rstrip())
            if PROMPT.search(raw_lines[n]):
                closed = True
    flush()
    return looks, helps, shops, speech, tips


def parse_creation(raw: str) -> list[dict]:
    head = raw.split("Seja bem-vindo ao MUD Valinor")[0].replace("\r", "")
    steps = [s.strip() for s in re.split(r"_{20,}", head)]
    out = []
    for s in steps[1:]:
        body = "\n".join(l.rstrip() for l in s.splitlines() if l.strip())
        if len(body) < 80:
            continue
        out.append(body)
    return out


def find_players(tr: str) -> set[str]:
    """Nomes de outros jogadores: linhas dos blocos do 'who' e quem fala no canal OOC."""
    players, inside = set(), False
    for l in tr.splitlines():
        l = PROMPT.split(l)[-1].strip()
        if l.startswith("Todos os personagens online"):
            inside = True
        elif inside and re.match(r"^\d+ personage", l):
            inside = False
        elif inside and (m := WHO.match(l)):
            players.add(m[1])
    players |= {m[1] for m in re.finditer(r"^\(OOC\) ([A-Z]\w+)(?: [A-Z]\w+)? (disse|perguntou|exclamou|falou)", tr, re.M)}
    # mestres de pericia (Zurg, Domick...) tambem falam no OOC: sao NPCs curados, nao jogadores
    npcs = {w for n in yaml.safe_load((DATA / "npcs.yaml").read_text()) for w in n["name"].split()}
    return players - npcs - {"Halbarion", "Você"}


# ---------------------------------------------------------------- main
def refs_list(s: set) -> list[str]:
    return sorted(x for x in s if x)


def main() -> None:
    raw = (RAW).read_bytes().decode("latin1")
    raw = redact(re.sub(r"\xff[\xfb-\xfe].|\xff[\xf0-\xfa]|\x1b\[[0-9;]*[a-zA-Z]", "", raw))
    tr = redact(TRANSCRIPT.read_text(errors="replace"))
    players = find_players(tr)

    rooms, visits, remains = parse_rooms(raw, players)
    assign_regions(rooms, visits)

    if sys.argv[1:] == ["regioes"]:
        for key, r in sorted(rooms.items(), key=lambda kv: kv[1]["line"]):
            print(f"{r['region']:32} {'*' if r['confidence'] == 'confirmed' else ' '} {r['title']} | {r['description'][:60]!r}")
        return

    curated = {}
    for loc in yaml.safe_load((DATA / "locations.yaml").read_text()):
        curated.setdefault(loc["name"].split(" (")[0].strip(), loc["id"])

    ids, seen = {}, Counter()
    for key, r in sorted(rooms.items(), key=lambda kv: kv[1]["line"]):
        base = f"room:{r['region'].split(':')[1]}.{slug(r['title'])}"
        seen[base] += 1
        ids[key] = base if seen[base] == 1 else f"{base}-{seen[base]}"

    out_rooms = []
    for key, r in sorted(rooms.items(), key=lambda kv: kv[1]["line"]):
        e = {"id": ids[key], "title": r["title"], "region": r["region"]}
        if r["title"] in curated:
            e["location"] = curated[r["title"]]
        e["safe"] = r["safe"]
        e["description"] = r["description"]
        e["exits"] = r["exits"].most_common(1)[0][0].split()
        if len(r["exits"]) > 1:
            e["exits_variants"] = sorted(r["exits"])
        if r["mobs"]:
            e["mobs"] = [m for m, _ in r["mobs"].most_common()]
        if r["objects"]:
            e["objects"] = [o for o, _ in r["objects"].most_common()]
        e["visits"] = r["visits"]
        e["sources"] = [f"logs/raw.log:{r['line']}"]
        e["confidence"] = r["confidence"]
        out_rooms.append(e)

    looks, helps, shops, speech, tips = parse_texts(tr, rooms, ids, players)
    texts, tseen = [], Counter()

    def add(kind: str, title: str, body: str, rooms_: set | None = None, extra: dict | None = None):
        mention = re.compile(r"\b(" + "|".join(map(re.escape, players)) + r")\b", re.I) if players else None
        if mention and mention.search(title):
            return
        if mention:
            body = "\n".join(l for l in body.splitlines() if not mention.search(l))
        base = f"text:{kind}.{slug(title)}"
        tseen[base] += 1
        e = {"id": base if tseen[base] == 1 else f"{base}-{tseen[base]}", "kind": kind, "title": title, "body": body}
        if rooms_ and refs_list(rooms_):
            e["rooms"] = refs_list(rooms_)
        e.update(extra or {})
        e["sources"] = ["logs/transcript.log" if kind != "creation" else "logs/raw.log"]
        e["confidence"] = "confirmed"
        texts.append(e)

    for body in parse_creation(raw):
        add("creation", body.splitlines()[0][:60], body)
    for cmd, body in helps.items():
        add("help", cmd, body)
    for (cmd, body), where in looks.items():
        add("look", cmd, body, where)
    for body, where in shops.items():
        names = [rooms_by_id_title(out_rooms, w) for w in refs_list(where)]
        add("shop-list", " / ".join(dict.fromkeys(n for n in names if n)) or "loja", body, where)
    for who, said in speech.items():
        body = "\n".join(said)
        add("speech", who, body, set().union(*said.values()))
    for t, where in tips.items():
        add("tip", t[5:].strip()[:60], t, where)
    add("remains", "Restos de criaturas (decomposição)", "\n".join(f"{c:>4}x  {t}" for t, c in remains.most_common()))

    yaml.SafeDumper.add_representer(str, lambda d, v: d.represent_scalar(
        "tag:yaml.org,2002:str", v, style="|" if "\n" in v else None))
    header = "# GERADO por db/tools/minerar.py a partir de logs/ — NAO EDITAR A MAO, rode o script de novo.\n"
    dump = lambda xs: header + yaml.safe_dump(xs, allow_unicode=True, sort_keys=False, width=200)
    rooms_txt, texts_txt = dump(out_rooms), dump(texts)
    if SENHA:
        assert SENHA not in rooms_txt and SENHA not in texts_txt, "senha vazou pro YAML"
    (DATA / "rooms.yaml").write_text(rooms_txt)
    (DATA / "texts.yaml").write_text(texts_txt)
    kinds = Counter(t["kind"] for t in texts)
    print(f"{len(out_rooms)} salas, {len(texts)} textos {dict(kinds)}; {len(players)} jogadores ignorados")


def rooms_by_id_title(out_rooms: list[dict], rid: str) -> str | None:
    return next((r["title"] for r in out_rooms if r["id"] == rid), None)


if __name__ == "__main__":
    main()
