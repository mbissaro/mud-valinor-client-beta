# Notas — MUD Valinor (Halbarion, Humano Guerreiro, Bri)

## Estado (2026-10-21)
Nível 3, 19.576/32.400 XP, 6 ouro, 7 práticas guardadas. Vida máx 55, mana 100, mov 220, CA 3, hitroll 4, damroll 3.
Atributos: For 17, Int 14, Des 14, Sab 15, Con 12, Car 14. Alinhamento +11. Nenhuma morte.
Carga: 1/5 itens, 44/100 kg. Inventário não conferido (antes: 2 pergaminhos de retorno, 4 elixires).
Próximo passo: caçar coelhos (hp cheio) e levar ao Zurg por ouro; comprar Ataque Aprimorado (Domick, 100 ouro).
No nível 3 o bestiário abaixo (feito no nível 2) deve estar mais fácil; reavaliar com consider.

## Básico
- Servidor latin1: entrada precisa ir em latin1 (mud.sh converte).
- Modo Aural ligado: prompt `<hp m mv>`.
- XP por nível: 2=1.200, 3=9.600, 4=32.400, 5=76.800, 6=150.000.
- Perícias custam 100 ouro + 1 prática. Ataque Aprimorado: Domick (Sala de Treino de Perícias). Chutar: mestre da classe no Amplo Bosque.
- Config: autogold, autoloot ligados; wimpy 6.

## Academia de Aventureiros (zona segura)
- Saguão: W armaduras grátis (estante), E armas grátis + reparo (Phrantes), N corredor, D saída.
- Corredor 1: W perícias (Domick), E magias. Corredor 2: W loja, E idiomas. Corredor 3: W cura (Mestre Toric: dormir nos leitos cura e dá Bênção+Armadura, hp vai a 30), E refeitório. N jardim (Narinë compra qualquer item por 1 moeda) -> portão N -> Amplo Bosque.
- Elmo metálico exige nível 2 (na mochila).

## Mapa da Academia (térreo, eixo norte-sul)
```
            [Amplo Bosque]
                 | n (portão !n, abrir)
 [Narinë]   Centro do Jardim
                 |
 Cura (W) -- Corredor 3 -- (E) Refeitório
                 |
 Loja (W) -- Corredor 2 -- (E) Idiomas
                 |
 Perícias(W)- Corredor 1 -- (E) Magias
                 |
 Armaduras(W)- Saguão -- (E) Armas/reparo
               u: 2º andar (Dodô, tutorial, biblioteca)   d: saída da Academia
```
Loja (lvl): protetor de ferro p/ braços 3 ouro (lvl2), espada longa 8, colchonete 10, pergaminho de retorno 1, lamparina 2, manoplas de ferro 3 (lvl7), armadura cristada 5 (lvl6).

## Amplo Bosque (nível 1)
- Entrada (N do jardim): saídas n e s w. A oeste: sala com n e w (coelhos frequentes). A leste há mata densa no limite.
- O "felino ágil" é descrito como espião desajeitado e fedorento (orc disfarçado?).
- Pássaro azul: fácil, 15 xp.
- Coelho veloz: PERIGOSO no nível 1 (bate ~4/rodada, 2x por rodada), fugi 2 vezes.
- Macaco, felino ágil, filhote de urso: "muito mais experientes" — evitar.
- Vespa enorme, cobra gigantesca: vistas a oeste, não testadas.
- Floresta ao extremo norte: só nível 4–5.
- Pergaminho de retorno leva ao saguão da Academia.

## Bestiário do Bosque (visto no nível 2)
| Monstro | consider (nível 2) | Resultado |
|---|---|---|
| Pássaro azul | um pouco mais experiente, páreo | Seguro. ~10 hp perdidos, 8–53 xp. Pode deixar asa decepada. |
| Raposa preguiçosa | mais experiente, párea | Bom alvo: ~17 hp perdidos, ~120 xp. Cabeça pode ser arrancada. |
| Cobra gigantesca | mais experiente, párea | PERIGOSA: até 6 hp por rodada; me levou a 4 hp. |
| Coelho veloz | mais experiente, páreo | PERIGOSO no nível 1: dois golpes por rodada, persegue quem foge. |
| Javali gordão | (nível 3) mais experiente, páreo | MELHOR ALVO no nível 3: 732 xp, custa ~35 hp (55 -> 20). Só com hp cheio. |
| Grande macaco | muito mais experiente, páreo | PERIGOSO no nível 2: me levou de 42 a 4 hp. "Muito mais experiente" = evitar. |
| Felino ágil | muito mais experiente, um pouco mais forte | Evitar. Descrição sugere espião disfarçado. |
| Filhote de urso | muito mais experiente, um pouco mais forte | Evitar. |
| Vespa enorme | — | Vista a oeste, parece agressiva. |

## Lições
- O wimpy foge, mas um burst pode tirar 6+ hp depois: usar wimpy alto (10) e recitar retorno logo após fugir.
- Mestre Toric cura enquanto você dorme nos leitos (`sleep leitos`) e dá Bênção, Armadura e Vitalidade (hp acima do máximo).
- Monstros do bosque não deixam ouro. Ouro só do orc da jaula (5) até agora; lojista compra itens.
- O servidor só reconhece acentos em latin1 ("tapeçaria"); sem acento não acha.
- Fonte de ouro: Zurg (refeitório, E do corredor 3) paga por coelhos caçados no bosque (`say caca`). `say comida` dá carne grátis.
- Narinë NÃO aceita corpos nem itens da Academia. `sacrifice corpo` não dá ouro. Lojista não compra lamparina nem elixir.
- Elixir colorido: cura ~8 hp + vitalidade (usar no meio da luta).
- Macaco atacado guarda rancor: persegue e ataca depois.
- Lutar só com hp cheio (raposa tira até 37 hp se começar com 32).
- Dormir nos leitos e ficar parado muito tempo derruba a conexão por inatividade ("O mundo ao seu redor se desfaz..."). A cura completa leva menos de 1 minuto: acordar (wake) logo depois.
- Ao relogar, o personagem volta na sala onde caiu (Sala de Cura).
- Pendente: juntar 100 de ouro para Ataque Aprimorado (Domick) e Chutar (mestre da classe no bosque).
- Nível 3: vespa enorme e coelho veloz viraram fáceis (coelho ~100 xp, tira ~25 hp). Zurg paga só 3 ouro por coelho (`give corpo zurg`).
- Depois de `wake` o personagem fica sentado: usar `stand` antes de andar.
- A porta do jardim (sul da entrada do bosque) fecha sozinha: `open s` antes de voltar.
- Caminho bosque -> cura: open s, s, s, s (corredor 3), w. Não descer mais um s (vai pra loja).
- Lobo sorrateiro aparece no bosque, não testado.


## Lição crítica: morte (nível 6, sessão longa)
- 2 javalis simultâneos derrubaram hp de 3 para -2 a -6 em sequência rápida; elixir/pergaminho não
  dão tempo de reagir quando já está "entorpecido demais" (inconsciente).Sangramento continua
  enquanto inconsciente, mesmo sem novos ataques.
- Morte: XP caiu ~25.000 (199.770 -> 174.885). Nível não caiu. Equipamento e ouro ficam no corpo
  no ponto de retorno (aqui, a Academia) — não se perdem, mas o corpo decompõe com o tempo.
- Ao morrer: vai para "Os Salões de Espera" (Estë dá um manto temporário + bênção). Precisa esperar
  Námo/Vairë julgarem (minutos) antes de ser teleportado de volta ao ponto de retorno.
- `get all corpo` para tudo de uma vez trava em "não pode carregar tantos objetos" (limite 5
  itens/mão). Alternar `get all corpo` com `wear`/`wield` de cada item até vaziar o corpo.
- O bosque ao norte da Academia (zona "floresta ao extremo norte") é efetivamente uma wilderness:
  "Ao X, ergue-se a grande Academia" é só visual (sem saída real nessa direção); só o texto
  "escadaria... porta da academia" marca a entrada real, que fica cercada de salas comuns.
  Perder-se lá facilmente consome o pergaminho de retorno; manter 3+ sempre.
- Fonte de ouro sem caçar: `give lamparina narine` (jardim) paga ~1 ouro por lamparina, mesmo após
  o Zurg parar de dar comida de graça no nível mais alto.


## Lição CRÍTICA: fome/sede severas MATAM (2ª morte, nível 6)
- Fome e sede severas ao mesmo tempo causam sangramento ("Você apenas deseja que seus ferimentos
  parem de sangrar tanto!") mesmo FORA de combate, perdendo ~3hp por tick. Em ~15 minutos sem
  comida/água isso mata (chegou a -hp e morreu de novo, dessa vez sem luta nenhuma).
- `rest`/`sleep` sozinho NÃO impede essa sangria; só comer e beber param.
- Sem cantil (vendemos o nosso!) e sem gruta/academia por perto, fica impossível saciar sede —
  NUNCA andar sem cantil de aventureiro (15 ouro na loja) e sem comida reserva.
- Aprendido com Zurg (grátis, `practice 'fatiar carne'` e `practice cozinhar`): perícias `slice`
  (precisa empunhar arma de corte) e `cook` — permitem virar corpo de bicho caçado em comida,
  sem depender de comprar pão. Fonte de água existe na Sala de Cura e no saguão da Academia
  (`drink fonte`), mas só lá — fora disso só com cantil enchido antes de saír.
- Noite ("A noite começa") deixa o bosque "Está escuro" SEM nenhum texto de sala (nem a dica da
  escadaria aparece) — navegação por leitura de texto não funciona de noite sem lamparina
  sobressalente. Portas fechadas ("Está fechado") ainda são perceptíveis no escuro e levam a
  prédios iluminados (Gruta Profunda, Torre Mágica, Academia de Combate, Acampamento dos
  Rangers) — todos dentro do mesmo bosque "floresta ao extremo norte", a maioria sem saída útil
  de volta (voltam pro mesmo lugar).
- SEMPRE manter: 1+ lamparina sobressalente, 1 cantil cheio, 2+ comidas, 2+ pergaminhos de
  retorno antes de qualquer caçada longa. Sem isso, qualquer imprevisto (fuga pra wilderness,
  anoitecer) pode encadear fome+sede+escuridão até morte sem nenhum combate.

## Lição: wilderness perigosa e bug de concorrência bot+manual (nível 6, sessão longa)

- A floresta ao norte da Academia pode ficar MUITO infestada: salas com 2-3
  javalis gordões + lobos sorrateiros simultâneos foram comuns numa sessão.
  Javali gordão ATACA ativamente (não é passivo) e pode machucar bastante em
  sequência; sem pergaminho de retorno e sem elixir, isso é arriscado mesmo
  com HP alto. `flee` funciona bem pra escapar (muda de sala), mas pode cair
  de novo em sala cheia de bichos.
- NUNCA rode bot.py em background e mande comandos manuais via mud.sh ao
  mesmo tempo: os dois escrevem no mesmo pipe/conexão do personagem e os
  outputs se misturam. Isso já causou um bug real: o bot pensou que
  `recite pergaminho` tinha funcionado (achou a palavra "Academia" no
  buffer) só porque um `look` meu concorrente trouxe essa palavra, e seguiu
  a lógica de "cheguei em casa" sem ter chegado. Sempre `pkill -f bot.py`
  antes de qualquer intervenção manual, e só relançar depois de confirmar
  estado real com `look`.
- `slice corpo` funciona em corpo de bezerro, raposa e coelho, não só
  javali. Mas cada corpo só rende 1 fatia de carne (depois disso: "Esta não
  é uma fonte adequada de carne"). `cook` pode queimar a carne (perícia
  nova, chance de falha) mas carne queimada ainda é comível via `eat`.
- Fome evolui: "com fome" → "com muita fome" → "MORRENDO DE FOME" (drena
  movimento rapidamente nesse último estágio). Resolver companheira (comer)
  antes de chegar no estágio crítico evita o risco de sangramento visto na
  lição anterior.
- Bot.py recebeu um fallback (`buscar_entrada()`): quando cai em local
  desconhecido, tenta andar sozinho até achar entrada/oeste/leste real
  (checando saídas sem diagonal) antes de depender do pergaminho. Ajuda,
  mas não é garantido (pode esgotar as 20 tentativas numa wilderness muito
  grande) — intervenção manual ainda pode ser necessária.

## Lição: ciclo de emergência contra fome severa (rápido e seguro)

Caçar+slice+cook pra comida é lento e arriscado (filhote de urso sozinho
tirou Halbarion de 84 pra 14hp numa luta, nível 6) — não é bom plano pra
resolver fome crítica em cima da hora. Ciclo muito mais rápido e seguro,
sem saída da Academia:
1. `get <qualquer item sem uso> mochila` (ex: O Guia do Aventureiro)
2. Levar até Narinë (Centro do Jardim) e `give <item> narine` → ela paga
   1 moeda por "qualquer coisa", mesmo itens que não são junk óbvio.
3. Ir até a Loja (corredor principal, 2 salas ao sul do corredor
   cura/refeitório, porta oeste) e `buy pao` (1 moeda) → `eat pao`.
Isso resolve fome crítica em ~6 comandos, todos dentro da Academia
(zona segura), sem nunca precisar sair pro bosque. Prioridade sobre
caçar comida quando a fome já está em "MORRENDO DE FOME".

## Exploração: Academia de Aventureiros, partes nunca vistas

Mapa textual (item "mapa da Academia de Aventureiros", achado no 2º andar):
corredor central norte-sul no térreo liga, de sul pra norte: saguão de
entrada (loja a leste da entrada externa, salas de treino a oeste) →
refeitório (e) / sala de estudos [sic, idiomas?] (w) → sala de estudo de
idiomas (e) / treinamento de perícias (w, e a oeste desta treinamento de
magias) → depósito de armas (e) / depósito de armaduras (w) → Sala de Cura
→ 3 salas de combate (n/e/w da cura).

Saguão de entrada (térreo): tem escadas `u` (2º andar) e `d` (saída da
Academia). Depósito de Armas (e do saguão): Phrantes, cuteleiro, repara
itens com `repair <item>`. Depósito de Armaduras (w do saguão): costureira
ajusta roupas. Sala de Treino de Magias (corredor, perto do treino de
perícias): mago Herenvardo.

2º andar ("Corredor Silencioso", acessado por `u` do saguão): tem uma
2ª "Sala de idiomas" (e) e porta "Tutorial Inicial" (w) — um corredor de
salas de tutorial com orbes brilhantes que re-ensinam comandos básicos
(cada orbe dá um texto de ajuda ao `examine orbe`, e cada sala tem um
professor PNJ): Sala da Observação → Movimentação → Ajuda → Objetos →
Contêiners → Comunicação → Auto-Conhecimento (orbe é um espelho aqui) →
Preparação (tem escada `u` pra mais um andar, não explorado ainda). Um
"mapa da Academia de Aventureiros" largado no chão do Corredor Silencioso
foi pego — dá a descrição textual do prédio ao `look mapa`.

Sala de treino de combate (Leste e Oeste do Jardim): boneco de palha +
magos que oferecem treino seguro dizendo `desejo lutar` — não testado
ainda, mas parece prática de combate sem risco real de morte.

16 pontos de prática (`practice` sem argumento lista tudo) ainda não
usados — Fatiar Carne só 27%, Cozinhar só 19%, vale investir pontos aí
pra reduzir as falhas vistas nesta sessão.

## Exploração: Tutorial Inicial (2º andar) é corredor ONE-WAY, cuidado com fome

O "Tutorial Inicial" (porta w do Corredor Silencioso, 2º andar) é um
corredor de salas de orbe SEM saída de volta pelo caminho de entrada —
a Sala da Observação só tem saída `n`, nunca `s`/`e` de volta. Isso quase
causou fome crítica (MORRENDO DE FOME, sangrando) presa lá dentro sem
rota de escape rápida. Única forma de saída é completar o corredor até o
fim. Sequência completa (entrando por w do Corredor Silencioso):
Observação -n-> Movimentação -e-> Ajuda -e-> Objetos -s-> Contêiners -s->
Comunicação -w-> Auto-Conhecimento (orbe é um espelho) -w-> Preparação -u->
Sala das Portas (duas portas TRANCADAS; chave metálica está numa estante
na própria sala, `get chave estante` + `unlock <dir> chave`) -n-> Sala da
Atenção (tapeçaria norte esconde passagem, `examine tapeçaria` + `open
tapeçaria`) -n-> Sala do Combate (tem uma JAULA pra treino, `enter jaula`
— não testado ainda, mas zona "(Seguro)" como todo o tutorial) -e-> Sala
das Habilidades (tem um PERGAMINHO no lugar do orbe, não lido ainda) -e->
Fim do Treinamento -e-> volta pro Corredor Silencioso (2º andar).
Logo: se entrar no tutorial com fome subindo, já contar com ~12 comandos
pra sair pelo fim, não pela entrada.

## Lição CRÍTICA: 3ª morte — "Incapacitado" NÃO regenera HP sozinho

Terceira morte do personagem (nível 6, XP 223504 → 186752, perda de
36752; nível preservado; equipamento 100% recuperável no corpo, mesmo
processo de sempre: `get all corpo` + `wear`/`wield` intercalado por
limite de 5 itens).

Causa: combate contra múltiplos javalis gordões numa wilderness
anormalmente infestada (vários dias/sessões já mostraram isso, mas nesta
sessão especificamente o bosque teve grupos de 2-3 javalis convergindo
repetidamente) + fome em estágio "MORRENDO DE FOME" simultânea (sangramento
duplo: dano de combate E fome ao mesmo tempo). HP foi de 84 a -4 em poucos
comandos mesmo fugindo ativamente a cada ataque.

**O ponto crítico**: ao cair para HP muito negativo, o personagem entra no
estado "Posição: Incapacitado" (confirmado via `score`). Nesse estado:
- NÃO pode se mover, lutar, nem usar a maioria dos comandos.
- HP NÃO regenera sozinho (testado: hp parado em -4 por 45+ segundos
  reais sem nenhuma mudança, nem para pior nem para melhor).
- A perícia `Socorrer`/`Resgatar` (vista na lista de `practice`) existe
  provavelmente para OUTRO jogador reanimar alguém incapacitado — sozinho,
  não há nada a fazer além de esperar a morte ou um milagre de
  resgate/cura de área que não aconteceu aqui.
- Eventualmente morreu por conta própria (sangramento incapacitado ou
  fome), sem mais nenhum golpe de monstro.

**Regra prática daqui pra frente**: HP abaixo de ~25-30% MAIS fome em
estágio "muita fome" ou peor é combinação de ALTO RISCO DE MORTE real,
não só "perigoso". Nessas condições, priorizar fugir pra zona segura
(mesmo arriscando mais dano na fuga) é melhor do que ficar parado
"resting" esperando regenerar, porque regen natural sem bênção é lento
(pode levar 20-40s reais pra subir 10-15hp) e a fome continua drenando
durante esse tempo. Se cair incapacitado sozinho, não há recuperação:
é esperar a morte.

## Lição: Movimento (mv) em 0 BLOQUEIA fuga — regra de margem mínima

`flee` falha com "Você está cansado demais para fugir!" quando mv=0.
Cada golpe/esquiva em combate consome mv, então uma luta longa pode
zerar mv mesmo com HP ainda ok, te travando sem opção de escapar se o
combate virar. Regra: ao ver mv cair abaixo de ~20-25 durante uma luta,
tratar como alerta igual a HP baixo — terminar a luta atual rápido e
voltar pra curar antes de engajar outro bicho, nunca deixar mv chegar a 0
no meio do bosque.

## Exploração: fora da Academia — Vila de Bri e Biblioteca

A Academia tem uma saída real pro mundo: do Saguão, `d` leva a "Entrada
para a Academia" (saídas `n`/`u`), e `n` daí leva à "Estrada Horizonte" —
a primeira rua de verdade da vila de Bri. Um guarda ali avisa: "seu lugar
é na Academia... tente não sair da vila de Bri ou encontrará perigos!"
— ou seja, a vila de Bri é uma zona mais segura que o mundo aberto, mas
ainda fora do grupo "(Seguro)" da Academia.

Mapa da vila de Bri (do item "mapa da vila de Bri", pego no 2º andar):
grid de ruas com Casa de Cura, Sede McD, Galinheiro, Biblioteca, Praça
de Bri, Pônei Saltitante (provável taverna), Estábulos, Açougue, Padaria,
Lacticínios, Correios, Penas e Pergaminhos, Loja Esmeralda, Ferreiro,
Armorial, Loja de Armas, Tenda do Escriba, Loja de Chás, Loja de
Utilidades, Sede Grn, Mansão Abandonada, Loja do Annir, Casa Bill, Loja
de Animais — tudo conectado à Academia pela Estrada Horizonte.

Postes nas ruas têm `look poste` com as 4 direções descritas em texto —
útil pra navegar sem se perder (ex.: da Estrada Horizonte perto da
Academia: norte=Biblioteca, leste=Rua da Águia, oeste=Avenida Zênite/
Estrada do Falcão/Praça de Bri).

Biblioteca de Bri (norte da Estrada Horizonte): saguão de entrada (sala
do copista a leste, sala reservada com mural a oeste) → antecâmara
(balcão com escadas leste/oeste) → Nave Principal → Ala Leste tem uma
estante com o livro "Os Poderes de Arda" (3 páginas, lore de Tolkien:
Ainur/Valar/Maiar, a Era das Lâmpadas, a fundação de Valinor/Valimar em
Aman) — `get livro estante`, `book livro read <página>`.

Um jogador (aparentemente nigromante/druida visitado
em forma espectral translúcida na Sala de Cura) lançou vários buffs
generosos no personagem sem ser pedido (bênção, resistência a paralisia,
armadura mágica) e trocou algumas falas — bom exemplo de roleplay/
interação social espontânea no MUD.

## DESCOBERTA IMPORTANTE: guarda dá pergaminho de retorno de graça

Na Estrada Horizonte (fora da Academia, perto da Biblioteca), um guarda
avisou Halbarion que não parecia experiente o bastante pra estar ali e
DEU DE GRAÇA um pergaminho de retorno, dizendo pra recitá-lo e depois
`look` no "Guardião do Norte" se ficar perdido. Isso resolve o problema
recorrente desta sessão (múltiplas quase-mortes e uma morte real por
falta de scroll). Vale ir até essa rua e falar com guardas sempre que
precisar reabastecer scrolls de emergência, antes de gastar ouro na
loja. Recitar mantém o personagem seguro — não gastar esse scroll
sem necessidade real.

## Exploração: O Pônei Saltitante (taverna/estalagem) — rico em referências Tolkien

Vila de Bri, sul da Praça (via Grande Estrada Leste): a estalagem "O
Pônei Saltitante" (referência direta a "The Prancing Pony" de Bri, no
Senhor dos Anéis). Estrutura: Pátio (n=hospedaria, s=estábulo) →
Entrada da Hospedaria (Sr. Carrapicho, estalajadeiro — equivalente a
Barliman Butterbur; aluga quarto por 1 moeda; diz que ao norte dá pra
comer e beber) → Taverna (Nob — o criado hobbit do livro — vende comida/
bebida via `list`/`buy`: nozes 1g, queijo 2g, salame 2g, cerveja 3g,
cogumelos 3g, bolo de chocolate 3g, rum 3g, cerveja grande 4g, uísque 4g,
limonada 6g, torta de cereja 7g — tudo preço baixo mas ainda precisa de
ouro, que o personagem não tinha no momento).

