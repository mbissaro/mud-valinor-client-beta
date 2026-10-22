#!/usr/bin/env python3
"""Minera logs/raw.log + logs/transcript.log e gera a camada BRUTA da base:

  db/data/rooms.yaml    todas as salas vistas (titulo, descricao real, saidas, mobs, objetos, links observados)
  db/data/texts.yaml    ajudas, descricoes examinadas, falas de NPC, listas de loja, dicas, criacao
  db/data/objects.yaml  itens (inventario, equipamento, lojas, baus, drops, examine) e objetos de cenario

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
    (r"^(À porta da Academia de Aventureiros|Na Estrada do Lago|Acesso à Grande Ponte|Na Grande Ponte de Esgaroth|"
     r"Na Parte Mais Oeste da Ponte|Próximo ao Meio d[ae]|Atravessando o Meio da Ponte|A Vista da Cidade num Trecho|"
     r"Bifurcação da Ponte Superior|Divisão \w+ da Ponte$|Na Extremidade \w+ da Ponte$)", "region:esgaroth.grande-ponte"),
    (r"^(Avenida Perimetral|Esquina das Perimetrais|Praça (Floresta das Trevas|Montanha Solitária|da Flechada Precisa)|"
     r"Avenida Transversal|Alto do Mercado|No Centro de Esgaroth|Rua Oposta|Viela do Herói|Rua de (Cima|Baixo)|"
     r".*Rua dos Caramujos|.*Ponte de Baixo|.*Mercado (Central|Setentrional)|Na Rampa Intermediária|.*Rua das Pulgas|"
     r"No Ancoradouro|Quartel da Guarda)", "region:esgaroth"),
    (r"^(O Amplo Bosque|A Academia de Combate|A Torre Mágica|O Acampamento dos Rangers|A Gruta Profunda|"
     r"A Trilha de Pedras Claras|A Ponte de Pedras Claras|O Pequeno Templo|O Círculo Natural)$", "region:bosque"),
    (r"^(Portão Ocidental|Portão Oriental|Rua da Honra|Praça da Coragem|Cajado Torto - Taverna|Casa de Cura|"
     r"Elmo de Pedra - |Loucura ou Aventura - |O Orc Esfolado - |Bom Patrão - |Estrela da Manhã - )", "region:vila-aventureiros"),
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
                     r"O fígado|As tripas|.*poça de sangue|.* está se decompondo aqui)")
MOB_POS = re.compile(r"(está (em pé|sentad[oa]|dormindo|descansando|deitad[oa])|está aqui, (sentad|lutando|montad)|"
                     r"brilha sob uma aura|está sob uma)")
FAIL = re.compile(r"^(Você não (vê|encontra|consegue)|Não (há|existe|vejo)|Esta pessoa não|Isto não|Hã\?|Huh\?|Este comando não|Você não possui|"
                  r"Você não está|Você não tem|Não foi possível|Ninguém)")
# mensagens assincronas que caem no meio da resposta de um comando (so tiramos as do comeco)
NOISE = re.compile(r"( foi para o | foi para a | voou para | voou d| chegou\.| chegou d| saltitou | partiu)|^(Começa |"
                   r"A noite começa|O sol |A lua |Murmúrios ecoam|Uma paz benfazeja|O dia |Você está com (fome|sede)|"
                   r"Você está MORRENDO|===|Com um encantamento)|ÿ")
LOOKV = {"look", "l", "examine", "exa", "glance", "consider", "con", "read", "ler", "listen", "search", "vasculhar"}
HELPV = {"help", "ajuda", "policy", "book", "news", "commands", "socials", "time", "weather"}
DIRS = {"n": "n", "s": "s", "e": "e", "w": "w", "u": "u", "d": "d", "ne": "ne", "nw": "nw", "se": "se", "sw": "sw",
        "norte": "n", "sul": "s", "leste": "e", "oeste": "w", "cima": "u", "baixo": "d", "north": "n", "south": "s",
        "east": "e", "west": "w", "up": "u", "down": "d", "nordeste": "ne", "noroeste": "nw", "sudeste": "se", "sudoeste": "sw"}

# itens e objetos (transcript.log)
FLAGS = re.compile(r"^(\([^)]*\) )+")  # "(2x) ", "(Brilhando) ", "(atrelado à bela égua) "
STATS = {k: re.compile(v) for k, v in {
    "weight": r"^Isto pesa (.+?)\.$",
    "wear": r"^Isto é usado nas posições: (.+?)\.$",
    "condition": r"^(?:Observando mais atentamente você percebe que i|I)sto está (.+?)\.$",
    "capacity": r"^Capacidade: (.+?)\.$",
    "light": r"^Você nota que isto ainda fornecerá luz por (.+?)\.$"}.items()}
HEALTH = re.compile(r" está (perfeitamente saudável|com alguns arranh|levemente|ferid|gravemente|muito ferid|quase mort|"
                    r"sangrando)| está usando:$", re.M)
ITEM_EVENT = re.compile(r"^(?:Você (pegou|comprou|vestiu|empunhou|colocou|jogou|deu|come|comeu|bebeu|recitou|vendeu)|"
                        r"\S.*? (deu)) (.+)\.$")
EVENT_TAIL = re.compile(r" (?:(?:da|do|de|na|no) (?:mochila|corpo|(?:uma|um|a|o) (?:bela |pesada |pequeno |grande )?"
                        r"(?:estante|armário|baú|caixa)|estante|chão)\b.*|para (?:você|(?:o |a )?[A-ZÀ-Ú].*|(?:o|a) \w+ [A-ZÀ-Ú]\S*)|em (?:seu|sua|seus|suas) \S+(?: \S+)?"
                        r"|no pescoço|sobre sua cabeça)$")
GROUND = re.compile(r"^(.+?) (?:foi (?:abandonad|largad|jogad|arremessad|deixad)|jaz largad|está aqui no chão)")
SHOP_ROW = re.compile(r"^\s*\d+\s+(\d+)\s+(Ilim\.|\d+)\s+(.+?)\s+(\d+)$")
EQ_ROW = re.compile(r"^<([^>]+)>\s+(.+)$")
FOOD = re.compile(r"pão|carne|queijo|salame|bolo|torta|cerveja|rum|uísque|limonada|cogumelo|nozes|azeitona|perdiz|maçã|"
                  r"elixir|especiarias|temperos|iguarias|ervas|cantil")


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


def words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


def hits(kw: str, text: str) -> bool:
    """'look tapecaria' acerta 'tapeçarias': alguma palavra do texto comeca com a palavra-chave (sem acento)."""
    k = "".join(words(kw))
    return bool(k) and any(w.startswith(k) for w in words(text))


def strip_article(s: str) -> str:
    return re.sub(r"^(o|a|os|as|um|uma|uns|umas|alguns|algumas) ", "", s.strip(), flags=re.I)


def lower_first(s: str) -> str:
    return s[:1].lower() + s[1:]


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
                # buffs acabando, acoes sobre voce e cabecalhos soltos nao sao objetos da sala
                if not t.startswith(("Sua ", "Seu ")) and " você" not in t and t.endswith((".", "!", '"')):
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


def tr_lines(tr: str) -> list[str]:
    return [PROMPT.split(l)[-1] if not CMD.match(l) else l for l in tr.splitlines()]


def clean_body(out: list[str]) -> str:
    """Tira do comeco e do fim as mensagens assincronas (falas, clima, chegadas) que cairam na resposta."""
    junk = lambda s: NOISE.search(s) or (SPEECH.match(s.strip()) and "'" in s)
    body = list(out)
    while body and junk(body[0]):
        body.pop(0)
    while body and junk(body[-1]):
        body.pop()
    return "\n".join(body).strip()


def parse_texts(tr: str, rooms: dict, ids: dict, players: set[str]):
    lines = tr_lines(tr)
    idx = room_index(rooms)
    here = None
    where: list[str | None] = []  # sala atual em cada linha do transcript
    edges: Counter = Counter()    # (de, direcao, para) observados ao andar
    start, moved, mv = None, False, None
    looks: dict[tuple, set] = {}
    look_line: dict[tuple, int] = {}  # linha do 1o comando que gerou cada (cmd, texto)
    helps: dict[str, str] = {}
    shops: dict[str, set] = {}
    speech: dict[str, dict[str, set]] = defaultdict(dict)
    tips: dict[str, set] = {}
    cmd, out, closed, cmd_n = None, [], False, 0

    def flush():
        if not cmd or not out:
            return
        p = cmd.split(maxsplit=1)
        v, txt = p[0].lower(), clean_body(out)
        if txt.endswith("\nVocê não vê nada especial."):  # livros: capa + "nada especial" no fim
            txt = txt[:-len("\nVocê não vê nada especial.")]
        # "Você não vê nada especial." seguido de peso/posicao ainda e um examine valido
        if not txt or (FAIL.match(txt) or FAIL.match(txt.splitlines()[-1])) and "\nIsto pesa" not in txt:
            return
        if v in LOOKV and len(p) == 2:
            looks.setdefault((f"{v} {p[1].lower()}", txt), set()).add(here)
            look_line.setdefault((f"{v} {p[1].lower()}", txt), cmd_n)
        elif v in HELPV:
            helps.setdefault(cmd.lower(), txt)
        elif v in ("list", "listar") and "Núm" in txt and len(txt[txt.index("Núm"):].splitlines()) > 1:
            shops.setdefault(txt[txt.index("Núm") - 1 if txt.index("Núm") else 0:].strip("\n"), set()).add(here)

    raw_lines = tr.splitlines()
    for n, l in enumerate(lines):
        m = CMD.match(l)
        if m:
            flush()
            cmd, out, closed, cmd_n = m[2].strip(), [], False, n
            start, moved, mv = here, False, DIRS.get(cmd.lower())
            where.append(here)
            continue
        t = l.strip()
        if t.startswith("Saídas:") and n > 0:
            for key in idx.get(lines[n - 1].strip(), []):
                d = rooms[key]["description"].splitlines()
                if [x.strip() for x in lines[n - len(d):n]] == [x.strip() for x in d]:
                    here = ids[key]
                    # ponytail: 1a sala depois de um comando de direcao = destino; lag do servidor gera
                    # aresta errada as vezes, main() filtra pelas saidas da sala e fica com a maioria
                    if mv and not moved:
                        moved = True
                        if start and here != start:
                            edges[(start, mv, here)] += 1
                    break
        where.append(here)
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
    return looks, look_line, helps, shops, speech, tips, where, edges


# ---------------------------------------------------------------- itens e objetos
def parse_items(lines: list[str], where: list, beings: str) -> dict[str, dict]:
    """Nome de item -> fatos: inventario, equipamento (seu e de NPCs), lojas, conteudo de baus, eventos."""
    items: dict[str, dict] = {}

    def item(name: str) -> dict | None:
        name = re.sub(r" \(\d+\)$", "", FLAGS.sub("", name.strip()).rstrip("."))  # "um caroço de maçã (2)"
        if not name or name in ("Nada", "Alguma coisa") or name.startswith("água") or REMAINS.match(name[:1].upper() + name[1:]):
            return None
        it = items.setdefault(name, {"name": name, "verbs": Counter(), "slots": set(), "worn_by": set(), "shops": {},
                                     "containers": set(), "dropped_by": set(), "rooms": set(), "held": 0, "lines": []})
        it["lines"].append(n)
        return it

    mode, owner = None, ""
    for n, l in enumerate(lines):
        t = l.strip()
        if mode in ("inv", "cont") and l.startswith(" ") and t:
            if (it := item(t)):
                if mode == "inv" or "Halbarion" in owner:
                    it["held"] += 1
                else:  # bau, estante, galho: objeto do mundo
                    it["containers"].add(owner)
                    it["rooms"].add(where[n])
            continue
        if mode == "eq" and (m := EQ_ROW.match(t)):
            if owner == "Você" and (it := item(m[2])):
                it["slots"].add(m[1])
                it["held"] += 1
            elif hits(owner.split()[-1], beings) and (it := item(m[2])):  # so NPC conhecido, nunca jogador
                it["worn_by"].add(f"{owner} <{m[1]}>")
            continue
        if mode == "shop" and (m := SHOP_ROW.match(l)):
            if where[n] and (it := item(m[3])):
                it["shops"][where[n]] = {"room": where[n], "level": int(m[1]), "price": int(m[4]), "stock": m[2]}
            continue
        mode = None
        if t == "Você está carregando:":
            mode = "inv"
        elif (m := re.match(r"^(.+) contém:$", t)):
            mode, owner = "cont", lower_first(m[1])
        elif (m := re.match(r"^(.+) está usando:$", t)):
            mode, owner = "eq", m[1]
        elif t.startswith("Núm") and "Preço" in t:
            mode = "shop"
        elif (m := ITEM_EVENT.match(t)) and (it := item(EVENT_TAIL.sub("", m[3]))):
            it["verbs"][m[1] or "recebeu"] += 1
            it["held"] += m[1] in (None, "pegou", "comprou", "vestiu", "empunhou")
            if (d := re.search(r" do corpo d[eo] (.+)$", m[3])) and "Halbarion" not in d[1]:
                it["dropped_by"].add(d[1])
    return items


def split_examine(body: str) -> tuple[str | None, dict] | None:
    """Separa descricao e linhas de atributo do examine. None se a descricao for lixo de outro comando."""
    ls = body.splitlines()
    first = next(i for i, x in enumerate(ls) if any(p.match(x.strip()) for p in STATS.values()))
    desc = "\n".join(ls[:first]).strip()
    if re.search(r"^\s*[|+]", desc, re.M):
        return None  # pager do mapa caiu na resposta do examine
    stats = {k: m[1] for x in ls[first:] for k, p in STATS.items() if (m := p.match(x.strip()))}
    if "wear" in stats:
        stats["wear"] = stats["wear"].split(", ")
    return (None if not desc or FAIL.match(desc) else desc), stats


def best_item(items: dict, kw: str, body: str, rooms_: set, n: int) -> dict | None:
    """O jogo resolve 'look X' no que voce carrega e depois na sala. Aproximacao: so candidatos que ja estiveram na
    mao ou nesta sala; desempata pelas palavras do nome que aparecem no texto e depois pela mencao mais recente."""
    cands = [it for it in items.values() if hits(kw, it["name"])
             and (it["held"] and it["lines"] and it["lines"][0] < n or it["rooms"] & rooms_)]
    bw = set() if re.search(r"^\s*[|+]", body, re.M) else set(words(body))  # desenho ascii: so recencia vale
    return max(cands, default=None, key=lambda it: (
        len({w for w in words(strip_article(it["name"])) if len(w) > 3} & bw),
        max((l for l in it["lines"] if l < n), default=-1)))


def category(it: dict) -> str:
    n = it["name"].lower()
    if "mapa" in n:
        return "mapa"
    if "livro" in n or n.startswith("o guia"):
        return "livro"
    if "pergaminho" in n:
        return "pergaminho"
    if FOOD.search(n) or it["verbs"].keys() & {"come", "comeu", "bebeu"}:
        return "comida e bebida"
    if it["slots"] or it["worn_by"] or it.get("stats", {}).get("wear"):
        return "equipamento"
    return "outro"


def build_objects(items: dict, looks: dict, look_line: dict, out_rooms: list[dict], npc_words: set[str]):
    by_name = {" ".join(words(k)): it for k, it in items.items()}
    scenery: dict[str, dict] = {}
    # linhas de objeto das salas: item largado no chao ou peca do cenario
    for r in out_rooms:
        for line in r.get("objects", []):
            bare = FLAGS.sub("", line)
            if (g := GROUND.match(bare)):
                key = " ".join(words(g[1]))
                it = by_name.get(key) or items.setdefault(lower_first(g[1]), {
                    "name": lower_first(g[1]), "verbs": Counter(), "slots": set(), "worn_by": set(), "shops": {},
                    "containers": set(), "dropped_by": set(), "rooms": set(), "held": 0, "lines": []})
                by_name[key] = it
                it["ground_line"] = bare
                it["rooms"].add(r["id"])
                continue
            s = scenery.setdefault(bare, {"name": bare, "flags": FLAGS.match(line)[0].strip() if FLAGS.match(line) else None,
                                          "rooms": set(), "descriptions": {}})
            s["rooms"].add(r["id"])

    # so o nome do ser (4 primeiras palavras): "O bibliotecário arruma os livros" nao e o livro
    room_mobs = {r["id"]: " ".join(" ".join(m.split()[:4]) for m in r.get("mobs", [])) for r in out_rooms}
    by_body: dict[str, list] = defaultdict(list)
    for (cmd, body), where in looks.items():
        p = cmd.split()
        if len(p) > 1 and p[0] in ("look", "l", "examine", "exa", "read", "ler") and p[1] != "in":
            by_body[body].append((p[1], {w for w in where if w}, look_line[(cmd, body)]))
    hit_first = {b.splitlines()[0] for b, cs in by_body.items() if any(hits(c[0], b) for c in cs)}
    for body, cands in by_body.items():
        # mesma resposta atribuida a varios comandos (lag): fica com quem tem a palavra-chave no texto
        good = [c for c in cands if hits(c[0], body)]
        if not good and body.splitlines()[0] in hit_first:
            continue  # "look gargulas" recebeu a placa do poste que outro "look poste" ja explica
        for kw, rooms_, n in good or cands:
            if HEALTH.search(body) or "".join(words(kw)) in npc_words or any(hits(kw, room_mobs.get(x, "")) for x in rooms_):
                continue  # olhou um ser vivo
            stats = {}
            if any(STATS["weight"].match(x) for x in body.splitlines()):
                res = split_examine(body)
                if res is None:
                    continue
                desc, stats = res
            else:
                desc = body
            it = best_item(items, kw, body, rooms_, n)
            if it:
                it.setdefault("stats", {}).update(stats)
                it["examined"] = True
                if desc and len(desc) > len(it.get("description") or ""):
                    it["description"] = desc
                continue
            sc = next((s for s in scenery.values() if s["rooms"] & rooms_ and hits(kw, s["name"])), None)
            sc = sc or scenery.setdefault("kw:" + "".join(words(kw)), {"name": kw, "flags": None, "rooms": set(),
                                                                          "descriptions": {}})
            sc["rooms"] |= rooms_
            sc["descriptions"].setdefault(body, set()).update(rooms_)
    return [*items.values()], [*scenery.values()]


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
    return players - npcs - {"Halbarion", "Dorgrin", "Você"}  # nossos personagens


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

    looks, look_line, helps, shops, speech, tips, here_at, edges = parse_texts(tr, rooms, ids, players)
    exits_of = {ids[k]: {x.lstrip("!") for v in r["exits"] for x in v.split()} for k, r in rooms.items()}
    links: dict[str, dict] = defaultdict(dict)
    for (a, d, b), _ in edges.most_common():  # maioria vence; direcao tem que existir nas saidas da sala
        if d in exits_of[a] and d not in links[a]:
            links[a][d] = b

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
        if links.get(ids[key]):
            e["links"] = dict(sorted(links[ids[key]].items()))
        e["visits"] = r["visits"]
        e["sources"] = [f"logs/raw.log:{r['line']}"]
        e["confidence"] = r["confidence"]
        out_rooms.append(e)

    texts, tseen = [], Counter()
    mention = re.compile(r"\b(" + "|".join(map(re.escape, players)) + r")\b", re.I) if players else None
    scrub = lambda s: "\n".join(l for l in s.splitlines() if not mention.search(l)) if mention else s

    def add(kind: str, title: str, body: str, rooms_: set | None = None, extra: dict | None = None):
        if mention and mention.search(title):
            return
        body = scrub(body)
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
    npcs = yaml.safe_load((DATA / "npcs.yaml").read_text())
    npc_words = {w for n in npcs for w in words(n["name"]) if len(w) > 3}
    beings = " ".join([*(m for r in out_rooms for m in r.get("mobs", [])), *(n["name"] for n in npcs)])
    items = parse_items(tr_lines(tr), here_at, beings)
    pages = [b for b in helps.values() if " - Página " in b.splitlines()[0]]
    objects = object_entries(*build_objects(items, looks, look_line, out_rooms, npc_words), scrub, pages)

    rooms_txt, texts_txt, objects_txt = dump(out_rooms), dump(texts), dump(objects)
    if SENHA:
        assert SENHA not in rooms_txt + texts_txt + objects_txt, "senha vazou pro YAML"
    (DATA / "rooms.yaml").write_text(rooms_txt)
    (DATA / "texts.yaml").write_text(texts_txt)
    (DATA / "objects.yaml").write_text(objects_txt)
    kinds = Counter(t["kind"] for t in texts)
    okinds = Counter(o.get("category", o["kind"]) for o in objects)
    print(f"{len(out_rooms)} salas ({sum(len(r.get('links', {})) for r in out_rooms)} links), {len(texts)} textos "
          f"{dict(kinds)}; {len(objects)} objetos {dict(okinds)}; {len(players)} jogadores ignorados")


def object_entries(items: list[dict], scenery: list[dict], scrub, pages: list[str]) -> list[dict]:
    curated = {}
    for c in yaml.safe_load((DATA / "items.yaml").read_text()):
        curated[" ".join(words(strip_article(re.split(r" \(|/", c["name"].split(":", 1)[-1])[0])))] = c["id"]

    def link(name: str) -> str | None:
        k = " ".join(words(strip_article(name)))
        return next((cid for ck, cid in curated.items() if ck in k or (len(k) >= 12 and k in ck)), None)

    out, seen = [], Counter()

    def new_id(base: str) -> str:
        seen[base] += 1
        return base if seen[base] == 1 else f"{base}-{seen[base]}"

    for it in sorted(items, key=lambda x: strip_article(x["name"]).lower()):
        e = {"id": new_id(f"obj:{slug(strip_article(it['name']))}"), "name": it["name"], "kind": "item",
             "category": category(it)}
        if it.get("description"):
            e["description"] = scrub(it["description"])
        e["examined"] = bool(it.get("examined"))
        e.update(it.get("stats", {}))
        for src, dst in (("slots", "worn_at"), ("worn_by", "worn_by"), ("dropped_by", "dropped_by"),
                         ("containers", "found_in")):
            if it[src]:
                e[dst] = sorted(it[src])
        if it["shops"]:
            e["shops"] = sorted(it["shops"].values(), key=lambda x: x["room"])
        if it.get("ground_line"):
            e["ground_line"] = it["ground_line"]
        rooms_ = {x for x in it["rooms"] | it["shops"].keys() if x}
        if rooms_:
            e["rooms"] = sorted(rooms_)
        if it["verbs"]:
            e["actions"] = sorted(it["verbs"])
        if (cid := link(it["name"])):
            e["item"] = cid
        if (t := re.search(r"'(.+)'", it["name"])):  # livro: paginas lidas com BOOK <livro> READ <n>
            ps = [b for b in pages if b.startswith(f"{t[1]} - Página ")]
            if ps:
                e["pages"] = [scrub(b) for b in sorted(ps, key=lambda b: int(re.search(r"Página (\d+)", b)[1]))]
        e["sources"], e["confidence"] = ["logs/transcript.log"], "confirmed"
        out.append(e)
    for sc in sorted(scenery, key=lambda x: strip_article(x["name"]).lower()):
        e = {"id": new_id(f"obj:cenario.{slug(strip_article(sc['name']))}"), "name": sc["name"], "kind": "scenery"}
        if sc["flags"]:
            e["flags"] = sc["flags"]
        if sc["descriptions"]:
            kept: dict[str, set] = {}
            for t, r in sorted(sc["descriptions"].items(), key=lambda kv: -len(kv[0])):
                full = next((k for k in kept if k.startswith(t)), None)  # resposta cortada pelo prompt
                kept.setdefault(full or t, set()).update(r)
            e["descriptions"] = [{"text": scrub(t), "rooms": sorted(r)} for t, r in kept.items()]
        e["examined"] = bool(sc["descriptions"])
        if sc["rooms"]:
            e["rooms"] = sorted(sc["rooms"])
        e["sources"], e["confidence"] = ["logs/raw.log", "logs/transcript.log"], "confirmed"
        out.append(e)
    return out


def rooms_by_id_title(out_rooms: list[dict], rid: str) -> str | None:
    return next((r["title"] for r in out_rooms if r["id"] == rid), None)


if __name__ == "__main__":
    main()
