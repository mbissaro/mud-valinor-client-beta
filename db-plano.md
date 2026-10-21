# Base de dados de worldbuilding: MUD Valinor → referência de design

Spec + plano de implementação gerado por agente planner (Opus 5.5) a partir
de notas.md e catalogo.md. Objetivo: transformar o que foi descoberto no
MUD numa base de dados estruturada, reutilizável como inspiração de design
para outro jogo (não para o MUD em si).

**Fontes lidas:** `notas.md` (1904 linhas, inteiro), `catalogo.md` (inteiro),
`extrair.py` e início de `logs/mapa.md`/`logs/salas.md`.

**Sobre `logs/`:** é dado bruto mesmo. O `mapa.md` usa como chave da sala o
par "título + saídas". Com isso, linhas de chat entram como se fossem salas
(ex.: "(OOC) Fulano disse 'já volto' [w]"). Salas diferentes com o mesmo
título se fundem numa só, como as dezenas de "A Grande Estrada do Leste" e
os dois "Jardins: Ervas Perfumadas". Não existe id de sala (vnum). Serve só
para conferir saídas, nunca como fonte principal.

---

# PARTE 1 — SPEC (modelo de dados)

## 1.1 Princípios

1. **Nomes de campo em inglês, conteúdo em português.** Os campos ficam
   portáveis para qualquer engine. Títulos de sala, nomes de NPC e comandos
   ficam como aparecem no MUD, porque a palavra-chave exata importa
   (`narine`, `guardia`, `servos`).
2. **Ids legíveis e estáveis**, no formato `tipo:regiao.nome`, por exemplo
   `loc:bri.praca`, `npc:narine`, `item:pergaminho-retorno`. Uma referência
   entre entidades é sempre esse texto, nunca um número.
3. **Toda entidade guarda sua procedência e seu grau de certeza.** Isso é
   necessário porque as notas misturam fatos confirmados, palpites
   ("provavelmente", "talvez") e correções posteriores ("CORREÇÃO",
   "Correção: só o Portão NORTE").
4. **Duas camadas em cada entidade:** o que acontece no MUD (fatos) e o que
   serve para o seu jogo (`design`). A segunda camada é a razão de existir
   da base.
5. **Granularidade de "lugar notável", não de cada sala.** As notas não
   registram sala por sala. Trechos repetitivos viram um único `segment`
   com contagem aproximada de salas.

## 1.2 Campos comuns a todas as entidades

```yaml
id: npc:vato-nogueira            # obrigatório, único
name: Vato Nogueira              # nome exato no jogo
keywords: [vato, nogueira]       # o que o parser aceita (útil e frágil)
tags: [transporte, viagem-rapida, tolkien-adaptado]   # vocabulário livre, temático
sources:                         # procedência (obrigatório ter pelo menos 1)
  - "notas.md#DESCOBERTA ENORME: Vato Nogueira — transporte rápido e seguro (charrete)"
  - "catalogo.md#2. NPCs"
confidence: confirmed            # confirmed | inferred | hypothesis | superseded
first_seen: 2026-10-21           # opcional: data ou sessão
notes: ""                        # prosa livre, curta
design:                          # camada de inspiração (opcional, mas é o objetivo)
  patterns: [mech:fast-travel-relocating-driver]
  takeaway: "Viagem paga que elimina o risco, mas o motorista some do ponto de origem e cria um mini-mistério."
  reuse_ideas: []
```

## 1.3 Entidades

### Region (região)
Agrupa locais. Corresponde às seções de Topologia do catálogo.

| campo | tipo | observação |
|---|---|---|
| kind | enum | `city`, `hub`, `road`, `wilderness`, `dungeon`, `quest-area`, `district` |
| parent | ref Region | ex.: Rua do Mercado dentro de Bri; Jardim de Imladris dentro de Valfenda |
| safety | enum | `safe` ("(Seguro)"), `guarded` (vila), `hostile`, `unknown` |
| danger | 0-5 | perigo relativo para personagem de nível baixo |
| level_range | [min,max] | ex.: Mansão Knob [1,10], dito na placa |
| atmosphere | lista | ex.: `[sepulcral, decadente]` (Cemitério), `[contemplativo, atemporal]` (Valfenda) |
| navigation | enum | `grid`, `linear`, `maze`, `one-way`, `wilderness`: Valfenda e o Jardim são `maze`, o Tutorial é `one-way` |
| tolkien_refs | refs LoreRef | |