NPCs notáveis na taverna: **Dori**, um dos doze anões companheiros de
Thorin Escudo de Carvalho (irmão de Ori e Nori) — totalmente equipado em
tema (insígnia da Montanha Solitária, malha de couro e anéis, braçadeiras
"das trevas de Angband", cinto de ouro e prata) — NPC histórico rico,
não apenas decorativo. Um "carteador"/homem tranquilo jogando cartas
(lembra o disfarce de capuz marrom de Passolargo/Aragorn na taverna
original do livro, embora não nomeado como tal). Um bardo chamado
**Nedhellener**, tocando banjo, com texto de flavor sugerindo que daria
pra puxar conversa dele por uma história/canção — tentativas de `say`/
`ask bardo about historia` não deram resposta; provavelmente precisa de
sintaxe ou condição específica não descoberta ainda.

A Grande Estrada Leste (ao sul da Praça de Bri) tem uma casa-depósito
genérica a oeste e a entrada do Pônei Saltitante a leste; clima dinâmico
observado ("Começou a chover") independente do ciclo dia/noite.

## DESCOBERTA ENORME: macieira grátis na Avenida Zênite resolve fome pra sempre

Na Avenida Zênite (norte da Praça de Bri, fora da Academia), há uma
macieira: `get maca macieira` colhe uma maçã grátis, ilimitadamente
(testado, funcionou sem custo). `eat maca` resolve "com fome"/"muita
fome"/"morrendo de fome" instantaneamente, sem precisar caçar bicho,
usar `slice` (que falha a maioria das vezes) nem ter ouro pra pão. Isso
resolve o problema mais recorrente e perigoso de toda a sessão — sempre
que a fome apertar, ir até esse ponto em vez de caçar coelho/raposa no
bosque perigoso.

Rota da Academia até a macieira: do Saguão, `d` → Entrada da Academia,
`n` → Estrada Horizonte (tem o guarda que dá pergaminho de retorno
grátis), `w`, `w` → Praça de Bri, `n` → Avenida Zênite (macieira +
Guardião do Norte, o NPC mencionado pelo guarda pra usar após recitar o
scroll perdido).

Essa mesma Avenida Zênite tem o "Guardião do Norte" (NPC-chave do
protocolo de resgate do guarda: recitar o pergaminho de retorno e depois
`look` nele) e um "obscuro homem do norte" (outro NPC, não investigado).

## Guardião do Norte (Avenida Zênite): NPC "GPS" de ajuda/navegação

`look`/`say preciso de ajuda` pro Guardião do Norte dá informações
valiosas e sempre atualizadas:
- Rota de volta: da Avenida Zênite, ir à Praça de Bri (sul), depois 3x
  leste, Academia fica ao sul de lá.
- Comida grátis/comprável: Rua do Mercado (2x sul da Praça, depois leste
  na parte norte da rua) tem Açougue, Padaria e Laticínios.
- Pra qualquer outra ajuda, direciona pro guarda do Portão Norte (poucos
  metros ao norte da Avenida Zênite) — `look` nele quando achar.
Esse NPC funciona como um "GPS" built-in da vila — vale consultá-lo
sempre que perdido ou precisando de recursos, antes de vagar sem rumo.

## Mundo maior: guarda do Portão Norte lista todos os destinos conhecidos

`say preciso de ajuda` pro guarda do Portão Norte (fora da vila) revela
a lista completa de locais nomeados que ele sabe indicar: A Praça de
Bri, Academia de Aventureiros, **Archet**, **Valfenda** (= Imladris =
Rivendell, confirmado por ele — "vá pela Grande Estrada do Leste,
contornando pelo sul de Bri, é uma estrada muito longa... se avistar um
elfo ou passar por um Urzal, chegou lá"), A Grande Estrada do Leste,
Animais de Estimação, Armorial, Biblioteca de Bri, Casa-Mathom, Correio,
Ervas e Cachimbos, Loja de Armamentos, Loja de Roupas, Oficina do
Ferreiro, Penas e Papéis, Pônei Saltitante, Seção de Alimentos,
Utilidades. Basta dizer o nome do local pra ele (`say <nome>`) pra
receber a rota.

Fora do Portão Norte já não é mais zona "(Seguro)" — é "perigos" segundo
o próprio guarda. Viajar até Archet/Valfenda é uma jornada longa,
provavelmente arriscada demais pra nível 6 sem conhecer o caminho — vale
nível/equipamento melhor antes de tentar.

## Pergaminhos de retorno são RENOVÁVEIS de graça pelos guardas

Confirmado: toda vez que o personagem passa por um guarda da vila (visto
no Portão Norte, dentro e fora), se ele achar que o personagem "não
parece experiente o bastante", ele dá um pergaminho de retorno de graça
de novo. Ou seja, antes de qualquer expedição arriscada, vale passar
pelos guardas dos portões pra garantir estoque de scrolls de emergência
sem gastar ouro nenhum — resolve de vez a crise de "sem pergaminho" que
dominou boa parte desta sessão.


## Lição: lojas fecham de madrugada (horário do jogo)
Testado as 3h (horário do servidor IC) em várias lojas da Rua do Mercado:
Açougue, Padaria e Armorial todas responderam "Desculpe-me, mas você
poderia voltar mais tarde?" ao tentar `list`. Não é bug nem recusa
específica — é ciclo dia/noite afetando comércio. Horário do jogo
visível via comando `time`. Próximo reboot automático do servidor:
22/10/2026 06:00:00. Voltar a essas lojas de dia (ou esperar o relógio
avançar) para efetivamente comprar/vender.


## Exploração: Rua do Mercado completa + Oficina do Ferreiro
Rua do Mercado tem 2 interseções (leste e oeste), poste em cada uma.
- Interseção leste: n=Açougue, s=oficina de reparo (ferreiro, ver abaixo), e=Grande Estrada Leste, w=continua Rua do Mercado.
- Interseção oeste: n=Padaria, s=Armorial, w=Rua do Mercado->Avenida Zênite/Estrada do Falcão, e=volta.
Oficina do Ferreiro: NPC "o ferreiro" não vende (`list`->"Você não pode
fazer isto aqui."), só repara: comando `repair <item>` (igual Phrantes
na Academia). Forja deixa sede.


## DESCOBERTA: Portão Sul de Bri + guarda-GPS funciona em qualquer portão
Portão Sul fica em: Praça de Bri -> Grande Estrada Leste (s,s) -> cruzamento
com Avenida da Lei -> s = Dentro do Portão Sul (saídas n s sw).
Guarda de QUALQUER portão (Norte ou Sul) responde `say <nome do lugar>`
com rota detalhada a partir da Praça de Bri. Rotas coletadas:

- Correio: Praça -> s,s (cruzamento Rua do Mercado) -> 2º estabelecimento
  a oeste, lado sul da Rua do Mercado.
- Ervas e Cachimbos: DUAS lojas separadas.
  - Ervas: norte da Praça, 1º estabelecimento a leste da Avenida Zênite.
  - Cachimbos: leste da Praça, na Estrada Horizonte, 1ª construção ao
    norte (casa velha na encosta da colina).
- Loja de Armamentos (Sr. Tuneloso): Praça -> s,s -> última loja a leste
  do cruzamento, lado sul da Rua do Mercado.
- Loja de Roupas (Alfaiataria do Annir): Praça -> Avenida da Lei s,s,s,s
  (cruzamento) -> oeste,oeste -> loja ao norte.
- Penas e Papéis: Praça -> s,s (cruzamento Rua do Mercado) -> 1º
  estabelecimento a oeste, lado sul da Rua do Mercado.
- Utilidades (frascos/bolsas/tochas/lamparinas/chás/pergaminhos):
  Praça -> s,s (cruzamento) -> estabelecimentos a oeste do cruzamento,
  lado NORTE da Rua do Mercado.
- Seção de Alimentos (vários, alimentos em geral): Praça -> s,s
  (cruzamento) -> estabelecimentos a LESTE do cruzamento, lado norte da
  Rua do Mercado (Açougue/Padaria ficam aqui).
- Animais de Estimação (Mascotes e Montarias): Praça -> Avenida da Lei
  s,s,s,s (cruzamento) -> leste,leste,leste -> loja ao norte.
- Casa-Mathom: da Praça de Bri, fica a sul e oeste (objetos doados).

Ainda sem rota detalhada pedida: Oficina do Ferreiro (já visitada,
ver seção da Rua do Mercado), Armorial (já visitada), Loja de Roupas
já coletada acima.


## DESCOBERTA: passagem secreta em "Fora do Portão Sul"
Em "Fora do Portão Sul" (Dentro do Portão Sul -> s), a descrição avisa
"folhagens... estranhamente reviradas merecem investigação". Sequência:
`examine folhagens` -> revela abertura escondida -> `open abertura` ->
nova saída `d` aparece -> leva a área ESCURA (sem luz: "Está escuro...",
não dá pra ver nada/arriscado). Precisa de fonte de luz (tocha/lamparina,
vendida em Utilidades) antes de explorar essa passagem a fundo. Voltou
pra cima (`u`) sem entrar na escuridão. Pendente: comprar tocha e voltar.


## Exploração: Loja de Utilidades, Penas e Papéis, Correio
- Loja de Utilidades: norte da interseção oeste-oeste da Rua do Mercado
  (além de Padaria/Armorial, mais uma interseção pra oeste). Fechada de
  madrugada (mesmo padrão).
- Penas e Papéis: sul dessa mesma interseção (onde fica o "especialista
  em pergaminhos"). Tem porta oeste ligando direto ao Correio.
- Correio de Bri: sala "(Seguro)". Sistema de correio é OOC (fora de
  personagem), funciona em qualquer lugar do MUD via `HELP MAIL` —
  não é elemento de roleplay IC, é utilidade de comunicação entre
  jogadores. Tem NPC "curioso passarinho azul" e um carteiro
  decorativos. Nota: "Você ainda não tem um armário" (provavelmente
  precisa de comando específico pra obter caixa de correio pessoal,
  não investigado a fundo pois é sistema OOC).


## Exploração: Rua do Mercado lado leste (Loja de Armamentos, Laticínios)
Nova interseção da Rua do Mercado (mais a leste, perto da Rua da Águia):
norte = Loja de Laticínios (NPC "Siulin", jovem garota), sul = Loja de
Armamentos (NPC "Senhor Tuneloso", vendedor de armas). Ambas também
fechadas mesmo após "Começa um novo dia" — lojas têm horário de
abertura próprio, não abrem instantaneamente ao virar o dia. NPC nomeado
itinerante "Kheodred, o herói das guerras" caminha por essa rua; `say`/
`ask` sobre guerras não gerou resposta (provavelmente decorativo, só
`look`/`examine` tem texto rico).


## Exploração: Rua da Águia (fronteira leste de Bri)
Interseção da Rua do Mercado com Rua da Águia (cerca-viva ao leste =
limite da vila). Rua da Águia completa (norte a partir daí):
1. trecho norte 1: só flavor (pássaros atrás da cerca-viva).
2. Interseção com Estrada Horizonte (Colina de Bri ao leste bloqueia
   passagem; Estrada Horizonte segue oeste de volta à Academia).
3. trecho norte 2: Colina de Bri ao leste.
4. Setor pobre/favela: "mais pobre e abandonado", farrapos e lixo,
   barraca de mendigo (decorativa, sem obj. interativo) às bordas
   da Colina.
5. trecho com matagal abandonado a oeste, Colina a leste.
6. Encontro com a Estrada da Justiça (fim dela) — NPC "cão abandonado"
   dormindo. Daqui a Estrada da Justiça segue oeste, ligando-se à
   Avenida Zênite / Cruzamento do Portão Norte (já mapeado antes).
Isso fecha o perímetro leste/norte da vila. Ainda falta explorar a
Rua da Águia ao SUL da interseção com a Rua do Mercado.


## Exploração: Rua da Águia sul + perímetro completo de Bri mapeado
Rua da Águia ao sul da interseção com Rua do Mercado: trecho bonito
(pinheiros, jardins, 2 bancos de pedra) -> "Encontro da Rua da Águia
com a Avenida da Lei" = canto SUDESTE de Bri (cerca-viva ao sul e
leste). Com isso o perímetro de Bri está todo conectado:
Portão Norte -> Avenida Zênite -> Estrada da Justiça -> Rua da Águia
(fronteira leste, com setor pobre/favela) -> Rua do Mercado -> Grande
Estrada Leste -> Avenida da Lei -> Portão Sul -> canto SE -> de volta
pra Avenida da Lei rumo oeste.


## Exploração: Mascotes e Montarias (loja ABERTA)
Avenida da Lei (muro sul de Bri) -> norte = "Mascotes e Montarias"
(NPC "peão de estábulo"). Esta loja estava ABERTA mesmo de madrugada —
talvez não siga o mesmo horário comercial das lojas de rua. `list`
mostra tabela Nível/Animal/Preço:
  19  a bela égua         95
  25  o cavalo de guerra  125
  6   o gato              30
  16  o falcão real       80
  9   o cão de caça       45
  7   a mula              35
  20  um crocodilo        100
No nível 6 atual já dá pra comprar "o gato" (30 gold) quando tivermos
dinheiro. Útil lembrar para quando juntarmos gold.


## Exploração: Avenida da Lei (muro sul) completa
Partindo do cruzamento Grande Estrada Leste/Avenida da Lei (perto do
Portão Sul) rumo oeste: estátua de "Uthar Darkbane" com placa dourada
("Descanse em paz, Uthar Darkbane") -> ruínas decorativas ao norte
(sem acesso) -> casa trancada ao norte ("!n" saída, "Está fechado" —
possível side-quest com chave não encontrada ainda) -> Alfaiataria do
Annir ao norte (NPC "Annir, o alfaiate" — fechada na hora testada) ->
continua oeste até a Avenida Zênite / Estrada do Falcão (fronteira
oeste de Bri, ainda a explorar).


## PONTOS DE INTERESSE PENDENTES (trancados, possível quest futura)
- "Uma Mansão Abandonada": ao norte na Avenida da Lei (poste: "Norte-
  Uma Mansão Abandonada"), guardada por "duas gárgulas de pedra...
  olhos vermelhos que parecem brilhar levemente". Saída marcada "!n"
  (fechada). `n` -> "Está fechado." Visual de dungeon/side-quest.
- Casa descuidada (também na Avenida da Lei, mais a leste): saída
  "!n", também "Está fechado."
Ambas precisam provavelmente de chave/quest específica, não tentado
arrombar ainda. Nível atual (6) pode ser baixo demais para essa área.


## Exploração: canto sudoeste de Bri — "mestre dos ladrões"
"Encontro da Estrada do Falcão com a Avenida da Lei" = canto SW de
Bri (cerca-viva oeste+sul). NPC "o mestre dos ladrões... para mostrar
as maneiras de se roubar" presente (provável trainer de perícia
Roubar/furtar, relevante pra classe Ladino — Halbarion é Guerreiro,
não testado se pode treinar). `look mestre`/`look ladrao` não
reconheceram o nome (sintaxe exata ainda não descoberta).


## Exploração: Portão Oeste de Bri
"Dentro do Portão Oeste" (saídas e/w/nw), guardado por NPC nomeado
"Hary Barba-de-Bode" / "Hary, o porteiro" (referência a Harry
Goatleaf, personagem de Bree em O Senhor dos Anéis). Mesmo serviço
de rota por nome de lugar (`say preciso de ajuda` -> `say <lugar>`)
que os outros guardas. NÃO deu pergaminho de retorno grátis (talvez
esse bônus só vem de guardas comuns/patrulha, não de porteiros
nomeados — não confirmado). NPC "Adalgrim" (nome hobbit de Tolkien)
visto passando por aqui, sentido oeste->norte.


## DESCOBERTA: saída oeste de Bri leva à Interseção de Eriador (lore real de Bree!)
Portão Oeste -> w (Fora do Portão Oeste, NPC "senhor bem vestido" no
alto do muro organizando defesas, inacessível) -> w (Sobre Um
Passadiço, fosso) -> w (trilha ao longo do fosso) -> w (A Interseção):
cruzamento das três estradas históricas de Eriador — Grande Estrada do
Leste (oeste daqui), Velha Estrada Norte (norte), Caminho Verde (sul).
Tem uma "pedra grande e branca" com inscrição em westron quase
ilegível: "Nem todo caminho é uma verdade, há estradas falsas e
verdadeiras até seu tesouro. É uma encruzilhada. Boa sorte!" — hint de
puzzle/side-quest de navegação (nem toda estrada leva aonde parece).
NÃO explorado ainda pra além desse ponto (fome subiu pra estágio 2,
"Você está com fome", decidiu voltar pra Bri comer antes de se
arriscar mais longe). Pelo guarda do Portão Norte: Grande Estrada do
Leste leva a Valfenda (contornando pelo sul de Bri, estrada muito
longa). Não confirmado ainda qual estrada leva a Archet.


## Lição: CUIDADO ao subir (`u`) na macieira da Avenida Zênite
A sala da macieira tem saída `u` -> "No Alto da Macieira" (vista bonita
da Praça de Bri, pássaros). Mas descer de novo (mesmo após a sala dizer
"o tronco... fornece uma descida segura") resultou em QUEDA real:
"Você está caindo... OUCH! Você caiu no chão!" com perda de HP de 80
para 60 (20 de dano). Não vale a pena subir só por curiosidade — não
há recompensa clara lá em cima (só flavor text), e o risco de queda ao
descer é real. Evitar repetir sem necessidade.


## Exploração: Comércio de Ervas (NPC "Mat Urzal")
Avenida Zênite, norte da macieira -> e = "Comércio de Ervas", casa de
hobbit "Mat Urzal" que vende fumo/ervas em caixinhas organizadas por
plaquinha. Loja fechada no horário testado (mesmo após o sol já ter
nascido - lojas parecem ter horários específicos de abertura, não só
"dia vs. noite").


## Exploração: Praça das Flores + bairro residencial (leste da Avenida Zênite)
Avenida Zênite (trecho norte, antes do cruzamento c/ Estrada da
Justiça) -> e = "Na Praça das Flores": pequena praça com fonte de
pedra (`drink fonte` funciona, cura sede) e bancos, cercada de
canteiros floridos. É a entrada do bairro residencial "mais pacato"
de Bri (sem lojas/estalagens). Poste local lista:
  N = Rua das Cerejeiras, E = Rua das Rosas, S = Rua dos Trevos
  (que por sua vez dá acesso a Rua das Samambaias, Rua das Orquídeas,
  Rua das Macieiras), O = volta à Avenida Zênite.
Também tem "!ne" (pequeno mercadinho a sudeste da praça, trancado) e
"!se" (casa de dois andares a nordeste, de alguém abastado, trancada).
Rua das Cerejeiras (testada): ruela ladeada de casas grandes/abastadas
com cerejeiras, portões norte/sul pras casas individuais — bairro
residencial de luxo, não explorado casa por casa (provavelmente
residências privadas/trancadas, baixo valor de exploração por
comando gasto).


## Exploração: Casa-Mathom (referência real a Tolkien)
Grande Estrada Leste (trecho sul, perto do Pônei Saltitante) -> w =
"A Casa-Mathom": depósito caótico de objetos "para possível uso
futuro" construído pelos hobbits de Bri. Referência direta ao
"mathom-house" de Michel Delving no livro (O Senhor dos Anéis). Texto
sugere "se tiver paciência para procurar" encontrar algo útil, mas
`search`, `procurar`, `look chao` não funcionaram — sintaxe exata não
descoberta (pendente).


## Exploração: Colina de Bri / Caminho Arborizado (nordeste/leste da Praça)
Praça de Bri -> ne = "Um Caminho Arborizado" (trilha rumo à colina),
andando ne/e repetidas vezes sobe a colina (2ª macieira encontrada no
meio do caminho) até "Uma Bifurcação no Caminho" com placa de madeira
grande listando:
  Norte = Mina Abandonada (cuidado!)
  Sudoeste = A Praça de Bri
  Leste = A Colina
- Leste -> "A Colina": caminho estreito que termina em "Diante de uma
  Colina Íngreme" (beco sem saída decorativo, sem escalada possível).
- Norte -> "A Entrada da Mina Abandonada": túnel vedado por pedras e
  madeira pelos guardas de Bri por segurança (minério insuficiente,
  abandonada) — SEM acesso real, só saída `s` de volta. Sem perigo
  real presente apesar do aviso "cuidado!" na placa (aviso é só sobre
  o motivo histórico do veto, não sobre monstros).


## Exploração: galinheiro de Nob (Grande Estrada Leste, oeste da Praça)
Praça de Bri -> w = Grande Estrada Leste, galinheiro ao norte (`!n`,
trancado) pertencente a Nob (o mesmo NPC da Taverna do Pônei
Saltitante). Aviso na porta: manter porta fechada p/ não fugirem as
galinhas, e dizer `say Alimente as galinhas` a Nob caso faltem milho
pras galinhas — pequena interação de roleplay/quest ambiente (não
testada ainda, requer ir até Nob na taverna).


## DESCOBERTA ENORME: Vato Nogueira — transporte rápido e seguro (charrete)
Grande Estrada Leste (oeste da Praça de Bri, perto da trilha de pedras
que sobe a colina): NPC nomeado "Vato Nogueira", sentado numa bela
égua, com charrete montada. Oferece viagem rápida para: VALFENDA
(Rivendell/Imladris), ARCHET, BRI, ESTRADO, FOSSO BRANCO.
Uso: `say como viajar?` -> ele explica: "Apenas acomode-se sobre a
charrete, entregue-me cinco moedas e peça seu destino." Custa 5 gold.
`HELP VATO NOGUEIRA` tem mais detalhes (não lido ainda).
ISSO RESOLVE o problema de viajar até Valfenda/Archet com segurança,
sem arriscar a longa e perigosa Grande Estrada do Leste a pé. Só
precisa juntar 5 gold (ainda não temos nenhum gold). Prioridade:
juntar 5+ gold (vender itens a Narinë por 1 gold cada, ou outra
fonte) para poder usar esse transporte quando quisermos ir a Valfenda.


## Roleplay: mendigo na Estrada do Falcão
"decrépito e velho mendigo" sentado na Estrada do Falcão (trecho norte,
perto do Portão Oeste), implorando esmola ("Uma esmola, pelo amor dos
deuses!"). Trajado com trapos que "um dia foram roupas de um nobre" —
hint de lore (nobre caído em desgraça). Ainda sem gold pra testar
`give <moeda> mendigo`.


## DESCOBERTA ENORME: chegamos em Archet a pé (seguro, sem Vato Nogueira)
Rota completa a pé desde Bri (toda SEGURA, sem perigo encontrado, nível
6): Portão Norte de Bri -> n (Sobre um Passadiço) -> n (Ao Redor de
Bri) -> nw (Uma Trilha ao Norte de Bri) -> nw (Uma Trilha ao Norte de
Bri, 2ª sala) -> nw (Uma Trilha Perto de Bri, ramal p/ colina ao
norte não explorado) -> nw (A Velha Estrada Norte, rumo Fornost nas
Colinas do Norte — trilha leste leva a "lugar desolado" não
explorado) -> n (Velha Estrada Norte 2) -> ne (trilha pra Archet) ->
ne ("Uma Estrada Muito Utilizada" x3, uma delas tem ramal leste/sw) ->
n (A Entrada de Archet).
Jogo confirma explicitamente nessa rota: "o caminho parece bastante
frequentado e não oferece perigo algum, até mesmo para os mais jovens
aventureiros" — ou seja, SEGURO pra qualquer nível ir a Archet a pé,
sem precisar do Vato Nogueira/5 gold.

Em "A Entrada de Archet": arco de pedra, muralhas semi-destruídas,
estrada calçada ao norte. NPC "Kylara" (aura branca) dá boas-vindas
calorosas e avisa: "os esgotos e os subterrâneos são perigosos para
quem não é do mal ou não tem um cartão negro" — sugere área de
esgotos/subterrâneos em Archet reservada para personagens malignos ou
com item especial "cartão negro" (não relevante pra Halbarion,
Guerreiro comum). Saídas daqui: n e s w — vila de Archet ainda a
explorar.


## Exploração: Archet, Rua dos Ofícios + Casa Bancária
"(Seguro) Rua dos Ofícios" é o centro de Archet: fonte, bancos de
pedra, NPC "Umaro, líder da guarda de Archet" (sem resposta a
`say preciso de ajuda`). Ao norte, grande construção comercial
movimentada (porta trancada "!n", não visitada ainda).
Leste: outra Rua dos Ofícios com Casa Bancária (sul) e Sala da Guarda
(norte, ainda não visitada). Casa Bancária: NPC "Vognus, o banqueiro"
cumprimenta pelo nome ("Olá Halbarion"). Sistema real de banco via
comando `BANK` (ver `HELP BANK`): `bank balance` confirma saldo 0
("Não há nenhum depósito em seu nome"). Útil quando tivermos gold —
guardar dinheiro em segurança (com taxa) em vez de carregar.


## Exploração: Archet, Torre Sudeste / "Os Saguões de Inverno" (abandonado)
Rua dos Ofícios (extremidade leste) -> n = "A Torre Sudeste": antiga
torre de muralha, interior virou restaurante. NPC decorativo "Nauk"
(anão perdido, lendo o Guia do Aventureiro). Entrando (`se`): "Os
Saguões de Inverno" — restaurante outrora movimentado, hoje
abandonado ("hoje isso não vai além de lembranças"), sem NPCs/comida
disponível. Mais pra dentro (`se` de novo): antiga cozinha virada
depósito caótico de objetos jogados sem organização (beco sem saída,
só `nw` de volta). Lore de declínio da cidade, sem interação de
gameplay encontrada.


## Exploração: Archet, Rua das Batalhas + "Os Saguões de Outono" (bar ativo)
Da Torre Sudeste, seguindo pela Rua das Batalhas (distrito de armas/
armaduras de Archet, todas as lojas vistas "!e" trancadas: loja de
armaduras, loja de armas, forjaria) até "A Torre Nordeste": virou um
BAR ativo. Entrando (`ne`): "Os Saguões de Outono" — bar funcionando,
garçonete servindo. `list` mostra menu (todos nível 0, qualquer nível
pode comprar):
  pão duro com carne desfiada - 4 gold
  caneca de cerveja - 4 gold
  fatia de salame - 2 gold
  porção de azeitonas - 1 gold
  rodela de queijo - 2 gold
Ainda sem gold pra comprar, mas é opção MUITO barata (1 gold a
azeitona) pra quando tivermos dinheiro — mais barato que o pão da Loja
de Bri.


## Exploração: Archet, Rua das Distrações + Hospedaria Sono Cerrado
Oeste da Torre Nordeste: "Rua das Distrações" (área de jogos de azar
e bebidas, barracas inacessíveis, "construção de mármore negro"
trancada com guardiões visíveis pelas janelas — provável
guild/instituição poderosa, não identificada). Ao norte dessa rua:
"Hospedaria Sono Cerrado" — NPC "Tantarel", hospedeiro ("Olá
forasteiro! ... Talvez queira descansar..."). Quadro de avisos: diária
custa 10 gold, dá direito a quarto com água/comida/cama enquanto
quiser ficar (entregar a chave na saída). Encontrada cortina
escondendo passagem ao norte (não explorada ainda).

Confirmado: tentar passar da cortina ao norte sem pagar os 10 gold
resulta em Tantarel puxar o personagem de volta ("você vai precisar
alugar um quarto para poder entrar ali"). Pendente até termos gold.


## Mapa das 4 Torres de Archet (muralha reaproveitada)
Archet tem 4 torres antigas da muralha, cada uma reaproveitada:
- Torre Sudeste: restaurante abandonado ("Os Saguões de Inverno").
- Torre Nordeste: bar ativo ("Os Saguões de Outono").
- Torre Noroeste: "mais lojas" (entrada "!nw" trancada, aroma de
  flores vindo de dentro, não visitada por dentro).
- Torre Sudoeste: ainda não visitada.
Rua das Distrações (oeste) -> tem a própria "Academia de Aventureiros"
de Archet ao sul (onde "jovens aventureiros aprendem suas lições
básicas" — equivalente da Academia de Bri, mas em Archet).


## DESCOBERTA ESTRUTURAL IMPORTANTE: a Academia de Aventureiros é um HUB ÚNICO
Entrando pela "Academia de Aventureiros" vista em Archet (Rua das
Distrações -> s -> "Entrada para a Academia" -> u), chega-se ao
MESMÍSSIMO saguão de entrada já conhecido de Bri (descrição idêntica:
fonte de mármore, quadro com planta na parede norte, depósito de
armaduras a oeste, depósito de armas a leste, diretora presente,
escadas ao sul pro 2º andar/saída). Ou seja, a Academia NÃO pertence
exclusivamente a Bri — é uma zona neutra/hub com múltiplas entradas
(ao menos Bri e Archet), o que explica por que o "Ponto de retorno"
do personagem é só "Academia de Aventureiros" sem especificar cidade.
Pergaminho de retorno provavelmente leva sempre a esse mesmo saguão
único, independente de onde for recitado.

Confirmado por teste: a saída do saguão (`d` -> "Entrada para a
Academia" -> `n`) leva de volta pro MESMO lugar de onde você entrou
(nesse caso, Archet), não necessariamente pra Bri. O sistema parece
"lembrar" o portal de entrada por sessão/instância de personagem —
mecânica tipo portal contextual, não uma saída fixa única.


## Archet: pendências de exploração
Não visitadas ainda: Torre Sudoeste (4ª torre do anel), interior da
loja da Torre Noroeste ("!nw" trancada), interior da "construção de
mármore negro" (Rua das Distrações, "!n" trancada, guardiões visíveis
pelas janelas), extremo sul/oeste da Rua dos Ofícios original (perto
da Entrada de Archet), Sala da Guarda (trancada), esgotos/subterrâneos
(avisados como perigosos, exigem "cartão negro"/alinhamento maligno).
Arquivo de navegação ficou confuso dentro do anel das 4 torres — se
retornar, usar o poste/placa ao invés de tentar memorizar direções.


## Exploração: Biblioteca dos Aventureiros (2º andar da Academia, diferente da Biblioteca de Bri)
Corredor Silencioso (2º andar) -> mais ao norte -> porta leste "Biblioteca
dos Aventureiros" (sala "(Seguro)"): estantes de livros, mesas com
poltronas, mural de avisos/postagem (sistema tipo fórum/board OOC,
não referenciado a tópicos específicos). `look estante` não achou
objeto (decorativo). Mapa pego do chão no Corredor Silencioso: "um
mapa da Academia de Aventureiros" (vendível a Narinë por 1 gold).


## Exploração: Sala dos Professores + Sistema de Quest por Profecias (histórico)
2º andar da Academia, mais ao norte do Corredor Silencioso: "Sala dos
Professores" (tapete, quadros de professores antigos, lareira,
NENHUM NPC presente) e, na mesma área, portas "Diretoria" (porta
dourada) e uma 3ª porta sem placa — ambas SEM acesso real (`n`/`w`
deram "Oops. Por ali não..." mesmo existindo visualmente na
descrição, só decorativas/bloqueadas).
Na Sala dos Professores há um mural de notas com sistema real de
jogo: `NOTE LIST` / `NOTE READ <núm>` (ver `HELP NOTE`). Mural chamado
"Mural da Quest": tem ~15 notas de "Derinthuck" (staff), todas
datadas de 19/01/2008 — ENIGMAS/PROFECIAS numeradas (rimas em quadra,
estilo adivinhação) que compunham uma quest de resposta individual
("Uma somente [chance]", "Nada de equipe", resultado revelado só no
"último dia do prazo"). Pelo timestamp de 2008, é quase certo que essa
quest específica já se encerrou há muito tempo (conteúdo histórico/
arquivado, não uma atividade ativa hoje). Não vale a pena tentar
"responder" essas profecias específicas, mas o sistema `NOTE`
confirma que o MUD tem murais de quest reais — vale ficar atento a
murais mais recentes em outras salas.


## Exploração: Sala de Estudos (2º andar) + Mural da Academia (ativo, jogadores reais)
Corredor Silencioso -> porta leste marcada "Sala de idiomas" na placa,
mas a sala real se chama "Sala de Estudos": isolamento acústico, mesas
de estudo, estante (`look in estante` -> "contém: Nada" no momento,
sistema de pegar item útil existe mas estava vazia). Mural aqui é
"O Mural da Academia de Aventureiros" — ATIVO, com posts de
JOGADORES reais (não só staff), datados entre 2015-2019+ (bem mais
recente que o mural de profecias de 2008 da Sala dos Professores).
Exemplos: "Jenny" compra pergaminhos mágicos específicos (sagacidade,
inteligência draconiana, força ancestral, forma sombria, esfera
ância — NÃO é nosso pergaminho de retorno comum); menção a "Dóris"
(parece ser NPC/sistema de itens recorrente, visto em várias notas);
piada de jogador sobre um "Portal Extradimensional" seria ligado a
Esgaroth (confirma que Esgaroth/Lago Comprido existe no mapa do MUD).
Mural tem 15 notas no total, não lidas todas por economia de tempo —
pode valer revisitar se buscarmos vender pergaminhos ou entender o
sistema "Dóris"/portal melhor no futuro.


## Progresso: primeiro gold da sessão (2 moedas)
Vendemos pra Narinë (Centro do Jardim): mapa da Academia novo (1 gold)
+ fatia de carne de lobo sorrateiro (1 gold) = 2 gold total. Mapa de
Bri NÃO vendido (ela recusa esse item específico, confirmado em
sessões anteriores). Ainda insuficiente pra Vato Nogueira (5 gold) ou
hospedaria de Archet (10 gold), mas é um começo. Dar itens
"colecionáveis" quaisquer a Narinë parece ser fonte de gold
repetível (1 gold por item, sem limite diário confirmado).


## DESCOBERTA ENORME: Loja "Provisões para Jovens Aventureiros" (dentro da Academia!)
Corredor principal da Academia -> w (placa "Loja") = "Provisões para
Jovens Aventureiros". Vende MUITO barato (preços em gold):
  Núm  Nível  Item                              Preço
  1    7      par de manoplas de ferro          3
  2    6      armadura cristada                 5
  3    2      protetor de ferro p/ braços       3
  4    1      cantil de aventureiro             15
  5    1      colchonete de penas               10
  6    1      pergaminho de identificação       1
  7    1      PERGAMINHO DE RETORNO             1  <- baratíssimo!
  8    1      espada longa                      8
  9    0      dado de seis faces                4
  10   0      dado de vinte faces               4
  11   0      fatia de pão                      1
  12   0      LAMPARINA (fonte de luz)          2
Compramos 1 lamparina com os 2 gold ganhos de Narinë (ficamos com 0
gold de novo, mas agora temos luz!). PRIORIDADE: usar a lamparina pra
voltar e explorar a passagem secreta escura em "Fora do Portão Sul"
(abertura nas folhagens, nunca explorada por falta de luz).
Essa loja é MUITO mais barata que a Rua do Mercado de Bri para
pergaminhos de retorno (1 gold aqui vs. grátis-mas-aleatório dos
guardas) — vale lembrar como backup. `BUY`/`SELL`/`VALUE`/`AUCTION`
são os comandos de uso (ver respectivos HELPs); tem sistema de leilão
mencionado (`HELP AUCTION`), não testado.


## Mapa ASCII de Bri (item "um mapa da vila de Bri", `look mapa`)
O mapa mostra um layout em grade. Linha central tem: Sede(cura)/Casa
de Cura no topo, depois "Sya", Sede McD / Galinheiro, Biblioteca à
direita. Linha do meio: Sede Grn | Praça (centro) | Pônei Saltitante/
Estábulos | Academia (extremo direito). Abaixo: Tenda do Escriba/Loja
de Chás/Loja de Utilidades | Açougue/Padaria/Lacticínios. Mais abaixo:
Loja Esmeralda/Correios/Penas e Pergaminhos | Ferreiro/Armorial/Loja
de Armas. Depois de "Xaxim": Mansão Abandonada/Loja do Annir/Casa
Bill | Loja de Animais (extremo direito). O Portão Sul NÃO aparece
rotulado no mapa (deve ficar fora da área desenhada, mais a leste/
abaixo). Mapa é só leitura (`look mapa`), funciona como um pager de
texto (`p`/`m`/etc. pra navegar páginas, emenda direto nas Políticas
do jogo do MUD Valinor após a 2ª página — sair com `s`).


## DESCOBERTA: dungeon "formigueiro" sob o Portão Sul (precisa lamparina)
Com a lamparina acesa (`wear lamparina`, comprada por 2 gold na Loja
da Academia), voltamos a "Fora do Portão Sul" e refizemos
`examine folhagens` -> `open abertura` -> `d`. A passagem secreta
RESETA entre visitas (precisa reabrir toda vez, não fica
permanentemente aberta).
Desce para "Um Ponto de Junção sob o Portão Sul": "algo que lembra a
entrada para um formigueiro", túneis escavados na pedra pra n/s/e/w e
escada de metal `u` (não testada, provável saída alternativa).
Rota explorada (labirinto de "Junções"/"Curvas no Túnel da Galeria",
sem mapa): N -> E -> N -> W -> N -> N chegou em "Outra Interseção"
com 3 "pequeno morcego de aparência feroz" pendurados no teto —
NÃO hostis passivamente (não atacaram ao entrar na sala). Uma das
salas no caminho ("Uma Junção", mais limpa que as outras) tem um
"duto de ar" vertical, "liso demais para escalar" — provável acesso
secreto que precisa de equipamento/perícia não disponível ainda.
Decidi NÃO combater os morcegos (objetivo era explorar, não caçar) e
recuar em segurança. mv gasta rápido aqui (~4/passo vs ~2 normal em
Bri — terreno de masmorra mais custoso). Dungeon nível aparentemente
baixo (mobs "pequenos"), pode ser boa opção de caça futura quando
quisermos voltar a upar, MAS fica sob território que o guarda avisou
como arriscado (Portão Sul é zona "não-segura" fora da vila) — ainda
não teve exposição suficiente para avaliar o risco real de combate
aqui. Recomendação: se formos caçar aqui no futuro, seguir a regra já
estabelecida (fuga agressiva ao primeiro sinal de perigo, nunca lutar
com mv baixo).


## Exploração: Caminho Verde (ao sul da Interseção de Eriador)
Rumo ao antigo porto de TARBAD (Tharbad, referência real de Tolkien,
porto em ruínas no sul de Eriador). Andei `s` 4x a partir da
Interseção: só descrições repetitivas/genéricas de estrada vazia
("a Vila de Bri ainda está próxima..."), sem bifurcação ou ponto de
interesse novo nesse trecho inicial. Provavelmente uma estrada muito
longa (como a Grande Estrada do Leste até Valfenda) — não vale
continuar a pé sem objetivo claro. Voltei após 4 salas.


## ATENÇÃO: "aura azul" de proteção expirou nesta sessão
Mensagem vista: "A aura azul que envolvia seu corpo desapareceu
lentamente..." ao entrar na Grande Estrada do Leste (fora de Bri).
Essa aura provavelmente era alguma proteção temporária (recém-saído
da Academia? efeito de nível baixo? benção de algum NPC?) que
protegia Halbarion de perigo/PK fora da zona seguro. NÃO sabemos
exatamente o que ela fazia, mas sua expiração é um sinal de que
devemos ser MAIS cautelosos agora em áreas externas não-seguras do
que estávamos antes (ela pode ter sido um fator de segurança
implícito nas explorações anteriores que correram bem). Redobrar
atenção a HP/mv ao explorar fora de Bri/Archet de agora em diante.


## Exploração: início da Grande Estrada do Leste (rumo Valfenda) — AMBIENTE PERIGOSO
A partir da Interseção de Eriador, indo `w` (rumo Valfenda, contornando
pelo sul de Bri segundo o guarda): 2ª sala já descreve "colinas
escuras... nenhum sinal de vida... clima tenebroso... tremor aos
ossos" — tom claramente mais perigoso que qualquer área andada até
agora (incluindo o trecho seguro até Archet). 3ª sala tem ramal `nw`
pro bosque norte, sem saída `w` direta (preciso ir por `e` ou `nw`).
Recuei aqui por precaução: SEM a "aura azul" de proteção (expirou
nesta sessão, ver nota acima) e sem terreno/mobs testados, não vale
arriscar ir mais fundo rumo a Valfenda a pé sem companhia ou melhor
preparo. Quando quisermos de fato chegar a Valfenda, o caminho mais
seguro é claramente o Vato Nogueira (5 gold, viagem instantânea) em
vez de seguir a pé por essa estrada.


## Exploração: "Antes do Cemitério" (trilha leste da Velha Estrada Norte)
O "lugar desolado" mencionado na Velha Estrada Norte é um CEMITÉRIO
abandonado: cerca de ferro enferrujada, ervas daninhas, portão
derrubado e emaranhado de vinhas (`examine portao` -> decorativo,
bloqueado permanentemente). Saídas: `s` (não testada) e `w` (na
verdade volta pra Velha Estrada Norte, não é entrada do cemitério
propriamente — a sala em si JÁ é a entrada/borda do cemitério, "s"
deve ser o caminho real pra dentro). Nenhum mob visível na borda.
Recuei sem entrar mais a fundo (`s`) porque a fome chegou a "muita
fome" (estágio 3) nesse ponto — prioridade passou a ser comer.
PENDENTE: voltar aqui com fome/sede resolvidas e tentar `s` pra
explorar o interior do cemitério (potencial dungeon de mortos-vivos,
risco desconhecido, ir com cautela redobrada visto que a aura de
proteção expirou).


## Exploração: Rua do Xaxim (atalho secreto dentro de Bri)
Beco escuro ligando a Estrada do Falcão (oeste) à Avenida Zênite
(leste), atravessando o "miolo" de Bri. Descrição ameaçadora ("beco
particularmente escuro e abandonado... ratos guinchando... escuridão
se aprofunda") mas SEM perigo real: ratos são só decorativos, sem
combate. NPC "Rowlie Macieira" (aura branca, "enorme prazer de viver
em meio a plantas e animais") encontrado aqui, puramente decorativo.
`look caixotes` não achou objeto. Esse beco é um ATALHO útil entre
Estrada do Falcão e Avenida Zênite sem precisar passar pela Rua do
Mercado/Praça.


## Confirmado: interação do galinheiro com Nob FUNCIONA
`say Alimente as galinhas` dito a Nob (na taverna do Pônei Saltitante,
balcão) disparou reação real: "Nob ponderou 'Oh, como fui esquecer
disso? Sou um desastre mesmo...' Nob arruma rapidamente algumas coisas
antes de sair." e ele efetivamente saiu da sala (foi para o sul, rumo
ao galinheiro). Pequena interação de roleplay funcional, sem
recompensa aparente pra nós, mas confirma que o mundo reage a gatilhos
de fala específicos — bom sinal de que vale testar frases exatas
mencionadas em avisos/placas por toda a vila.

## Bardo Nedhellener: trigger de história/canção ainda não encontrado
Tentativas sem sucesso: `say`, `ask ... about historia/cancao`,
`listen bardo`, `talk nedhellener`, `converse nedhellener` — todas
deram "O que?" ou sem resposta. `look`/`examine` dão só o texto de
flavor sugerindo "uma conversa pode ser puxada". Sintaxe exata
permanece desconhecida; pendência mantida.


## DESCOBERTA ENORME: "Mansão Knob" — área de quest oficial nível 1-10
Trilha "pequena colina" (saindo de "Uma Trilha Perto de Bri", perto do
Portão Norte): N -> "Uma Trilha" -> N -> "Uma Colina Suave" -> U ->
"O Portão Principal": casarão de 3 andares, tijolos vermelhos, jardim
bem cuidado. Placa de bronze (`look plaqueta`) confirma ser área
OFICIAL de quest: "Bem vindo! Esta área foi desenvolvida para
jogadores de nível 1 a 10... -Cedrick, Abril de 1996" + adaptação por
"Eleuvis, Julho de 2003". EXATAMENTE nosso nível (6)!
Portão trancado (`examine portao` -> "estranhos sons vindos de dentro
do sítio"; comando certo é `open cerca`, não "portao"). Dentro:
"Depois do Portão Frontal" (porta da casa trancada "!n", convite de
flavor pra espiar) -> perímetro externo da casa (sala de visitas,
biblioteca vistas pelas janelas) -> "O Quintal" (fundos, N/E/S/W,
horta, 2 construções, algo misterioso atrás de cerca viva) ->
"No Interior do Quintal": NPC "servente da casa" (mal-humorado, mas
pacífico até agora), cabana trancada ao norte (odor horrível a oeste,
também trancado) -> "Um Cruzamento" (N=jardim, E=cheiro de feno/
estábulo) -> "O Jardim" (fileiras de flores, horta, parede de 6m):
NPC "jardineiro" (simpático, convida a sentar, oferece algo mas
"volte amanhã" — horário fechado) e NPC **"Lady Knob" / "Marry Knob"**
(mulher bonita, "aliança de esposa", ATACOU com um chute ao
aproximar-se pela primeira vez — "apavorada com sua presença" — mas
depois calma, não hostil persistente). Chute foi desviado sem dano.
Essa é claramente uma mansão de quest com família "Knob" (talvez
ligada a sequência de resgate/investigação). NÃO fomos feridos.
PENDENTE: explorar estábulo (E do Cruzamento), tentar entender o
gatilho da Lady Knob (hostil só na primeira aproximação?), tentar
achar chave pra cabana/casa principal. Sede chegou a "muita sede"
nesse ponto — resolver antes de continuar.

A Mansão Knob tem sua PRÓPRIA FONTE de água ("Oeste da Porta da
Frente", a oeste do portão frontal): `drink fonte` resolve sede
normalmente aqui dentro, sem precisar voltar a Bri. Útil saber se
formos explorar essa área mais a fundo no futuro.

Estábulo ("Entrada do Estábulo" -> `open porteira` -> e -> "Os
Alojamentos dos Cavalos", NPC "tratador de animais"): aqui aparece
**"Senhor Knob"**, o patriarca, que empunhou um chicote de equitação,
vestiu uma calça de couro, e trancou a porteira ao sair pelo norte —
comportamento de NPC com rotina/IA ativa (anda entre salas, se
equipa), não hostil diretamente mas desconfiado. Família Knob
completa catalogada: Senhor Knob (patriarca, chicote), Lady
Knob/Marry Knob (esposa, atacou uma vez por medo), servente da casa
(mal-humorado), jardineiro (simpático), tratador de animais (não
interagido ainda). Essa é certamente uma quest/mistério estruturado
(remete a enredos clássicos de "mordomo suspeito"/mansão assombrada
de áreas clássicas de MUD americanas dos anos 90, dado os créditos de
1996). PENDENTE para futura sessão: investigar mais a cabana
(residência de "alguém pequeno"), o "odor horrível" a oeste da
cabana, e a casa principal trancada — provavelmente uma sequência de
quest com objetivo e NPC-chave ainda não identificados.


## ATENÇÃO: mais um buff expirou ("Você não mais se sente tão resiliente")
Além da "aura azul" já registrada, outro efeito expirou nesta sessão:
"Você não mais se sente tão resiliente" (visto voltando da Mansão
Knob). Provavelmente uma bênção/buff temporário de proteção a mais
que estava ativo desde a criação do personagem ou desde uma morte
anterior. Reforça o alerta: Halbarion está ficando mais vulnerável
"de verdade" com o tempo, sem os buffs de novato que mascaravam riscos
reais nas primeiras explorações. Cautela redobrada permanece válida.

Mais um: "Sua resistência a paralisia lentamente se desfaz..." — 3º
buff de novato expirando em sequência nesta sessão (aura azul,
resiliência, resistência a paralisia). Confirma que é um PACOTE de
buffs temporários de recém-formado se esgotando com o tempo/uso,
não eventos isolados. A partir de agora Halbarion enfrenta o jogo
"normal" sem rede de segurança extra.


## DESCOBERTA: portões de Bri TRANCAM de noite
Tentei sair pelo Portão Norte às 20h (horário do servidor IC) e a
saída norte estava "!n" com `open n` -> "Está trancada." (trancada
de verdade, não só fechada — diferente das portas de loja que só
dizem "fechado"). É uma mecânica de segurança noturna real. Verificar
outros portões (Sul/Oeste) antes de assumir que todos fecham, e
lembrar de planejar viagens externas para o período diurno.


## Exploração: Biblioteca de Bri, Ala Oeste — livros "OS POVOS DE ARDA"
Mecânica de leitura: `get <livro> estante` (precisa espaço na
mochila) -> `look <livro>` mostra quantas páginas tem -> `book <livro>
read <página>` lê página específica.
- "Cuivienyarna - A Lenda do Despertar dos Quendi" (14 páginas): texto
  real de Tolkien (de História da Terra-média) sobre o despertar dos
  primeiros elfos (Quendi) na terra, os três pais-elfos Imin/Tata/Enel
  que acordaram primeiro e deram origem às palavras um/dois/três. Lida
  só a página 1 por economia; resto fica disponível pra leitura
  futura se quisermos o lore completo.
- "Dragões - Os Servos de Morgoth" e "Orcs - A Raça Corrompida":
  títulos vistos, conteúdo ainda não lido (mesma mecânica
  `book <livro> read <n>` deve aplicar).
Devolver livro à estante: ainda não testado (`put <livro> estante`
provavelmente).

- "Dragões - Os Servos de Morgoth" (keyword de item: "servos", não
  "dragoes"): página 1 fala de Glaurung (Pai dos Dragões, 1ª Era),
  Ancalagon (primeiro dragão alado), Scatha (dragão do norte gelado) e
  Smaug (último dos grandes dragões) — lore real e correto de
  Tolkien. Resto das páginas não lido (economia de tokens).

- "Orcs - A Raça Corrompida" (keyword: "orcs"): página 1 conta a
  origem clássica dos Orcs — Melkor nos Poços de Utumno (Primeira Era
  das Estrelas) torturou Elfos capturados até transformá-los em Orcs.
  Lore correto. Resto não lido.
Com isso os 3 livros da estante "OS POVOS DE ARDA" foram amostrados
(1ª página cada). A estante "OS PODERES DE ARDA" (Ala Leste) já tinha
sido lida por completo em sessão anterior.


## Exploração: andar superior do Pônei Saltitante (quartos)
`u` da Entrada da Hospedaria -> "Um Corredor Vazio" (sala luxuosa
leste trancada) -> n -> outro corredor com pinturas (salas leste/oeste
trancadas também, "!e"/"!w"). Mesmo sistema de Archet: precisa pagar
pela diária ao Sr. Carrapicho antes de acessar qualquer quarto. Não
testado quanto custa aqui em Bri (em Archet era 10 gold). Sem gold
agora, não foi possível testar.


## Exploração: Escritório do Copista (Biblioteca de Bri, sala leste do Saguão)
Trancada fora do horário (placa externa: "Horário de atendimento: 8
às 20 horas"), mas consegui `open e` e entrar mesmo já passado das
20h (talvez o fechamento real seja um pouco depois, ou é só decoração
sem enforcement estrito). Dentro: NPC "Ferion" (copista) não estava
presente no momento. Placa interna explica o serviço real:
- Custa 10 moedas + 1 moeda por página copiada.
- Só copia livros LACRADOS a pedido dos próprios autores (ou seja,
  não serve pra duplicar livros comuns como os da Ala Oeste/Leste).
- Comandos: `BOOK <livro> VALUE` (orçamento) e `BOOK <livro> COPY`
  (solicitar cópia). `HELP LIVROS` pra mais detalhes.
Não é útil agora (sem livro lacrado, sem gold), mas é um sistema real
documentado para referência futura.


## DESCOBERTA: Mural da Biblioteca de Bri — "Mobs Atalhos" e geografia avançada
Sala Reservada (oeste do Saguão da Biblioteca) tem seu próprio mural
"O Mural da Biblioteca de Bri", com posts técnicos de jogador "Kadzu"
(2013) explicando um sistema de "MOB's Atalhos": NPCs específicos
posicionados propositalmente nas pontas de áreas MUITO longas pra
servir de alvo de summon/resgate rápido (provavelmente via comando
`summon`, não testado/não disponível no nosso nível). Configuração
citada:
- "Valfenda - Passagem Alta", dentro do caminho para as MONTANHAS
  SOMBRIAS (= Misty Mountains, referência real de Tolkien): "cervo do
  campo" (keyword cervo/campo) na ponta oeste, "tamanduá mirim"
  (keyword tamandua/mirin) na ponta leste.
- "Caminho para as Montanhas Sombrias - Limiar do Ermo": "grande urso
  marrom" (keyword com espaços, nome completo) na ponta oeste, "tatu
  bola" (keyword tatu/bola) na ponta leste.
- "Caminho para as Montanhas Sombrias" tem QUATRO LADRÕES NPCs com
  quests: Anatole, Daudet, Gautir, Beringol.
- Aviso prático: "a maioria não checa seu ouro, e a hora do mud" —
  reforça que fome/sede e hora do dia são fatores de risco reais
  reconhecidos pela comunidade de jogadores, não só por nós.
Essa é uma área de nível mais avançado (Montanhas Sombrias), fora do
nosso alcance atual (nível 6), mas vale guardar pra referência futura
quando formos além de Valfenda.


## Exploração: Loja de Chás (Senhora Artemisas) + confirma lojas fechadas de noite
Rua do Mercado (interseção com Correio ao sul) -> n = Loja de Chás,
NPC "Senhora Artemisas". Fechada à noite: "Desculpe-me, mas você
poderia voltar amanhã?" (frase ligeiramente diferente de "mais
tarde" das outras lojas — pode indicar fechamento noturno específico
vs. intervalo de horário comercial normal). Confirma mais uma vez: a
maioria do comércio de Bri fecha de noite.


## Exploração: "A Esmeralda Brilhante" (joalheria)
Rua do Mercado (mais a oeste, interseção com "loja tenebrosamente
silenciosa" ao norte) -> s = "A Esmeralda Brilhante": joalheria com
vitrine trancada de gemas, pinturas, esculturas. NPC "o joalheiro"
(fechado à noite, mesma frase "voltar amanhã"). Provavelmente a
"Loja Esmeralda" do mapa ASCII. Pendente visitar de dia pra ver o
que vende (`list`).


## Exploração: Tenda do Escriba (NPC "Buraqueiro")
Mesma interseção da Esmeralda Brilhante, lado norte -> "A Tenda do
Escriba": NPC "Buraqueiro" vende pergaminhos (fechado à noite, mesma
frase). Interior rico em flavor (escriba transcrevendo pergaminhos
pra ganhar dinheiro). Pendente visitar de dia.

## Resumo: TODAS as lojas de Bri visitadas até agora fecham de noite
(Açougue, Padaria, Armorial, Loja de Utilidades, Loja de Chás,
Esmeralda Brilhante, Tenda do Escriba, Alfaiataria do Annir, Loja de
Armamentos, Loja de Laticínios, Mascotes e Montarias é EXCEÇÃO —
ficou aberta). Portões da vila (ao menos o Norte) também trancam de
noite. Planejar idas às lojas/saídas externas para o período diurno.


## Casa-Mathom: sintaxe de busca ainda não encontrada (tentativas exaustivas)
Testado nesta sessão: `search`, `procurar`, `look chao`, `vasculhar`,
`vasculhar quinquilharias`, `procure` — todos "O que?" ou "Você não
vê isto aqui". Note que `vasculhar` funcionou em OUTRO contexto
(folhagens do Portão Sul), então o verbo existe no jogo, mas a sala
da Casa-Mathom não aceita nenhuma keyword tentada até agora. Marcando
como pendência de baixa prioridade — pode precisar de um item
específico no alvo (ex: `vasculhar roupas`/`vasculhar garrafas`,
nomes exatos não testados) ou não ser realmente interativo.


## LIÇÃO IMPORTANTE: portas "trancadas" de noite podem ser abertas com `open`
Ao sair da Academia pelo `d` (saguão -> direto pro Amplo Bosque, um
atalho que pulou a "Entrada para a Academia"), a porta voltando pra
dentro estava fechada ("Está fechado.") mas `open n` FUNCIONOU sem
problema ("Você abriu a porta."), permitindo entrar normalmente.
Isso sugere que a trava noturna dos PORTÕES DE BRI (Norte/Oeste/Sul)
que bloqueou nossas tentativas anteriores pode também ter sido
contornável com `open n`/`open s` em vez de só andar na direção —
não tentamos `open` explicitamente nos portões antes, só andamos
direto e recebemos "Está fechado."/"Está trancada.". PENDENTE: na
próxima tentativa de sair de Bri de noite, tentar `open <direção>`
antes de desistir.
Nota de risco: fiquei brevemente exposto no Amplo Bosque à noite sem
a porta de volta aberta, com javali/coelho/felino próximos (não
hostis no momento, mas sem a aura de proteção isso poderia ter sido
perigoso). Reentrei em segurança sem dano.


## Correção: só o Portão NORTE estava trancado de noite, não todos
Testado: Portão Sul respondeu "Já está aberta." ao `open s` — estava
LIVRE o tempo todo, mesmo de noite. Então a trava noturna não é
universal a todos os portões; precisa testar cada um individualmente
em vez de assumir que todos fecham juntos.

## Perícia "Procurar" (search) — ainda não encontramos quem ensina
`practice info procurar` confirma a sintaxe real é `search` (inglês),
recomendada pro nível 5 (temos nível 6, deveria estar disponível),
ensinada por: Domick, "um velho guardião", "um guardião", Algiz (o
ex-caçador), "um sujeito maltrapilho", Marim Golpe-Forte. Tentamos
`practice procurar` com guardas comuns ("Um guarda está patrulicando/
em pé/vigilante") em várias salas (Estrada Horizonte, Portão Sul
dentro e fora) e SEMPRE deu "Não há ninguém capaz de ensinar isto
aqui" — ou seja, o "guarda" comum de patrulha NÃO é o "guardião"
necessário. Precisamos encontrar especificamente um dos NPCs nomeados
da lista (Domick, Algiz, Marim Golpe-Forte) ou o NPC itinerante "Um
velho guardião" (visto cruzando por ruas de Bri em momentos
aleatórios nesta sessão, nunca parado no mesmo lugar). Essa seria a
chave provável para finalmente resolver a Casa-Mathom.


## Exploração: Estábulo do Pônei Saltitante (NPC "Bob")
Pátio do Pônei Saltitante -> s = "Entrada do Estábulo", NPC "Bob".
Sistema OOC real: `GUARDARPET` (guardar animal de estimação comprado)
e `PEGARPET` (recuperar). Complementa a loja "Mascotes e Montarias"
(Avenida da Lei) — quando comprarmos um animal lá (ex: "o gato" por
30 gold, acessível no nível 6), guardamos/recuperamos aqui.


## Exploração: INTERIOR DO CEMITÉRIO (Velha Estrada Norte, trilha leste)
Entramos de fato no cemitério (não só a borda): "Entrada para o
Cemitério" (árvore podre, espinheiros, buracos, lápides — tudo
decorativo) -> "A Terra Irregular" -> "As Profanas Terras da Morte"
(menção a "criaturas grotescas" e saqueadores, mas nenhuma hostil
presente) -> "A Morte de uma Criança" (lápide triste de criança, NPC
"um coveiro" pacífico, cavando, ignora o jogador) -> "As Terras
Esburacadas" (esquilos, uivo de lobo distante) -> "As Terras Escuras"
(NPC "A viúva" passou, NPC "saqueador de túmulos" pacífico,
empunhando formão + escudo de placa roubada) -> "O Caixão de Thomas"
(caixão aberto com corpo, nota+rosa decorativos, sem interação) ->
"A Lápide Caída" (placa de bronze confirma nome "Thomas" de novo) ->
"O Túmulo do Guerreiro Desconhecido" (espadas cruzadas decorativas,
não pegáveis) -> "Um Túmulo Subterrâneo" (viúva lamentando, `say meus
pesames` sem resposta) -> "A Árvore Caída" (verme solitário inofensivo,
bloqueio de árvore caída força rota `se`) -> "Ao Longo da Cerca de
Ferro": aqui o texto vira aviso EXPLÍCITO de perigo ("ossos humanos
mastigados... violados por lobos... reconsidere seus pensamentos de
ir em frente").
NENHUM mob hostil encontrado em ~12 salas exploradas (coveiro,
saqueador e viúva são todos pacíficos/decorativos) — cemitério parece
ser majoritariamente atmosférico/lore, não uma dungeon de combate
nessa parte. RECUEI na "Cerca de Ferro" por causa do aviso textual
explícito, sem ter sofrido nenhum dano. Pendente: resto do cemitério
(saídas `s`/`w`/`nw` daqui não exploradas) se quisermos continuar
noutra sessão, com mais cautela ainda por causa do aviso de lobos.


## RESOLVIDO: perícia "Procurar" (search) aprendida com Domick
Domick, "Mestre do Conhecimento", fica na Sala de Treino de Perícias
(corredor principal da Academia, porta oeste "Treinamento de
Perícias"). Sintaxe correta pra praticar perícias com nome de mais de
uma palavra: `practice 'procurar'` (aspas simples), não
`practice procurar domick` nem sem aspas. Agora `search` está
disponível pra usar. PENDENTE: voltar à Casa-Mathom e testar
`search` lá (resolve finalmente aquela pendência antiga).

## Zurg vende "pedaço de carne de coelho" por 1 gold (estoque limitado a 1!)
Refeitório: `list` no Zurg mostra também cantil (16g), cogumelo (2g),
perdiz assada (2g) além da carne de coelho (1g, só 1 em estoque).
Usamos esse 1 gold (do chicote vendido a Narinë) pra comprar e comer
a carne, resolvendo fome crítica ("MORRENDO DE FOME") instantaneamente.
Ficamos de novo com 0 gold.


## LIÇÃO CRÍTICA: javali ficou MUITO mais perigoso sem a aura de proteção
Tentamos caçar 1 javali gordão na entrada do Amplo Bosque (mesmo
cenário "seguro" de sempre) pra conseguir gold. Resultado muito
diferente de antes: HP caiu de 84 -> 75 -> 60 -> 52 -> 47 -> 33 -> 23
-> 18 -> 13 em poucos ticks de combate, com mensagens de dano muito
mais fortes ("DESTRUIU você com seu golpe esmagador", "DESFIGUROU
você") do que o padrão anterior desta sessão. Isso confirma que os 3
buffs de novato que expiraram (aura azul, resiliência, resistência a
paralisia) estavam absorvendo dano real — SEM eles, o mesmo javali que
antes era rotina agora quase matou o personagem em menos de 10
segundos de combate.
`flee` precisou ser chamado 2x manualmente (mensagem automática "Você
tenta fugir, mas não vê como!" apareceu uma vez sozinha, não
confiável) e mesmo fugindo fomos perseguidos/atingidos de novo por um
segundo javali/mob na sala seguinte. Com HP em 13/84 (15%), recitamos
o ÚLTIMO pergaminho de retorno que tínhamos — sem ele, a situação
poderia ter sido fatal. Chegamos a 0 pergaminhos de retorno de
sobra. Cura em leitos da Sala de Cura recuperou rápido (18->59 em
~15s, depois 59->84 completo ao levantar).

### REGRA NOVA, CRÍTICA: NÃO CAÇAR MAIS no Amplo Bosque sem repor
pergaminhos de retorno E reavaliar risco real (buffs de novato
acabaram, o bosque pode estar MUITO mais perigoso agora do que
documentado em notas anteriores desta sessão). Considerar: praticar
"Esquivar"/outras perícias defensivas, comprar elixires de cura antes
de caçar, ou evitar caça corpo-a-corpo até reavaliar equipamento/CA
(atualmente CA 3-4 de 10, baixa).


## Casa-Mathom: `search` funciona mas 8 tentativas = 0 itens achados
Com a perícia Procurar aprendida, `search` na Casa-Mathom dá
"Você começa sua busca..." seguido de "Você não encontrou nada." em
TODAS as 8 tentativas consecutivas. Proficiência limitada a 85% no
nível atual, então estatisticamente improvável (mas não impossível)
falhar 8x. Provavelmente a sala realmente não tem nenhum item restante
pra achar agora (outros jogadores já pegaram tudo?) ou nunca teve.
Desistindo dessa sala por ora — não vale mais tempo/tokens.
PENDENTE: tentar `search` em OUTRAS salas com descrições sugestivas
(ex: Rua do Xaxim com seus caixotes, ou outras áreas "caóticas"/
"escondido") já que a perícia está disponível agora.


## DESCOBERTA: "A Academia de Combate" (acessível só pelo Amplo Bosque)
No bosque, uma sala tem descrição "No sul, uma pequena construção de
pedras não permite que você veja o que há além dela" com saída "!s"
(trancada, `open s` resolve). Dentro: "A Academia de Combate" (NPC
"mestre Thanthal", um elfo) — sala de duelo com cartaz na parede
oeste listando "principais perícias que um corajoso guerreiro
necessita aprender" (não lido ainda). Só tem saída `n` de volta pro
bosque — é uma entrada alternativa de treino, não conecta à Academia
principal. Pendência: ler o cartaz, testar practice com Thanthal.


## Tentativa de gold via caça leve: resultado modesto, raposa é segura mas não rende item
Caçamos 2 raposas preguiçosas no Amplo Bosque com sucesso e segurança
(dano recebido: ~7-9 HP por raposa morta, bem mais seguro que o
javali). MAS: `slice corpo` falhou/"não é fonte adequada" em ambas
(raposa não dá carne cortável, diferente de javali/coelho/bezerro/
lobo/macaco documentados antes). Corpo inteiro também recusado por
Narinë ("não me interessam corpos"). Ou seja, CAÇAR RAPOSA É SEGURO
MAS NÃO GERA GOLD/ITEM ALGUM — só XP (ganhamos 89 + 108 = 197 XP no
total, sem risco real). Para gold de fato, precisaríamos focar em
mobs que dão item/carne vendável (javali, coelho, bezerro, lobo,
macaco grande) — mas esses são mais arriscados (javali quase matou
antes).
Avaliar com o usuário: continuar caçando raposas só por XP (seguro,
ajuda a subir nível/perícias mas não resolve o problema do gold para
Valfenda), ou tentar skinning/slice em outro mob mais arriscado.


## RESOLVIDO: estratégia segura pra gold — bezerro + slice + Narinë
Matamos 1 "bezerro assustado" (bosque, perto da entrada) com ZERO
dano recebido (84/84 intacto o combate todo) + ganhamos 328 XP total
(1 do kill + 327 do slice bônus). `slice corpo` funcionou de primeira
("Você corta um pedaço de carne do corpo de um bezerro"). Demos a
carne a Narinë = 1 gold. Bezerro é claramente o alvo mais seguro e
lucrativo encontrado até agora (mais seguro que raposa em termos de
dano, e GERA item vendável, diferente da raposa). ESTRATÉGIA PADRÃO
daqui pra frente pra gold rápido: localizar bezerro no bosque, matar,
slice imediatamente, levar carne pra Narinë, recuar se javali
aparecer antes de concluir.


## CORREÇÃO + DESCOBERTA ENORME: "A Gruta Profunda" (guilda de ladrões escondida)
A "pequena construção de pedras" no Amplo Bosque (saída `!s`, `open
s`) NÃO é sempre a mesma sala — dessa vez levou a algo totalmente
diferente de "A Academia de Combate" (visto antes): **"A Gruta
Profunda"**, uma guilda de ladrões disfarçada de "pequeno galpão" por
fora. Descrição rica: frequentada por encapuzados e por pessoas
comuns vistas no bosque que ninguém suspeitaria serem criminosas.
NPC principal: **"Mirindhel, a mestra dos ladrões"**, sentada numa
cadeira luxuosa observando os outros. Outro NPC: "uma anã orientando
os aprendizes" (trainer, não identificado se ensina perícias de
ladrão como Roubar). "Um neófito" lê um aviso na parede (`look aviso`
não achou, decorativo). Isso explica a entrada do Amplo Bosque como
PORTAL CONTEXTUAL de novo (como visto na Academia de Aventureiros) —
a mesma sala externa "!s" leva a destinos diferentes dependendo de
algum fator não identificado (talvez aleatório, talvez relacionado a
classe/alinhamento do personagem). Nenhuma hostilidade sofrida ao
entrar. Não tentamos interagir mais a fundo (prudência, é território
de "atividades criminosas", pode reagir mal a um Guerreiro comum
andando por lá). Saída: apenas `n`.


## DESCOBERTA ENORME: pão cura fome instantaneamente (sem cozinhar!)
"Provisões para Jovens Aventureiros" (Corredor 2 do corredor principal,
porta oeste "Loja") vende "uma fatia de pão" por 1 gold. `eat pao` cura
fome CRÍTICA ("MORRENDO DE FOME") na hora, sem precisar da perícia
cozinhar nem de fogo — ao contrário da carne crua (`eat fatia` de carne
dá "Isto precisa ser cozido."). É a solução de emergência mais rápida
pra fome, mais barata que correr pro Zurg. "Um caroço de maçã" (item do
inventário inicial) NÃO é comestível (`eat caroço` não faz nada, mensagem
"Você tentou morder..." sem consumir o item) — é só decoração/isca, não
comida de verdade.

## Rota exata: Saguão -> Centro do Jardim (Narinë)
Do saguão de entrada: `n` (Corredor 1: Perícias/Magias) -> `n` (Corredor 2:
Loja/Idiomas) -> `n` (Corredor 3: Cura oeste / Refeitório leste) -> `n`
(O Centro do Jardim, onde fica Narinë). Da sala do Jardim, a saída `!n`
(fechada) leva ao Portão Norte -> Amplo Bosque; `open n` antes de ir.
Essa é a rota confiável pra ir vender itens a Narinë e caçar no bosque.

## Pista: "Academia ao norte/oeste/noroeste" no Amplo Bosque é só flavor text
Várias salas do Amplo Bosque descrevem "Ao norte/oeste/noroeste, ergue-se
a grande Academia dos Aventureiros" mas isso NÃO é uma saída navegável
nessas salas — tentar a direção indicada dá "Oops. Por ali não...". A
ÚNICA sala que realmente entra na Academia é a que descreve "Ao norte,
acima de uma pequena escadaria, fica a ampla porta da academia dos
aventureiros" com saída real `!n` (precisa `open n` primeiro). Não confie
no texto ambiental pra navegar — só nas saídas listadas.


## MARCO ENORME: CHEGAMOS A VALFENDA (Imladris) via charrete do Vato Nogueira!
Depois de juntar 5 gold (bezerro/macaco + slice + Narinë), fomos até Vato
Nogueira (Grande Estrada Leste, oeste da Praça de Bri) e completamos a
viagem. Sintaxe exata (corrigindo nota anterior): `sit charrete` ->
`give 5 moedas vato` (NÃO "give gold" nem "give 5 gold", precisa ser
"moedas" em português) -> `say Leve-me para Valfenda` (frase EXATA, não
"say Valfenda" solto — confirmado via HELP VATO NOGUEIRA: "Leve-me para
cidade-de-destino"). A viagem é 100% automática e segura: o personagem
fica sentado na charrete e Vato cavalga sozinho por dezenas de salas,
nenhum combate ocorre mesmo passando por áreas com descrições ameaçadoras
("sons estranhos", "sombra imensa", trechos "Nos Limites de uma Floresta
Sombria"). HP e movimento ficam parados/regenerando passivamente durante
toda a viagem.

### Rota completa (lore 100% Tolkien/Bree-Rivendell):
Grande Estrada Leste (Bri) -> Praça de Bri -> Portão Sul de Bri (dentro
-> fora) -> Sobre um Passadiço -> Próximo ao Portão Sul -> A Grande
Estrada do Leste (início) -> Contornando a Colina de Bri -> dezenas de
salas genéricas "A Grande Estrada do Leste" (trechos secos/empoeirados,
"quilômetros e quilômetros", passa perto de Estrado e Archet ao sul) ->
clima vira sombrio/"silêncio sepulcral" -> Um Atalho (região desolada,
"sons estranhos rondam a área") -> sobe uma colina ("não se pode ir mais
fundo do que onde você chegou") -> avista DOIS RIOS ao longe -> **A
Última Ponte**, cruzando o **rio Fontegris (Mitheithel pros elfos)** —
referência real exata do livro (Last Bridge / Vale do Mitheithel) ->
Escalando o Desfiladeiro (ruínas de torres antigas visíveis nas colinas,
"aparência agourenta") -> Nos Limites de uma Floresta Sombria -> **vimos
Glorfindel, o Senhor-Élfico, montado em seu cavalo branco Asfaloth**,
parados numa sala com uma "PASSAGEM" escondida (referência direta à
cena do resgate de Frodo no livro!) -> desce a colina, vale com paredes
de pedra vermelha -> tráfego aumenta (carroças, cavaleiros) -> **Vau do
Bruinen** (travessia rasa do rio) -> Às Margens da Floresta -> Olhos
para o Vale (primeira vista de Valfenda: "Imladris, Valfenda, a Última
Casa Amiga") -> A Estrada Rochosa -> **A Ponte sobre o Bruinen** -> Curva
entre Árvores -> **Uma Enorme Área Coberta** (arquitetura élfica: bases
de madeira entalhada, teto cristalino, sem paredes) -> Uma Alameda de
Pópulos -> **O Bosquepraça** (destino final): praça com estátuas-lamparina
sobre pedestais, fonte em cascata, círculo de bancos de pedra.

### Valfenda — primeiras descobertas
"O Bosquepraça" é (Seguro) — zona segura, como a Academia. NPC **"A
Guardiã elfa"** (aura branca) atua como GPS de Valfenda: `look` nela
quando precisar achar lojas/locais ("Eu sou a Guardiã de Valfenda e
posso te ajudar com algumas localizações"). Vato Nogueira fica esperando
aqui mesmo por um tempo e pode levar pra outro destino a qualquer
momento (não precisa voltar até Bri pra reutilizá-lo, mas cada corrida
nova custa 5 moedas de novo, salvo crédito adiantado — ver HELP VATO
NOGUEIRA). Saídas do Bosquepraça: nw, se, sw — ainda não exploradas.


## Valfenda: "A Guardiã elfa" é o GPS local (mesmo padrão dos guardas de Bri)
Sintaxe correta pra falar com ela: `whisper guardia preciso de ajuda` (não
`whisper ... to ...`). Lista de locais que ela conhece em Valfenda: A
Grande Estrada Leste, Academia de Aventureiros, Alfaiataria, Aposentos
Reais, Caminho para as Montanhas Sombrias, Casa de Alimentos, Casa de
Animais, Casa de Cura, Casa de Doações, Casa de Estudos, Casa de
Utilidades, Floresta de Pinheiros, Indumentária e Fundição. Confirma que
há uma Academia de Aventureiros também em Valfenda (ou é o mesmo hub
único de Archet/Bri?) e um "Caminho para as Montanhas Sombrias" (citado
no mural antigo da Biblioteca de Bri — rota pras Montanhas Sombrias,
bem além do nível atual). Clima dinâmico observado: "Começa a nevar" em
Valfenda mesmo sem neve em Bri.
Rota pra Casa de Alimentos (a partir do Bosquepraça): nw -> n (até achar
entrada leste) -> e -> n (segunda entrada norte) -> n (até o Círculo
Florido) -> ne -> s -> chegou na loja.


## Valfenda: macieira grátis também existe aqui (Uma Alameda de Juníperos)
Mesma mecânica da Avenida Zênite em Bri: `get maçã macieira` colhe do
galho mais baixo (sem precisar subir/arriscar queda), `eat maçã` cura
fome instantaneamente, de graça, infinitas vezes. "Uma Alameda de
Juníperos" fica a `nw` do Bosquepraça. Saídas: n, se, sw.


## Exploração: Jardim de Imladris (leste do Bosquepraça/Alameda de Juníperos)
Acesso: Bosquepraça -(nw)-> Alameda de Juníperos (com macieira grátis)
-(n)-> 2ª Alameda de Juníperos -(e)-> Na Entrada do Jardim de Imladris
(tem a entrada da Academia de Aventureiros local — oeste — confirma
mais uma vez o hub único citado antes; NPC decorativo "tartaruga
simpática"; estante de material de Academia). Daqui, `n` leva a um
mini-labirinto circular de salas "No Jardim: Um caminho entre Canteiros"
e "Jardins: Ervas Perfumadas"/"No meio das Flores" que se repetem e
voltam uma pra outra facilmente (fácil se perder, nomes de sala iguais
com descrições quase idênticas). Destaques:
- Menção a uma "entesposa" vista de canto de olho (referência direta a
  Tolkien: as Entwives, esposas perdidas dos Ents).
- "Uma casa de marimbondos" ao sul de "Jardins: Ervas Perfumadas" (2ª
  versão) — não investigada, risco potencial.
- "Um mural bem legal está aqui no meio do nada" aparece em quase toda
  sala do jardim mas `look mural` / `read mural` não funcionam (keyword
  exato não encontrado ainda, ou é 100% decorativo/piada meta do mapeador).
Ainda não achamos o "Círculo Florido" citado pela Guardiã elfa na rota
pra Casa de Alimentos — a rota dela pode usar nomes de sala específicos
diferentes dos que vimos (ou o labirinto exige mais tentativas).


## Descoberta: "A Árvore dos Contos" (Jardim de Imladris, extremo sul)
Sala "No Extremo Sul do Jardim: Flores" (via Jardim -> ... -> se, a
partir da sala "Jardins: No meio das flores" com a bela referência "as
jóias dos Noldor"). Tem uma árvore mágica com inscrições no tronco —
funciona como um BOARD de verdade: `look árvore` dá a descrição, `note
list` lista as mensagens, `note read N` lê cada uma. Conteúdo (histórico
de construção de área, 12/06/2011, pelo builder Derinthuck, mesmo nome
visto no board de profecias da Academia): testes iniciais da feature
"árvore-mural", um recado de "Selkie", e uma nota de Derinthuck
explicando que só pode haver 1 mural por sala (teve que escolher entre o
mural genérico e a árvore) e convidando jogadores a sugerir "ideias de
construção" pra área antes de "rodar oficialmente". É puramente
histórico/meta — não achamos como adicionar uma nota nova (nem éramos
convidados a isso hoje, só é um registro congelado de 2011).


## DESCOBERTA ENORME: segundo charreteiro em Valfenda — "Faelar Anor"
Em "Uma Alameda de Pópulos" (leste do Bosquepraça, via se->e a partir
do Bosquepraça, ou alcançável pela Área Coberta -> nw -> e), há outro
NPC charreteiro: **Faelar Anor**, com uma "grande charrete com rodas
reforçadas" e um potro. Mesma mecânica do Vato Nogueira (5 moedas,
`sit`, `give`, pedir destino), mas com destinos MUITO mais distantes e
avançados — claramente fora do nível atual (6):
- Rumo OESTE: Mata dos Trolls, Topo do Vento (Weathertop — lore real!),
  Estrado, Bri.
- Rumo LESTE: Passagem Alta, Limiar do Ermo, a Carrocha (Carrock —
  referência ao Hobbit/Beorn!), Acampamento do Anduin, Terras de Beorn.
`HELP CONDUTORES` tem mais detalhes gerais sobre esse sistema de
transporte (não lido ainda). NÃO viajamos pra lá ainda — são destinos de
endgame/alto nível, guardados para quando Halbarion estiver mais forte.
Essa mesma Alameda de Pópulos tem uma arcada ao sul que leva a "uma área
cheia de moradas silvestres... casas de elfos" (bairro residencial de
Valfenda, ainda não explorado).


## Valfenda: sistema de compra de casas (housing, endgame)
Bairro élfico ao sul da Alameda de Pópulos: "Entre as Alamedas das
Ameixeiras e dos Ipês" -> s -> "No Centro das Casas: Fonte de Aguapés"
(ruas: Ipês, Ameixeiras, Tulipas; casas numeradas 1-48, todas iguais,
9 cômodos). `open e` dá acesso ao "Empório das Casas", NPC Learin
Verde-Braço. Custo: 50000 moedas por casa + taxa de manutenção anual de
2500 (bloqueio de acesso se não pago em 30 dias OOC). Comandos: `comprar
<N>`, `listar`, `pagar taxa`, `vender`. Totalmente fora de alcance
agora (0 gold), registrado só por completude de mapeamento.
Carpintaria do elfo carpinteiro fica a oeste da Fonte de Aguapés (não
visitada ainda) — faz mobília, não achamos indicação de vender armas.


## Exploração: "A Pinacoteca" e Biblioteca de Valfenda (norte do bairro élfico)
A partir da Fonte de Aguapés/Alamedas, seguindo várias salas "Uma
Alameda de Juníperos" (cada uma com um texto contemplativo/filosófico
diferente sobre o tempo parado em Valfenda — "alheias aos círculos do
mundo", referência direta a Tolkien), uma delas tem saída `w` pra "A
Pinacoteca": uma galeria de arte élfica (tapete vermelho, pinturas de
todos os temas, algumas ainda embrulhadas/não expostas) com escadas
(`u`) subindo para "Outro Corredor pela Biblioteca" — uma biblioteca
enorme (livros, pergaminhos, cadernos) com NPC "O bibliotecário". Ainda
não exploramos os livros em si (igual fizemos na Biblioteca de Bri).
Uma saída norte na Alameda de Juníperos leva a um beco sem saída: o
"Serviço de Correios" dos elfos (NPC Celorien Ramo-Verde, mesmo sistema
OOC de correio visto em Bri, com uma piada meta "Tweets recentes").


## Descoberta: "O Cartógrafo" (Eartitton) — sobe pela Pinacoteca/Biblioteca
Acesso: ... -> Biblioteca (Outro Corredor pela Biblioteca, final do
corredor) -> `d` -> "O Cartógrafo". NPC Eartitton vende mapas (não
armas): caneta-tinteiro (10g), mapa das cercanias de Bri (2g), mapa de
Archet (2g), mapa de Bri (4g), **mapa de Valfenda (4g)**, mapa de couro
lupino (2g), **"mapa do Caminho para as Montanhas Sombras" (2g)** — esse
último é revelador: confirma de novo que existe conteúdo de altíssimo
nível rumo às Montanhas Sombrias (igual achado no mural antigo da
Biblioteca de Bri), folha de papel em branco (1g). Sem gold agora (0)
pra comprar, mas o mapa de Valfenda seria muito útil pra não se perder
no labirinto de alamedas — prioridade de compra na próxima leva de gold.


## Exploração: Alameda de Plátanos + "Loja Magia Boa é Magia Pura"
A leste do "Encontro das Alamedas de Juníperos e Plátanos" (que por sua
vez é 1x n a partir da 2ª Alameda de Juníperos, perto do Bosquepraça)
começa a "Alameda de Plátanos" (arquitetura rica, janelas-portal).
Seguindo east, uma porta `!s` leva à "Loja Magia Boa é Magia Pura":
sala bagunçada e divertida com itens mágicos flutuando, soltando
fumaça e faíscas sem padrão algum. NPC "Aissa, a protegida do Maider"
está lá apenas testando magia — não é possível comprar dela (`list`
dá "Eu não consigo entender você", não é um lojista funcional, é
decorativo/easter egg).


## Descoberta: "A Casa de Estudos" (um dos locais listados pela Guardiã)
Acesso: a partir da Alameda de Plátanos -> n ("Os Corredores de Entrada",
estátuas de reis/guerreiros) -> n ("O Saguão Principal do Museu") -> n
("Escadarias de Acesso") -> u ("Os Corredores Circulares" — CONFIRMA que
o Museu, a Pinacoteca e a Biblioteca de Valfenda são o MESMO complexo
gigante interligado por corredores circulares e escadarias, assim como
a Academia é um hub único entre Bri/Archet/Valfenda) -> n ("Escadarias
de Acesso", outra, fim dos corredores de livros) -> d (desce por uma
escada "que não faz parte da biblioteca") -> **A Casa de Estudos**.
NPC (sem nome capturado ainda) vende misturas de ervas/temperos/
especiarias/iguarias (3-5 gold, níveis 1-12) — parecem ser
consumíveis culinários/de buff, não armas. Saídas daqui: n, e, w, u.


## Descoberta: "A Alfaiataria" de Valfenda (Alameda de Olmeiros)
Acesso: Casa de Estudos -> n -> "Uma Alameda de Olmeiros" (encosta das
montanhas talhada em escada de pedra) -> n -> **A Alfaiataria**. Vende
roupas finas, não armaduras de combate: fina calça/camisa de seda
(26g, nível 17-18), vestido com alças (2g, nível 10), calça com listras
(2g, nível 9), calça curta (2g, nível 7), calça de couro fornido (2g,
nível 6), manta bordada (3g, nível 3). Preços baixos mas níveis
relativamente altos para o que parecem ser itens cosméticos/leves.


## Achado: "Um Círculo Florido" (praça central, macieira + fonte juntas!)
Alameda de Olmeiros -> e -> **Um Círculo Florido**: área circular aberta
com canteiros, bancos de pedra, UMA MACIEIRA e uma fonte de pedras
verdes no mesmo lugar — ponto ideal de recuperação (fome + sede num só
lugar) em Valfenda. Três ruas partem daqui: Altéias, Olmeiros e
Casuarinas. Esse é o "Círculo Florido" que a Guardiã elfa citou na rota
pra Casa de Alimentos.


## Achado: "A Casa de Alimentos" (= "Casa de Refeições") + NPC Lindir!
Círculo Florido -> e (Alameda de Altéias) -> s -> **A Casa de
Refeições**. Vende: bolo de frutas silvestres (1g), cacho de uvas (3g),
favo de mel (2g) — tudo nível 0, bem barato. NPCs: "um alegre vendedor",
"um simpático elfo à procura de histórias para ouvir" (roleplay, não
testado ainda), e vimos **"Lindir" passando e indo para o norte** —
Lindir é um elfo canônico de Valfenda no livro/filme O Senhor dos Anéis
(cantor/membro da corte de Elrond que recebe Frodo)! Confirma novamente
o cuidado do MUD em povoar a área com NPCs de lore real.


## Fronteira norte de Valfenda: "Uma Ladeira de Pedras" (provável início do Caminho para as Montanhas Sombrias)
Seguindo a Alameda de Altéias totalmente a leste (via Círculo Florido
-> e -> e -> e -> e -> "Encontro das Alamedas de Choupos e Altéias" ->
ne), chega-se a uma zona de transição rumo às montanhas, com paredões
de pedra e vertigem ao olhar pra cima. NÃO explorado além disso — é
provavelmente o início do "Caminho para as Montanhas Sombrias" que a
Guardiã citou, uma área de nível muito mais alto. Recuamos para focar
em achar a loja de equipamentos ("Indumentária e Fundição") ainda
dentro da cidade.


## Achado: "A Casa de Animais" de Valfenda (Alameda de Choupos)
Círculo Florido -> e (Altéias) -> ... -> Encontro de Choupos e Altéias
-> w -> Alameda de Choupos -> e -> **A Casa de Animais**: estábulo/
hospedagem de montarias e bichos de estimação pra viajantes, mesmo
conceito do estábulo do Pônei Saltitante em Bri. Sem uso prático agora
(sem montaria).


## MARCO GIGANTESCO: "Os Salões de Elrond" + "O Salão do Fogo" (lore 100% canônico!)
Rota (via Alameda de Choupos): ... -> w (Uma Majestosa Arcada, tapete
vermelho/incenso) -> w -> **O Saguão Principal** (circular, 6 pilares,
candelabro de joias/ouro, janelas de vidro colorido, 2 escadarias) -> n
-> Majestosa Arcada -> ne -> **Os Salões de Elrond** (corredores de
pedra sem janelas, bem mais sóbrio/sério que o resto da cidade) -> `open
e`, e -> **(Seguro) O Salão do Fogo** — referência DIRETA e exata ao
livro "O Senhor dos Anéis" (capítulo "Muitos Encontros", onde Frodo
reencontra Bilbo cantando em Valfenda)! Tem uma lareira com chama
dourada. NPC ativo: **"Dunendel, o mensageiro da cidadela branca"**
(cidadela branca = Minas Tirith/Gondor!) "caminha por aqui em busca de
Elrond" — sugere um gancho de história/quest em andamento envolvendo
Gondor e Elrond. Ainda não falamos com ele. Saídas do Salão do Fogo: n,
s, w (não explorado mais a fundo ainda nesta sessão).


## Pendência: trigger do menestrel no Salão do Fogo não encontrado
"Um menestrel" no Salão do Fogo (sala interna, s do Salão do Fogo
principal) tem descrição que convida a "ouvir o que esse elfo tem a
tocar" (lira de sete cordas), mas `listen menestrel` e `listen` sozinho
deram "O que?" — mesmo mistério do bardo Nedhellener no Pônei
Saltitante em Bri, ainda sem solução. Possivelmente syntax diferente
(ask, hum, ou precisa de item/perícia específica) ou só decorativo.


## DESCOBERTA: "Uma Passagem Bem Guardada" + guardas falando Sindarin (puzzle de endgame)
Rota: Saguão Principal -> nw -> Escadarias Oeste -> u -> **A Nave
Superior** (corredor circular com parapeito olhando o salão principal,
bandeiras em cada pilar) -> ne -> **Uma Passagem Bem Guardada**. Porta
norte `!n` está LACRADA com trincos e fechaduras — texto explícito:
"Mesmo que tivesse a chave, ainda seria necessária muita força para
mover a gigantesca placa" (NÃO tentamos abrir, fora de alcance). Dois
"guarda real" ficam imóveis e falam em Sindarin (élfico, provavelmente
texto cifrado/fictício de propósito):
'Iwá Tewqvilyauih!' e 'Sowe stthowequsvilya stessvilya stvilyae bad ei
owehqihlthi ngi hîr ane Imladris, qemae pedo: anesoweshi boweth
owewthihng'. Isso provavelmente guarda a câmara/trono do próprio Elrond
— claramente conteúdo de nível muito mais avançado que o atual (6).
Saídas da Nave Superior: d, ne, se — "se" (rumo sul, luz e vento
externos pelas cortinas) ainda não explorado.


## Pequeno easter egg: sinos do Terraço (Casa de Reis)
No "O Terraço" (2º andar da Casa de Reis, via Nave Superior -> se),
há "uma corda suspensa" ligada a dois sinos no topo de uma torre.
`pull corda` toca os sinos com estrondo, mas não gerou nenhum efeito
visível (nenhuma mudança na sala, nenhum NPC reagiu) — parece ser só
ambientação sonora/decorativa.


## Rota mais curta: Casa de Reis <-> Círculo Florido
Do Saguão Principal da Casa de Reis: `w` (Majestosa Arcada) -> `w`
("Uma Alameda de Casuarinas", entrada de uma casa grande, NPC
"uma criança") -> `n` (outra Alameda de Casuarinas, com passadiço
elevado ligando duas torres) -> `n` -> **Um Círculo Florido** (macieira
+ fonte). Mais rápido que o caminho original via Alameda de Altéias.


## DESCOBERTA: Floresta de Pinheiros (arredores de Valfenda) + alvo seguro "morcego peludo"
Rota completa desde o Bosquepraça (dada pela Guardiã elfa): `se, sw, s,
w, s` -> A Estrada Rochosa -> `w` -> Às Margens da Floresta -> `s` ->
dentro da floresta (lagoa, clareiras, caminhos). No caminho, um
guardião deu outro pergaminho de retorno de graça (mesmo mecanismo de
Bri, confirmado funcionando em Valfenda) na sala "Olhos para o Vale".
ATENÇÃO: inventário lotou com os caroços de maçã inúteis acumulados —
tivemos que `drop all.caroço` pra liberar espaço e conseguir pegar o
pergaminho (sintaxe `all.<palavra>` funciona pra descartar todos os
itens com aquele nome de uma vez).
Dentro da floresta: "Uma Clareira Escura Fora da Caverna" tem aviso
textual explícito de perigo ("há um mal caminhando no interior") — NÃO
entramos na caverna oeste. Avançando pelas clareiras ao sul/oeste,
encontramos **"um morcego peludo"**: alvo CONFIRMADO seguro (perdeu
apenas 1-2 HP por ataque recebido, matou em 3 golpes, 5 XP) e, melhor
ainda, **dropa item ao morrer**: "um canino de morcego" (sem precisar
de slice!). Candidato a novo alvo padrão de farm em Valfenda,
equivalente ao bezerro de Bri — ainda não testamos vender o canino a
algum NPC comprador local (equivalente a Narinë).


## DESCOBERTA ENORME: "Sala de Doações" de Valfenda (itens gratuitos de outros jogadores!)
Rota: Bosquepraça -> se, e, e (3x leste pela Alameda de Pópulos, passando
pelo charreteiro Faelar Anor) -> n ("A Casa de Descanso" — hospedaria
de Valfenda, com "A Recepção" logo oeste, NPC recepcionista, quartos no
andar superior `!u`) -> w, w -> **Sala de Doações**. Jogadores reais
depositam aqui itens que não usam mais, e qualquer um pode `get` e
levar de graça! Achamos (e pegamos): "uma tosca bainha de couro"
(precisa nível 22 pra vestir) e "uma fina camisa de seda" (precisa
nível 17 — essa mesma camisa é vendida por 26 gold na Alfaiataria!).
Ambas muito acima do nível atual (6), guardadas pro futuro. Vale
voltar aqui sempre que passar por Valfenda — o conteúdo da sala muda
conforme jogadores doam/pegam itens, pode ter achados de nível baixo
em outras visitas. Esse é o lugar certo pra buscar equipamento de
graça em Valfenda, mais interessante que comprar na Indumentária e
Fundição (que, aliás, ainda não localizamos).


## Achado: "Casa de Cura" de Valfenda — NPC Isilië + referência a Lothlórien
Perto da Casa de Descanso (e da Sala de Doações), via `e` a partir da
Casa de Descanso: **Uma Sala de Espera** = Casa de Cura de Valfenda.
NPC "Isilië, a curandeira" (equivalente a Mestre Toric de Bri), cura
passivamente com encantamentos ('naimad'/'nran'). Tem fonte de mármore
pra beber. "Camas simples com colchões de folhas de MALLORN" — mallorn
são as árvores douradas de Lothlórien no livro, outra referência real
de Tolkien. `sleep camas` cura e regenera HP/mv rapidamente, igual à
Sala de Cura de Bri.


## Bestiário da Floresta de Pinheiros: dois tipos de morcego distintos
- **"Um morcego peludo"** (encontrado nas clareiras/junções): MUITO
  seguro, perde-se ~1-2 HP por golpe recebido, morre em 2-3 acertos,
  5-22 XP, dropa **"um canino de morcego"**.
- **"Um grande e nojento morcego"** (encontrado na lagoa): tanque mais
  forte — levou a HP de 84 a 71 (~15%) numa luta mais longa (6+ rounds),
  40 XP, dropa **"uma folha negra"** em vez de canino. Ainda gerenciável
  mas claramente um tier acima do morcego peludo comum.
Nenhum dos dois itens (canino, folha negra) foi vendido com sucesso
ainda — a Guardiã elfa aceitou um canino de graça via `give` mas NÃO
pagou gold por ele (diferente de Narinë em Bri). Ainda procurando o
NPC comprador equivalente em Valfenda.


## LIÇÃO: `give <item> <NPC>` em Valfenda NÃO dá gold (diferente de Narinë em Bri!)
Testamos dar "um canino de morcego" pra Guardiã elfa E pra Vato
Nogueira — ambos aceitaram o item (sem reclamar), mas NENHUM pagou
gold. O único efeito observado: alinhamento positivo subiu de 3 para
28 pontos (bom karma, não moeda). Conclusão: não existe (ou não
achamos ainda) um NPC "colecionador universal" equivalente a Narinë
em Valfenda — doar itens aqui parece ser puramente roleplay/alinhamento.
Pra ganhar gold de verdade em Valfenda, precisamos usar `sell <item>`
numa LOJA de fato (um NPC que diga explicitamente "compro e vendo
itens", como Zurg/Narinë fazem em Bri) — ainda não testamos `sell`
com nenhum lojista de Valfenda.


## DECISÃO: voltar a Bri via pergaminho pra usar método de gold já comprovado
Navegar em Valfenda é extremamente labiríntico — o "Jardim de Imladris"
(perto do Bosquepraça) e o "Círculo Florido" (perto da Casa de Reis)
parecem ser DUAS áreas distintas da cidade, apesar da Guardiã elfa dar
instruções de rota que pareciam cruzar ambas; seguimos a rota dela ao
pé da letra dentro do Jardim de Imladris e caímos num loop entre 2
salas "Jardins: Ervas Perfumadas" sem nunca sair rumo ao Círculo
Florido real. Dado que já temos um pergaminho de retorno e método de
gold 100% comprovado em Bri (bezerro + slice + Narinë), decidimos
recitar o pergaminho pra voltar à Academia e usar esse método lá,
em vez de continuar perdidos em Valfenda. Valfenda tem MUITO ainda a
explorar (Indumentária e Fundição nunca achada, loja de equipamentos
de combate ainda desconhecida) — fica pendente para uma próxima visita
com rota melhor mapeada.


## Dicas úteis de sintaxe + item que Narinë recusa
- `give all.<item> narine` vende TODAS as cópias de um item empilhado
  numa única chamada (ex.: deu 3 fatias de carne de bezerro de uma vez,
  1 gold cada) — mais eficiente que repetir `give` item por item.
- Narinë recusa "um cabresto arrebentado" (dropado de um bezerro morto
  sem precisar de slice): "isso é uma das poucas coisas que não me
  interessam", devolvendo o item. Mais um item na lista de recusados
  por ela (junto com mapa de Bri, caroço de maçã, corpos de animais).

## Sintaxe exata pra colher/comer maçã da macieira (resolvido de vez)
`colher maçã`/`colher macieira` NÃO funcionam (erro "O que?"). A sintaxe
real é `get maçã macieira` (colhe "uma deliciosa maçã" do galho mais
baixo). Para comer, `eat maçã` é AMBÍGUO se ainda tiver "um caroço de
maçã" na mochila (o jogo prioriza o caroço, que não é comestível, e
`eat 2.maçã` também não resolve a ambiguidade do jeito esperado).
Solução confiável: `drop caroço` antes (ou `put caroço cesto`, há cestos
de lixo em várias esquinas de Bri) e só então `eat maçã` acerta a
deliciosa maçã. Vale sempre descartar o caroço de maçã do inventário
inicial assim que possível — ele nunca é útil e só causa ambiguidade.

## Vato Nogueira: paradeiro MUDA conforme última corrida (não fica fixo)
Confirmado via `help vato nogueira`: ele "normalmente espera por
clientes nas redondezas da Praça de Bri, mas também aguarda por
algumas horas próximo ao destino da sua última corrida." Como a última
corrida desta sessão foi Bri -> Valfenda, ele muito provavelmente está
parado no Bosquepraça de Valfenda agora, NÃO em Bri. Buscamos
exaustivamente em Bri nesta sessão (Praça, Avenida Zênite, Portão
Norte, toda a Grande Estrada Leste até o início da estrada rumo
Valfenda, Pônei Saltitante completo incluindo taverna/hospedaria/
estábulo/quartos) e NÃO o encontramos — consistente com essa regra.
Localização padrão dele quando "em repouso" (sem corrida recente) é
perto da Praça de Bri, especificamente a sala "A Grande Estrada Leste"
a OESTE da Praça (perto do galinheiro de Nob e da trilha de pedras que
sobe a Colina de Bri) — ver seção anterior "DESCOBERTA ENORME: Vato
Nogueira". Se ele não estiver lá, a hipótese mais provável é que esteja
no destino da última viagem (aqui, Valfenda/Bosquepraça).
Pendência atual: ou (a) seguir a pé com cautela pela Grande Estrada do
Leste até o Bosquepraça de Valfenda pra pegá-lo lá (gasta MUITO mv —
~2-4 por sala, dezenas de salas, não é viável com mv < 150 cheio), ou
(b) esperar ele voltar a Bri "em algumas horas" de jogo.

## Nova sala: "Um Pequeno Trapiche" (pescador, rio que margeia Bri)
A partir de "A Grande Estrada do Leste" (início, logo após o Portão
Sul rumo Valfenda), saída `s` leva a um pequeno trapiche de pescadores
locais. NPC "o pescador" oferece sua "coleção de canoas" e avisa pra
não esquecer o colete salva-vidas antes de entrar no rio
(`say Preciso de um colete` para pegar um). Saída `e` daqui segue o
curso do rio pra leste (não explorada ainda). Pode ser um acesso
alternativo/aquático não testado ainda — ou só flavor de pescador.

## Segundo personagem: Dorgrin (anão clérigo, Esgaroth), criado 2026-10-22
Criação: NOVO, nome, senha 2x, email em branco, sexo, raça Anao (idade
60-120, altura 100-145cm, peso 40-70kg), cidade natal, classe, Modo
Aural. Anão só pode escolher Bri, Archet ou Esgaroth (Erebor, Moria,
Ered Luin recusadas). Começa com 26hp 94 mana 100mv, casaco de algodão,
capa negra, botas anãs, Guia do Aventureiro, 0 ouro. Magias a 0%:
Armadura, Causar Dano Leve, Curar Ferimentos Leves, Missil Magico
(praticar na guilda de clérigos, Pequeno Templo do Bosque).
- POLICY 4: nunca dois personagens conectados ao mesmo tempo. QUIT
  num, depois login no outro. MAIL fica bloqueado ("até seu personagem
  ser aprovado") enquanto o nome não for aprovado; registro de alt vai
  por mudmail para os maiar (comando `maiar` lista quem são).
- A Academia é a mesma para todos, mas o `d` do saguão depende da
  cidade natal: Halbarion sai em Bri, Dorgrin sai em "À porta da
  Academia de Aventureiros" (saídas e, u), perto de Esgaroth.
- Tutorial do 2º andar é obrigatório e one-way: n e e s s w w u,
  `get chave estante`, `unlock n chave`, `open n`, n, `open tapeçaria`,
  n, e e e -> Corredor Silencioso.
- Zurg (refeitório, n n n e do saguão): `say comida` dá carne de coelho
  grátis (uma vez); ensina de graça `practice 'fatiar carne'` e
  `practice cozinhar`; vende cantil 16, cogumelo 2, carne de coelho 1,
  perdiz assada 2. O refeitório tem um grande fogão a lenha.
- Ficar parado muito tempo: "Você desapareceu no Vazio" e o servidor
  derruba a conexão. Basta reconectar.

## Comando `areas`: todas as áreas e faixas de nível
Bri 1-100, Biblioteca de Bri 1-10, Estrada Leste 10-20, Fazenda do Sr.
Magote 40-55, Floresta Velha 5-15, Floresta de Pinheiros 1-5, Vila dos
Anões 10-35, Academia 1-8, Acampamento Norte do Vale do Anduin 30-75,
Alcatéia de Rhudaur 15-25, Aldeia de Lago Comprido 10-20, Archet 1-100,
Colinas dos Túmulos 15-25, Galerias Subterrâneas 5-30, Beirágua 20-30,
Bosque Sagrado 5-20, Bosque das Folhas Verdes 5-15, Caminho para as
Montanhas Sombrias 5-15, Carrocha 10-25, Cemitério de Lago Comprido
5-30, Charneca Etten 90-100, Creche Anã 1-5, Esgaroth 0-115, Estrada de
Lago Comprido 0-100, Estrado 5-20, Fortaleza Terra-Pardense 10-70, Fosso
Branco 15-25, Guilda Arcana 50-100, Isengard 60-80, Jardim de Imladris
4-9, Lago Comprido 5-15, Limiar do Ermo 30-50, Mata dos Trolls 50-70, O
Cemitério 5-10, Rio Anduin parte 1 40-50, Templo de Andrakaus 1-100,
Bosques das Colinas do Sul 5-10, Sonhos do Bardo 10-50, Passagem Alta
10-30, Rio da Floresta 15-25, Ruínas de Framsburg 75-95, Sapântano
10-20, Sede do Brandevin 35-45, Sítio Knob 0-10, Terras Profanas 5-15,
Terras de Beorn 5-40, Topo do Vento 1-100, Trilha Élfica na Floresta das
Trevas 15-75, Vale do Mago 10-45, Valfenda 1-100, Vila dos Elfos
Jangadeiros 25-35, (PK) Refúgio Sombrio 90-100.
- Vila dos Anões (10-35): da praça de Bri, oeste até 'A Interseção',
  depois sul pelo Caminho Verde até um acesso a nordeste. Abaixo dela
  fica a Creche Anã (1-5): labirinto, bonecas com anel útil, crianças
  anãs ladras. Alcançável pelo Halbarion.

## Esgaroth (Cidade do Lago)
Entrada: Estrada do Lago, placa: S Bosque das Folhas Verdes / Ponte do
rio da Floresta / Cemitério; N Aldeia de Lago Comprido; E Grande Ponte;
W Academia. Acesso à Grande Ponte (guarda Lairebaude, tosca placa), 7
salas de ponte para leste, Bifurcação da Ponte Superior (placa), ne ne
até a Avenida Perimetral Oeste.
- Ponto de retorno: "No Centro de Esgaroth: o Coração do Mercado"
  (Brandivaus, capitão da guarda; Asilë, aprendiz de espadas).
- Água grátis: nas praças (Floresta das Trevas, Montanha Solitária,
  Flechada Precisa) `push alavanca` enche o balde, `drink balde`. Não
  levar o balde (lei da cidade, quadro no Quartel da Guarda).
- Lojas vistas: Lampadário Luz Cegante; Empório de Armaduras
  Mão-de-Ferro (Feodor) e Casa de Armas Mão-de-Ferro (Disneck), filhos
  de Tercevans; Ancoradouro Abarrotado (Alastor, merceeiro, troca
  itens por comida); Correio do Lago (Rabelais); Taverna do Rei sob a
  Montanha (Dostolieve); doceira Hannendel (doces 2-8 ouro);
  Alfarrábio Novo (Ilde): capa para livros 20, pena de escrituras 10,
  caneta-tinteiro 10, mapas de Esgaroth/Aldeia/Bosque/Cemitério 3,
  mapa das cercanias de Lago Comprido 5, livro 'Uma aventura de
  Verda...' 200, folha de papel 1.
- Praça da Flechada Precisa: monumento de Bard flechando o dragão.
  Poste: NW Viela do Herói/Travessa Sul, NE Salão da Cidade, E Viela do
  Herói, S Viela do Herói/Av. Perimetral Sul, SW Biblioteca (na verdade
  o Alfarrábio Novo), SE Casa Grande.
- Casa Grande (entrada, saídas s nw): cabideiro, poltrona vermelha de
  veludo, Narag (homem de negócios esperando o mestre da cidade),
  Florbela, Belodon (filho do senhor, vive correndo pela cidade).

## Salões de Espera (morte)
Morto vai aos Salões de Espera: Estë dá o "etéreo manto dos mortos";
Námo e Vairë presentes. Após o veredito, volta ao saguão da Academia.
Itens que não cabem ao saquear o corpo ficam no chão quando ele some.
Morte zera a fome.
- Guardas de Esgaroth (Lairebaude, Lainever, filhos de Lairemel) são
  "GPS": `look <guarda>` faz ele oferecer escolta; teclar o número
  leva você na hora: [1] Coração do Mercado (retorno), [2] Estrada do
  Lago/entrada da Grande Ponte (Academia), [3] Ancoradouro Abarrotado
  (Alastor), [4] Praça da Flechada Precisa, [5] Praça Floresta das
  Trevas, [6] Praça Montanha Solitária. Avisam que não vão ajudar
  sempre.
- Alastor (Ancoradouro Abarrotado) troca QUALQUER item por comida:
  `give <item> alastor` -> uma maçã ("pequena maçã de qualidade baixa,
  dura, azeda"). Salva personagem sem ouro. Barris de maçãs com o
  emblema de Esgaroth, destinadas aos salões de Thranduil.
- Sede/fome em "MORRENDO" quase zeram a regeneração de movimento
  (+1 por tick). Beber na bomba devolve o ritmo normal (~15 mv/tick
  descansando).
- Lojas fecham à noite: Empório de Armaduras com plaqueta "Volto em
  horário comercial!".
- Poste da Av. Perimetral Norte: Sul = Avenida Transversal (Alto do
  Mercado, Banco, Alfaiataria Agulha de Ouro, Joalheria Dedo de Prata,
  Caneca D'Ouro); Leste = Praça Floresta das Trevas, acesso aos
  Mercados Setentrional e Central; Oeste = idem, Av. Perimetral Oeste.

## Terceiro personagem: Tolmo (hobbit ladino, Bri), criado 2026-10-22
Criação: hobbit pode ter 33-66 anos, 80-120cm, 15-40kg. Cidades natais
permitidas: Bri, Archet, Esgaroth. Começa com 17hp 110 mana 200mv máx,
chapéu de couro, camisa verde, casaco preto, calça preta. Carrega no
máximo 5 itens. Nome aprovado no mesmo dia; mudmail de registro alt
enviado. Se a conexão cair no meio da criação, o servidor guarda o que
já foi respondido e retoma (com Modo Aural antes da senha).
- Estante de armaduras da Academia: bracelete, botas e cinto servem no
  nível 1; perneiras e colarinho exigem nível 3. Hobbit usa botas sem
  problema. `get all estante` só pega 4 itens de cada vez.
- Comando `exits` funciona no escuro e mostra o nome das salas vizinhas
  iluminadas (e marca portas fechadas e saídas secretas).
- `help estrado`: vila do outro lado da colina de Bri, maioria hobbit,
  engenhosos (ciências, cultivo, erva de cachimbo). Thain eleito: Rungo.
  Área de treino, nível 5-20, vizinha de Archet e da Grande Estrada.
- `help beirágua`: vila hobbit, boa para iniciantes, itens bons para
  vender; a leste, na floresta, hobgoblins agressivos. De Bri: Portão Sul,
  Grande Estrada do Leste para leste, passagem ao norte. De Archet: trilha
  pela Floresta Chet, na entrada da cidade.
- Uma hora do jogo leva uns 4-5 minutos reais. À noite as salas ao ar
  livre ficam escuras ("Está escuro ..."); as tocas continuam iluminadas.

## Estrado (vila hobbit, nível 5-20)
Rota a pé do saguão da Academia (Bri): `d n w w w s s s s s s s s e e se
e ne e ne e e se n`. A sala da estrada antes do `n` diz "Ao norte, ainda
pode-se ver algumas casas dos habitantes de Estrado". Na estrada cada
passo custa até 8mv.
- A Caminho de Estrado (s nw) -> A Caminho de Estrado (ne se) -> Uma
  Curva na Trilha (e nw sw): "Você poderia jurar que viu algo reluzindo
  na beira da estrada" — item escondido, precisa de `search` (o Tolmo
  ainda não tem).
- Um Som Distante (n e w): "Um hobbit de aparência particularmente vil
  guarda o caminho norte".
- Laboratórios ("Um Pequeno Laboratório", mesmo título, descrições
  diferentes): um barulhento com marceneiros inventores e alquimistas
  hobbit; ao lado, "Um Amontoado de Engrenagens" (engrenagem enorme de
  madeira escura com luva de metal sextavada). O laboratório silencioso
  tem "um enorme e estranho objeto" zunindo (caixa ornamental com tubos
  estriados; pela pequena porta dá para sentir algo, mas "uma busca um
  pouco mais minuciosa parece ser necessária") e uma pequena alavanca
  vermelha brilhante. NPC nomeado: inspetor Veril (hobbit arrogante que
  olha por cima dos óculos).
- `push alavanca` = CATAPULTA: "O chão se abre e você cai sentado sobre
  o braço de uma enorme catapulta... ZOOM! Você atravessa a vila
  descrevendo uma parábola em pleno ar" e cai numa cama com mola em "Uma
  Toca Bem Cuidada" (smial com mobília de qualidade, crianças hobbit com
  bumerangue). `pull alavanca`: "Isto já está desativado."
- Armazém (a oeste dos laboratórios): caixas rotuladas, uma escada de
  madeira velha ("útil para se alcançar pequenas alturas"), caixa velha
  "PREGOS" (prego sujo e enferrujado) e caixa nova "JARDINAGEM" (enorme
  tesoura de poda, "a antítese da filosofia da coisa"). Peguei a escada
  e a tesoura.
- Rua escura a oeste da Toca Bem Cuidada: N Oficina de Obras, S A Toca
  dos Cristais (fechada), W rua.
- Oficina de Obras: marceneiro de aura vermelha, "ardiloso e
  misterioso", que sempre para no mesmo lugar; CADEIRA de couro com
  rodinhas. `look arrumação`/`look chão` mostra o contorno de uma porta
  oculta; `open alçapão` abre a saída secreta `d`. Embaixo (escuro):
  sala com uma criatura e porta a leste; `open e` = "a passagem para a
  câmara do rei"; a câmara (escura, duas criaturas) tem saídas S
  (fechada) e W. Voltar: `w`, `u`.
- Sem água em Estrado: o Tolmo recitou o pergaminho de retorno (veio no kit de novato, texto:
  "Os perdidos sempre reencontram conforto no ambiente de seus lares.") e voltou ao saguão da
  Academia. Bebeu na fonte de mármore, vendeu a escada de madeira e a tesoura de poda (itens de
  Estrado) a Narinë por 1 moeda cada, comprou lamparina (2), pegou carne grátis do Zurg
  (`say comida`; ele pede para voltar em alguns minutos depois da 1ª) e dormiu nos leitos da Cura:
  movimento 46 -> 175 em menos de 1 minuto real.
- Comida em Estrado: Horta de Cebolas tem cebolas no chão (`get cebola`, `eat cebola`).
- Escada de madeira: "velha e acabada... ainda é útil para se alcançar pequenas alturas".
  Tesoura de poda: "enorme e afiada... antítese da filosofia" do jardineiro.

### Estrado: trilha Chet até Archet e salas de aula (Tolmo)
- De "A Caminho de Estrado" (a que tem saída ne/se) a saída `nw` leva a "Uma Curva na Trilha" -> `nw` "Perto de Estrado" -> 16 salas "Uma Trilha Pela Floresta Chet" (sempre duas saídas; zigue-zague n/s/se/nw) -> "Perto de Archet" (troncos cortados, Archet ao norte) -> "Uma Estrada Muito Utilizada" (n Entrada de Archet, se/sw estrada). Rota Archet -> Estrado (da Uma Estrada Muito Utilizada): `se`, depois seguir `s s s se s s se s se s s s s s s se s se` ate "Perto de Estrado"; `se` chega na Curva na Trilha. Trilha sem combate (nivel 1, noite, hp 17).
- Salas de aula (descobertas ao final da exploracao): "Uma Ampla Sala de Aula" (professor Groto Cascalva, criancas hobbit, estante de carvalho, pintura do centro da vila com a estatua de granito segurando uma placa) e "Uma Pequena Sala de Aula" (professora Petula Cascalva, mesa com quebra-cabecas, brinquedos; ensina filosofia). Saidas w / e entre elas.
- Dormir em qualquer sala fechada regenera mv rapido se alimentado.
- Fome volta rapido para hobbit de nivel 1 (cebolas nao saciam por muito tempo).

### Estrado: subsolo dos hobgoblins e casas (Tolmo, nível 1)
- Do Beco sem Saída (n = Oficina de Obras, e = Uma Toca Bem Cuidada, s = A Toca dos Cristais, w = Curva na Estrada): na Oficina `look chão` mostra um contorno de porta oculta, `open alçapão`, `d`.
- "A Sala do Tesouro" (hobgoblins): tesoureiro hobgoblin velho de óculos contando dinheiro (não ataca, "parece um pouco mais forte" que o Tolmo nv1); mesa com anotações coberta de terra ("como se alguém tivesse subido sobre a mesa"; a terra treme por experiências mal sucedidas); `open e` abre a passagem para a câmara do rei. Há luz sem lamparina.
- "A Câmara do Rei": carcaças e peles frescas nas paredes, tochas, trono de granito bruto com caveiras entalhadas e musgo; o rei dos hobgoblins (insano, músculos rasgando as roupas, "um pouco mais forte") e 2 guarda-costas hobgoblin de elite, todos com Aura Vermelha. Não atacaram quem entrou e saiu. Saídas: w (volta) e s fechada.
- Casas ("smials") a oeste da Curva na Estrada, sul e oeste com porta fechada (`open s`, `open w`): "Uma Toca Suja" (mulher hobbit, casaco resistente de tecido negro no chão) e "Um Lar Mal Cuidado" (cama, cadeira, armários vazios, nenhuma criança). "A Toca dos Cristais": mulher hobbit e mesas com engrenagens, junções e molas.
- Placa da estátua de granito: "Nossos Heróis Caídos", nomes de hobbits mortos em batalha ou trabalhando; a maior honra de um hobbit é morrer jovem exercendo sua função.

## Beirágua (nível 20-30) - help
- Vila de tocas enfileiradas na margem norte do lago, jardins, Dragão Verde, perto da Colina de Bolsão. Mestre de perícias e magias: Celussë, a mestra da água. Atração: bons itens para hobbits.
- Dica: cuidado para não se perder nas plantações; "você veio do norte".
- Rota de Bri: portão oeste, Bosques das Colinas do Sul, Grande Estrada do Leste, ponte do rio Brandevin, depois oeste até a área (atenção às placas). De Archet: trilha sudoeste da entrada, sul pela Velha Estrada do Norte até A Interseção, de lá pelos bosques. Beirágua é a vila após Sapântano (help 'sapântano').

### Tolmo: morte no caminho para Beirágua (nível 1, 17 hp)
- Rota percorrida: Portão Oeste de Bri, `w` x4 até A Interseção, depois Grande Estrada do Leste a oeste: 3 salas "A Grande Estrada do Leste", bifurcação n s nw se com um grande cogumelo ("topo coberto com substância de cheiro de mofo"), depois cruzamento de três trilhas (n, e, w; a estrada segue sudeste-noroeste). Pela entrada `w` desse bifurcação há "Uma Pequena e Escura Trilha no Bosque" (saídas e s) fora da estrada.
- help "Bosques das Colinas do Sul" (nível 5-10; vizinhas Bri, Floresta Velha, Colina dos Túmulos, Sede do Brandevin, Fosso Branco): wargs agressivos, ninhada de aranhas assassinas, figuras que saem de Chet/Floresta Velha à noite; "evite sair da trilha da Grande Estrada do Leste"; choupana de John, o lenhador (mapa do local) e refúgio do Druida; Onae, o Guardião, procura Lothab, perdido na Floresta Velha.
- Um warg furioso atacou o Tolmo ao andar a noroeste no cruzamento: golpes "MASSACROU" tiraram 16 de 17 hp em poucos segundos, `flee` não adiantou (1 hp -> morte). Morte nº 1 do Tolmo, XP 0.
- Salões de Espera de novo: ao chegar, `stand`; arco ao norte: corredor com Estë, depois a sala circular com Námo e Vairë, que dizem que o veredicto "não será rápido" (aguardar). Andar nessa sala gasta movimento (168 -> 99).
- Lição: nível 1 não atravessa os Bosques das Colinas do Sul nem à noite nem de dia; para documentar Beirágua/Sapântano/Fosso Branco é preciso nível 5+ ou escolta. Hobbit 17 hp morre em 2 golpes de warg.

### Tolmo: fechamento de Estrado e achados em Bri
- Estrado: com `sneak` (Furtividade 100% de início para Ladino) o Tolmo passa por Um Som Distante e vai a `n` Saliências no Solo -> O Fim do Caminho sem os guardas hobbit atacarem; o mapa inteiro (45 salas) foi percorrido e todas as saídas testadas. O `n` "guardado" é o mesmo trecho dos escritórios do Thain; não há área nova além dele.
- Itens escondidos de Estrado (brilho na Curva na Trilha, objeto que zumbe no laboratório silencioso, itens perdidos no curral/estábulo) exigem a perícia `search`, que o Tolmo não tem (Prática: 0; Domick ensina no corredor 1 da Academia depois de subir de nível). Ficam sem exame.
- Perícias iniciais do Tolmo (Ladino nv1): Esconder 100%, Furtividade 100%, Língua Comum 100%; Apunhalar, Furtar, Escalar, Jogada de Morte etc. a 0%. `look <objeto>` de coisas inexistentes responde "Você não vê isto aqui".
- A Casa-Mathom (Bri, porta leste para a Grande Estrada Leste, depósito hobbit de "possível uso futuro"): no chão há um cantil de aventureiro (cheio), uma flor dourada (brilha, "energia renovadora", segurável), um cachimbo caído, um grande artefato (narguilé de vidro para fumar em grupo), brincos de pérolas (obra do ourives Fonstipéll, "o melhor e único de Esgaroth") e um "portal extradimensional" (contêiner de capacidade gigantesca, vazio) que dá para guardar itens. Todos podem ser pegos, exceto o portal.

### Estrado com o Halbarion (nível 6, Procurar 29%)
- `search` é uma ação cronometrada (~10 s): digite uma vez e espere o resultado ("Você não encontrou nada." ou um achado); mandar outro `search` antes interrompe ("Você para sua busca..."). `search <alvo>` responde "Você não pode procurar nisto!".
- Laboratório silencioso (e de Saliências no Solo; saídas e w; o objeto zune, escorado na parede sul): `look porta` pede "uma busca um pouco mais minuciosa"; `search` repetido (11 tentativas) revelou "uma alavanca dentro do objeto" (pequena, de material vermelho brilhante). `push alavanca` agora responde "Isto já está ativado."
- Sem achado após 20+ tentativas na Curva na Trilha (o brilho na beira da estrada) e 14 no Curral; a Entrada do Curral e a Estrada do Estábulo (12 tentativas) também vazias. Provável que sejam só ambientação ou exijam perícia maior.
- Sem cantil o Halbarion fica sem água em Estrado (sem fonte); fome pega rápido ao ficar tentando `search` (MORRENDO DE FOME em ~5 minutos). Cebolas do chão da Horta de Cebolas resolvem.
- Buscas finais em Estrado (Halbarion): Abrigo para os Animais 10 tentativas e Cocheira 10 tentativas, sem achado (O Estábulo e O Curral também sem achado). Com isso todas as salas de Estrado têm busca registrada; o único achado oculto foi a alavanca do laboratório silencioso.