Regiões já presentes nos dados: Academia (hub), Bri e seus distritos (Rua
do Mercado, Praça das Flores, Rua da Águia/favela, Avenida da Lei),
Biblioteca de Bri, Pônei Saltitante, Colina de Bri/Mina, Amplo Bosque (a
"floresta ao extremo norte"), Formigueiro sob o Portão Sul, Interseção de
Eriador, Velha Estrada Norte, Cemitério, Caminho Verde, Mansão Knob, Archet
(com as 4 torres), Grande Estrada do Leste, Valfenda (Bosquepraça, Jardim
de Imladris, bairro élfico, complexo Museu/Pinacoteca/Biblioteca, Casa de
Reis/Salões de Elrond), Floresta de Pinheiros e o Caminho para as
Montanhas Sombrias (conhecido só de ouvir falar).

### Location (sala ou lugar)

| campo | tipo | observação |
|---|---|---|
| region | ref | |
| kind | enum | `room`, `segment` (N salas genéricas iguais), `building`, `maze-cluster` |
| room_count_estimate | int | só para `segment`, ex.: "dezenas" de salas "A Grande Estrada do Leste" |
| safe_zone | bool | marcador "(Seguro)" |
| status | enum | `explored`, `partial`, `seen-only` (vista de fora ou pela janela), `locked`, `rumored` (conhecida só por GPS, mapa ou mural) |
| light | enum | `lit`, `dark-at-night`, `needs-light` |
| features | lista de objetos | ver abaixo |
| hazards | lista | ex.: `fall-damage` (descer da macieira: -20 HP), `infestation`, `text-warning` |
| summary | texto | 1 a 3 frases, não a descrição completa |
| flavor_quotes | lista | trechos marcantes, ex.: "Nem todo caminho é uma verdade..." |

`features` ganham tipo próprio porque são objetos reutilizáveis que se
repetem pelo mapa:
```yaml
features:
  - type: free-resource        # macieira, fonte
    gives: item:maca
    command: "get maçã macieira"
    limit: unlimited
  - type: board                # mural ou árvore-mural (sistema NOTE)
    era: 2008                  # quadro arquivado vs. ativo
    active: false
  - type: signpost             # poste ou placa com as direções
  - type: heal-bed             # leitos, camas de mallorn
  - type: container            # estante, cesto de lixo
  - type: interactive          # corda dos sinos, jaula
```

### Exit (conexão)
Esta é a entidade que cobre os casos especiais.

| campo | tipo | observação |
|---|---|---|
| from | ref Location | |
| dir | string | `n`, `se`, `u`, `d` ou verbo (`enter jaula`) |
| to | ref Location ou nulo | nulo quando o destino ainda é desconhecido |
| destinations | lista de refs | usado quando o destino varia |
| selection | enum | `fixed` (padrão), `return-to-entry`, `contextual`, `unknown` |
| door | objeto | `{state: closed/locked, opens_with: "open s", key: item:..., night_lock: true, resets: true}` |
| hidden | objeto | `{reveal: ["examine folhagens", "open abertura"], resets_each_visit: true}` |
| one_way | bool | no Tutorial a volta não existe |
| fake | bool | o texto sugere uma saída que não existe ("ergue-se a Academia ao norte" → "Oops") |
| mv_cost | int | ~2 em Bri, ~4 no formigueiro |
| requires | lista | `light`, `gold:10` (cortina do Tantarel), `level`, `alignment:evil` ou `item:cartao-negro` (esgotos de Archet) |

Como os casos especiais ficam:
- **Saída da Academia:** `from: loc:academia.saguao`, `dir: d`,
  `selection: return-to-entry`,
  `destinations: [loc:bri.entrada-academia, loc:archet.entrada-academia, loc:valfenda.entrada-academia]`.
- **Casinha de pedras no Amplo Bosque:** `dir: s`, `selection: contextual`,
  `destinations: [loc:bosque.academia-combate, loc:bosque.gruta-profunda]`.
  Quando houver hipótese sobre o gatilho (aleatório? classe?), ela vai numa
  OpenQuestion ligada a esta saída.
- **Passagem secreta do Portão Sul:** `hidden.reveal` mais
  `resets_each_visit: true` e `requires: [light]` na saída do outro lado.

### Route (rota nomeada)
As notas têm muitas rotas valiosas: rotas dadas pelos GPS, Bri→Archet a
pé, o percurso da charrete. Elas não se reduzem a uma Exit.

| campo | observação |
|---|---|
| from, to | refs Location |
| steps | lista de direções/comandos: `[d, n, w, w, n]` |
| mode | `walk`, `cart`, `teleport` |
| safety | texto do próprio jogo quando houver ("sem perigo algum, até para os mais jovens aventureiros") |
| via | lista ordenada de Locations marcantes (Última Ponte → Vau do Bruinen → ...) |
| given_by | ref NPC (rota informada pelo GPS) |

### NPC

| campo | tipo | observação |
|---|---|---|
| roles | lista enum | `shop`, `buyer`, `gps`, `transport`, `trainer`, `healer`, `repair`, `banker`, `innkeeper`, `guard`, `pet-stable`, `mail`, `lore`, `quest-hook`, `decorative`, `ambient-routine` |
| presence | lista | modelo para NPCs que mudam de lugar, ver abaixo |
| schedule | objeto | `{closed_at_night: true, closed_msg: "voltar amanhã", hours: "8-20"}` |
| hostility | enum | `passive`, `startled-once` (Lady Knob), `hostile`, `unknown` |
| interactions | lista | `{trigger: "say Alimente as galinhas", effect: "Nob sai rumo ao galinheiro", status: works}`, mais as tentativas que falharam |
| gifts | lista | ex.: guardas dão pergaminho de retorno se você "não parece experiente" (condicional, renovável) |
| canon | ref LoreRef | Dori, Lindir, Glorfindel, Nob, Carrapicho→Butterbur, Hary→Harry Goatleaf |

Modelo de `presence`:
```yaml
presence:
  - location: loc:bri.grande-estrada-leste-oeste
    mode: home                      # home | roaming | after-trip | seen-passing | stationary
  - location: null
    mode: after-trip
    rule: "fica algumas horas no destino da última corrida"
```
Lindir aparece como `seen-passing`, o "velho guardião" como `roaming` e
Senhor Knob como `roaming` dentro da mansão.

### Item

| campo | observação |
|---|---|
| category | `food`, `drink-container`, `light`, `scroll`, `weapon`, `armor`, `clothing`, `map`, `book`, `junk`, `trophy-drop`, `tool`, `pet`, `property` (casa) |
| level_req | int |
| effects | `{cures: hunger-critical}`, `{heal: 8, vitality: true}`, `{teleport: loc:academia.saguao}` |
| obtain | lista: `{method: buy\|drop\|harvest\|slice\|gift\|donation\|found, from: ref, cost: 1}` |
| quirks | ex.: o caroço de maçã causa ambiguidade no parser com a maçã; a carne crua exige `cook` |

Livros (Os Poderes de Arda, Cuivienyarna, Dragões, Orcs) são Items `book`
com `pages` e `lore_refs`.

### Trade (oferta ou recusa de compra e venda)
Tabela de junção entre NPC e Item. Resolve de uma vez os preços das lojas,
os itens recusados e os NPCs que aceitam o item sem pagar.

```yaml
- npc: npc:narine
  item: item:mapa-bri
  mode: refuses          # sells | buys | refuses | accepts-unpaid | repairs
  price: null
  level: null
  stock: null            # Zurg: carne de coelho, estoque 1
  side_effect: null      # accepts-unpaid: "alinhamento +25" (Guardiã, Vato)
  observed: 2026-10-21
```
Com isso, a "lista de itens recusados por Narinë" vira uma consulta, e não
um campo duplicado dentro do item.

### Creature (bestiário)
Não estava na lista original, mas os dados têm bastante. Fica separada de
NPC porque os campos são de combate.

| campo | observação |
|---|---|
| regions | refs |
| behavior | `passive`, `aggressive`, `chases-fleeing`, `holds-grudge` (macaco), `group-spawn` (2 a 3 javalis) |
| drops | refs Item; `slice_yields` (bezerro dá carne, raposa não) |
| observations | lista: `{char_level: 2, newbie_buffs: true, consider: "muito mais experiente", hp_lost: 38, xp: 120, verdict: avoid}` |

A observação é relativa ao nível do personagem e aos buffs ativos. O mesmo
javali passa de "melhor alvo" (nível 3, com buffs) para "quase fatal"
(nível 6, sem buffs). Esse contraste é design puro e não pode ser achatado
num número de perigo fixo.

### Mechanic (mecânica e padrão de design)
É o centro da camada de inspiração. Cada mecânica observada é escrita
como um **padrão reutilizável** e lista suas ocorrências no MUD.

| campo | observação |
|---|---|
| category | `survival`, `combat`, `economy`, `travel`, `navigation`, `social`, `progression`, `death`, `time`, `parser`, `meta-system` |
| rules | lista de fatos com números ("fome e sede severas juntas: cerca de -3 HP por tick; cerca de 15 min até morrer"; "carga: 5 itens / 100 kg") |
| stages | para mecânicas em escala: `["com fome", "com muita fome", "MORRENDO DE FOME"]` |
| counterplay | heurísticas aprendidas (as seções "Lição") |
| instances | refs para tudo que exemplifica o padrão |
| design.player_experience | `tension`, `frustration`, `delight`, `discovery` |
| design.verdict | `adopt`, `adapt`, `avoid`, mais o motivo |

Seed já identificado nos dados (cerca de 25):
- Sobrevivência: fome e sede com escala letal; sangramento fora de
  combate; `mv=0` bloqueia a fuga; estado incapacitado sem regeneração.
- Proteção de novato: buffs de novato que expiram (aura azul, resiliência,
  resistência a paralisia).
- Morte: perda de XP, o corpo fica com o equipamento, os Salões de Espera
  com Estë e Námo.
- Inventário: limite de carga, sintaxe `all.<item>`.
- Ciclo do dia: lojas fechadas à noite com horários individuais, portões
  trancados à noite (só alguns), clima regional (neve em Valfenda).
- Navegação: portal contextual, hub compartilhado com retorno à entrada,
  NPC GPS, saídas falsas no texto, escuridão que esconde o texto da sala,
  passagem secreta que se reseta, corredor sem volta.
- Economia: comprador universal a 1 g (Narinë), farm por slice, sala de
  doações entre jogadores, housing de 50000 g com taxa de manutenção.
- Viagem: viagem rápida paga com motorista que muda de lugar, segundo
  condutor com destinos de endgame.
- Social e meta: gatilhos de fala exatos, murais NOTE (arquivados vs.
  ativos), "mobs atalho" como alvos de summon, banco, correio OOC.
- Treino e cura: treino com jaula ou boneco, cura dormindo no leito.

### LoreReference (referência Tolkien)

| campo | observação |
|---|---|
| canon_name | Glorfindel, Last Bridge, Mitheithel, Entwives, mallorn, Prancing Pony, Hall of Fire, Carrock, Weathertop, Tharbad, Butterbur, Harry Goatleaf... |
| work | `LotR`, `Hobbit`, `Silmarillion`, `HoME`, `UT` |
| chapter | opcional ("Muitos Encontros") |
| mud_entities | refs (Location, NPC, Item) |
| fidelity | `exact`, `renamed` (Carrapicho = Butterbur), `adapted`, `invented-in-style` (Família Knob, Uthar Darkbane) |
| how_used | `npc-cameo`, `place`, `book-text`, `flavor-mention`, `travel-landmark` |

### Event (marco ou ocorrência)
Mortes, chegadas ("chegamos a Valfenda"), descobertas estruturais ("a
Academia é um hub único"), correções, bugs (concorrência entre bot e
comandos manuais).

| campo | observação |
|---|---|
| date / session | |
| type | `milestone`, `death`, `discovery`, `correction`, `bug`, `buff-expired` |
| summary | |
| deltas | `{xp: -36752}` |
| refs | entidades envolvidas; `supersedes` para correções |

### OpenQuestion (pendência ou mistério)

| campo | observação |
|---|---|
| question | "Qual o gatilho de canção do bardo Nedhellener?" |
| kind | `trigger-unknown`, `unexplored`, `locked`, `contradiction`, `mechanic-unclear` |
| priority | low / med / high |
| attempts | lista de comandos já tentados (`listen bardo`, `ask bardo about historia`...) |
| status | `open`, `resolved`, `abandoned` |
| resolution / resolved_by | texto e ref de Event |
| refs | |

Pendências já existentes: os triggers do bardo e do menestrel; o gatilho
do portal do bosque; o resto da Mansão Knob; o interior do Cemitério
depois da cerca; a Torre SO e a Torre NO de Archet; a construção de
mármore negro; os esgotos e o cartão negro; a Indumentária e Fundição; os
Aposentos Reais; a Casa-Mathom; a porta Sindarin; o rio do pescador; o
duto de ar do formigueiro; as mansões trancadas de Bri; o puzzle da
Interseção; Dunendel.

Contradições que o ETL precisa registrar como `kind: contradiction`:
- notas.md, linha 68 ("lojista não compra lamparina", "Narinë não aceita
  itens da Academia") contra a linha 96 ("`give lamparina narine` paga 1
  ouro") e contra Narinë aceitando o mapa da Academia.
- Cantil a 15 g na loja e a 16 g no Zurg (os dois podem estar certos).
- Quarto do Carrapicho a "1 moeda" contra a nota de que o preço não foi
  testado.

**Deixado de fora de propósito:** uma entidade para o estado do personagem
Halbarion (nível, atributos). Não tem valor para outro jogo. Quando
importar, fica em `Event.deltas`. Se quiser, adiciona-se depois.

---

# PARTE 2 — PLANO DE IMPLEMENTAÇÃO

## 2.1 Armazenamento recomendado

**A fonte da verdade são arquivos YAML versionados em git. O SQLite é
gerado a partir deles para consulta e nunca é editado à mão.**

| opção | prós | contras | veredito |
|---|---|---|---|
| SQLite como fonte | joins e consultas poderosas | diff ilegível no git; editar prosa em SQL é ruim; difícil de alimentar com Claude | não como fonte |
| JSON | stdlib, sem dependências | sem comentários; prosa multilinha fica feia; ruim de editar à mão | plano B se não quiser dependência |
| **YAML** | legível, prosa multilinha, comentários, diff limpo, fácil para Claude editar | precisa de PyYAML (uma dependência) | **recomendado** |
| Markdown com frontmatter | parecido com o que já é feito | um arquivo por entidade vira centenas de arquivos | exagero para o volume atual |

Layout em `/home/lucas/Desktop/mudvalinor/db/`:
```
db/
  data/
    regions.yaml  locations.yaml  exits.yaml  routes.yaml
    npcs.yaml  items.yaml  trades.yaml  creatures.yaml
    mechanics.yaml  lore.yaml  events.yaml  questions.yaml
    _ingested.yaml      # cabeçalhos de notas.md já processados
  tools/
    build.py            # valida + gera valinor.sqlite + exports
  valinor.sqlite         # gerado, no .gitignore
```
Um arquivo por tipo e não por região. São cerca de 12 arquivos, e uma sala
que muda de região não obriga a mover nada. `locations.yaml` deve ficar
entre 1500 e 2500 linhas, o que é aceitável.

Volume estimado depois da migração: cerca de 150 a 200 locations, 300
exits, 70 NPCs, 60 items, 120 trades, 15 creatures, 25 mechanics, 40 lore
refs, 20 events e 30 open questions.

## 2.2 Fases (cada uma entrega valor sozinha)

### Fase 0 — Preparação (decisões e segurança)
1. **`git init` em `/home/lucas/Desktop/mudvalinor`** (ou só em `db/`, ver
   decisão D3). Hoje a pasta não é um repositório git.
2. **Criar o `.gitignore` antes do primeiro commit**, com `.credenciais`,
   `logs/`, `.mud_*`, `*.swp` e `db/valinor.sqlite`. Risco alto:
   `.credenciais` tem a senha, e `logs/raw.log` e `logs/transcript.log`
   podem ter o login gravado.

### Fase 1 — Esquema e validador (mínimo viável)
3. **`db/tools/build.py`, modo `validate`**, com cerca de 150 linhas:
   - carrega todos os YAML;
   - verifica os campos obrigatórios por tipo (um dict em Python, sem
     biblioteca de schema);
   - verifica ids únicos;
   - verifica se toda ref `tipo:id` existe;
   - verifica se os valores de enum são válidos;
   - verifica se toda entidade tem pelo menos uma `source`.
   - Não usar jsonschema nem pydantic: um dict de regras basta para uma
     pessoa só.
   - Risco: baixo.
4. **Teste de verificação:** `db/tools/test_build.py` com um fixture de 3
   entidades, contendo uma ref quebrada e um id duplicado, e assert de que
   o validador acusa os dois. Um único teste com pytest ou um `__main__`
   com assert.

### Fase 2 — Migração dos dados atuais (ETL único, feito com Claude, não com regex)
A prosa de `notas.md` não dá para converter com regex de forma confiável.
Os mapas em ASCII também não. Só as tabelas do catálogo seriam
mecanizáveis, e mesmo elas são pequenas demais para justificar um parser.
Recomendação: **extração por LLM seção a seção, revisada no `git diff`.**

5. **Semente pelo `catalogo.md`**, por ser a fonte mais estruturada:
   Topologia → Region, Location, Exit; tabelas de NPCs → NPC; Itens →
   Item e Trade (incluindo a lista de recusas); Mecânicas → Mechanic. Um
   commit.
6. **Varredura do `notas.md` em lotes de cerca de 10 seções** (as ~125
   seções viram cerca de 13 lotes):
   - completar as entidades e adicionar Creature, Event, OpenQuestion,
     LoreRef e as camadas `design`;
   - marcar `confidence` (palavras como "provavelmente" e "talvez" viram
     `hypothesis`);
   - registrar contradições como OpenQuestion;
   - aplicar as correções (o fato antigo fica `superseded`, ligado a um
     Event `correction`);
   - registrar cada cabeçalho processado em `_ingested.yaml`;
   - validar e fazer commit a cada lote.
7. **(Opcional) Conferência das saídas contra `logs/mapa.md`**, filtrando
   títulos `(OOC)` e linhas de fala, para achar saídas que as notas não
   mencionam. Só gera sugestões, nunca escreve direto nos YAML, porque
   títulos repetidos se fundem.
   - Risco: médio, por alucinação na extração. A mitigação é `sources`
     obrigatório mais a revisão do diff.

### Fase 3 — Consulta
8. **`build.py`, modo `sqlite`:** gera `valinor.sqlite` com uma tabela por
   tipo, os campos-lista em colunas JSON e duas tabelas de junção
   explícitas (`refs(from_id, to_id, field)` e `tags(id, tag)`). Usa
   `sqlite3` da stdlib.
9. **Visualizador:** Datasette (`pip install datasette`, depois
   `datasette db/valinor.sqlite`). Dá uma interface web com filtros por
   faceta, busca e SQL sem escrever nenhum frontend. Exemplos de consulta:
   - itens que Narinë recusa: `trades WHERE npc='npc:narine' AND mode='refuses'`;
   - todas as instâncias do padrão "NPC GPS";
   - locais `safe_zone` com macieira e fonte;
   - todas as referências de LotR com fidelidade `exact`;
   - pendências abertas com prioridade alta.
   - Para consultas rápidas sem nada instalado: `sqlite3 db/valinor.sqlite`
     ou grep nos YAML.

### Fase 4 — Exports (só quando o outro jogo pedir)
10. **`build.py export --json`:** um único `valinor.json` portável, que
    qualquer engine (Godot, Unity, web, Ink) consome.
11. **`build.py export --dot <região>`:** grafo Graphviz das Locations e
    Exits por região, com saídas contextuais tracejadas e saídas sem volta
    com seta simples.
12. **(Decisão D6) `build.py export --catalogo`:** regera o `catalogo.md`
    a partir da base, para acabar com a manutenção tripla.

Não incluídos agora: busca full-text, embeddings, frontend próprio e API.
Valem a pena quando o Datasette deixar de bastar.

## 2.3 Fluxo de captura contínua

O `notas.md` continua sendo escrito exatamente como hoje (append-only, com
cabeçalhos `##`). A base é atualizada num **passo de ingestão ao final de
cada sessão**:

1. `python db/tools/build.py pending` lista os cabeçalhos `##` de
   `notas.md` que não estão em `_ingested.yaml`. O cabeçalho serve de
   chave; o validador avisa se houver cabeçalho duplicado.
2. Pedir ao Claude: "ingere as seções pendentes no db/". Ele edita os
   YAML e acrescenta os cabeçalhos ao `_ingested.yaml`.
3. `build.py validate` precisa passar.
4. Revisar o `git diff` e fazer o commit (`data: ingest sessão AAAA-MM-DD`).
5. Se quiser, `build.py sqlite` antes de consultar.

Por que não escrever direto no YAML durante o jogo: dá mais atrito no
meio da sessão, e o `notas.md` continua sendo o registro de *por quê*, que
a base só referencia. O custo é um passo a mais no fim da sessão, cerca de
5 minutos.

## 2.4 Testes
- **Unitário:** o teste de fixture do validador (passo 4). Precisa falhar
  se as checagens de ref, id ou enum quebrarem.
- **Integração:** num commit, `build.py validate && build.py sqlite` roda
  sobre os dados reais, com assert de que a contagem de linhas no SQLite
  bate com a contagem de entidades nos YAML.
- Não há E2E nem testes visuais, porque não existe interface própria.

## 2.5 Riscos e mitigações

| risco | severidade | mitigação |
|---|---|---|
| `.credenciais` ou logs com senha entrando no git | **crítica** | `.gitignore` antes do primeiro commit (passo 2); conferir com `git status` |
| Extração por LLM inventando fatos | alta | `sources` obrigatório; `confidence`; revisão lote a lote no diff |
| Palpites registrados como fatos | média | enum `confidence`; contradições viram OpenQuestion em vez de serem "resolvidas" no chute |
| Manter três cópias (notas, catálogo, db) que divergem | média | decisão D6: gerar o catálogo a partir da base |
| Títulos de sala repetidos | média | o id é distinto do `name`; trechos repetitivos viram `segment` |
| Perigo "absoluto" enganoso | média | o perigo da criatura fica em `observations` com nível e buffs, não num número fixo |
| Esquema mudando com dados novos | baixa | `notes` livre; enums ampliáveis; o validador só exige o mínimo |
| `logs/` usado como fonte | baixa | só como sugestão (passo 7), nunca escrito direto |

## 2.6 Decisões a confirmar antes de implementar

- **D1 — YAML ou JSON.** YAML exige `pip install pyyaml`. JSON tem zero
  dependências e é mais feio de editar. Recomendado: YAML.
- **D2 — Idioma.** Campos em inglês e conteúdo em português (recomendado)?
  Ou tudo em português? Um `name_en` para os nomes canônicos?
- **D3 — Onde fica o git.** Repositório na pasta `mudvalinor` inteira (com
  `.gitignore` agressivo) ou repositório separado só para `db/`? O
  separado é mais seguro em relação às credenciais.
- **D4 — Granularidade.** "Lugares notáveis mais `segment`" (recomendado)
  ou tentar uma entrada por sala, usando os logs?
- **D5 — Quem faz o ETL.** Claude em lotes com revisão (recomendado), ou
  preenchimento à mão?
- **D6 — Destino do `catalogo.md`.** Passa a ser gerado pela base
  (recomendado), continua manual ou é aposentado?
- **D7 — Datasette.** Pode instalar? A alternativa é usar só o `sqlite3`
  na linha de comando.
- **D8 — Camada `design`.** O Claude rascunha `takeaway`, `verdict` e
  `reuse_ideas` durante a ingestão para revisão posterior, ou o campo
  fica vazio pra preencher à mão? O rascunho acelera, mas mistura opinião
  com fato — nesse caso marcar `confidence: inferred`.
- **D9 — Bestiário e números de combate.** Manter no nível de detalhe
  atual (observações por nível) ou só "perigo, comportamento e drops"?

## 2.7 Critérios de sucesso
- [ ] `build.py validate` passa sobre os dados migrados, sem refs quebradas.
- [ ] Todo cabeçalho atual de `notas.md` está em `_ingested.yaml`.
- [ ] É possível consultar no SQLite ou no Datasette: as recusas de
  Narinë, todas as saídas `contextual` e `return-to-entry`, as instâncias
  de cada Mechanic, as OpenQuestions abertas e as LoreRefs `exact`.
- [ ] Uma sessão nova vai do `notas.md` à base em um único passo
  `pending` → ingestão → `validate` → commit.
- [ ] `.credenciais` e `logs/` nunca aparecem no `git log`.
