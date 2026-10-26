"""Checagem rápida do cliente: python3 cliente/test_cliente.py (ou pytest)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import completar  # noqa: E402
import conversa  # noqa: E402
import conexao  # noqa: E402
import logo  # noqa: E402
import mapa  # noqa: E402
import mochila  # noqa: E402
import painel  # noqa: E402
import vigia  # noqa: E402
from conexao import telnet  # noqa: E402
import valinor  # noqa: E402
from valinor import COMMANDS, wrap  # noqa: E402

# trecho real do raw.log (latin1 já decodificado, IAC tirado): prompt, sala no formato do SMAUG, prompt
SCARI = ("<84hp 100m 161mv> Estrada Scari\r\nQuase na metade do caminho entre Fosso Branco e o Água, mais perto do "
         "primeiro\n\rque do segundo. Enquanto Fosso Branco está ao sul, o Rio Água, que essa estrada\n\ratravessa no "
         "Vau Budge - que é também o nome da vila localizada ali -, fica um\n\rpouco mais longe ao norte.\n\r"
         "Saídas: sw\r\n\r\n<84hp 100m 161mv> ")


def test_telnet_partido_entre_pacotes():
    data, echo, rest = telnet(b"Senha: \xff\xfb")
    assert (data, echo, rest) == (b"Senha: ", None, b"\xff\xfb")
    data, echo, rest = telnet(rest + b"\x01ok\xff\xfd\x18")
    assert (data, echo, rest) == (b"ok", True, b"")
    assert telnet(b"\xff\xfc\x01x")[:2] == (b"x", False)


def test_wrap_no_espaco():
    line = [("abc def ", 1), ("ghi", 2)]
    assert ["".join(t for t, _ in r) for r in wrap(line, 7)] == ["abc def", "ghi"]


def test_sala_mapa_rota():
    base = mapa.Base()
    seen = mapa.last_room(SCARI)
    assert seen["title"] == "Estrada Scari"
    rid = base.identify(seen["title"], seen["description"], {"sw"})
    assert rid == "room:fosso-branco.estrada-scari-5"
    assert base.identify("Estrada Scari", "texto que mudou", {"sw"}, "room:fosso-branco.estrada-scari-4", "ne") == rid
    grid, cells = base.minimap(rid, 20, 9)
    cy, cx = 4, 9  # centro: célula (2, 2) da grade 5x5
    assert "".join(ch for ch, _ in grid[cy][cx - 1:cx + 2]) == "[@]"
    assert grid[cy + 1][cx - 2] == ("╱", "link")  # sw até a estrada-scari-4
    assert cells[(cy, cx - 1)] == cells[(cy, cx + 1)] == rid  # clique em qualquer célula do [@]
    assert cells[(cy + 2, cx - 4)] == "room:fosso-branco.estrada-scari-4"
    peek_grid, _ = base.minimap(rid, 20, 9, peek=frozenset(["room:fosso-branco.estrada-scari-4"]), here="")
    assert peek_grid[cy + 2][cx - 5] == ("[", "peek") and peek_grid[cy][cx] == (" ", "room")  # sem @ fora de você
    dest, path = base.nearest(rid, "taverna rama verde")
    assert base.rooms[dest]["title"] == "Taverna Rama Verde" and path[0][0] == "sw"
    assert mapa.speedwalk(["n", "n", "e"]) == "2n e"


def test_personagens_do_credenciais(tmp_path=None):
    import tempfile
    f = Path(tmp_path or tempfile.mkdtemp()) / "cred"
    f.write_text("Personagem: Aaa\nSenha: x\nPersonagemHobbit: Bbb\nSenhaHobbit: y\nPersonagemSemSenha: Ccc\n")
    conexao.CRED = f
    assert conexao.load_chars() == [("Aaa", "humano guerreiro · Bri", ""), ("Bbb", "hobbit ladino · Bri", "Hobbit")]
    assert (conexao.secret("Senha"), conexao.secret("SenhaHobbit"), conexao.secret("SenhaAnao")) == ("x", "y", "")
    assert conexao.secrets() == ["x", "y"]


def test_autocomplete_sem_senha(tmp_path=None):
    import tempfile
    t = Path(tmp_path or tempfile.mkdtemp()) / "transcript.log"
    t.write_text("Personagem: \n>>> [10:00:00] Fulano\nSenha (esqueceu? digite ESQUECI): \n>>> [10:00:01] velhasenha\n"
                 ">>> [10:00:02] look\n>>> [10:00:03] kill goblin\n>>> [10:00:04] say minha senha é segredo1\n"
                 ">>> [10:00:05] email fulano@exemplo.com\n>>> [10:00:06] kill guarda\n")
    c = completar.Completer(mapa.Base(), t, ["segredo1"])
    every = list(c.recent) + list(c.first) + list(c.args)
    assert not any("velhasenha" in x or "segredo1" in x or "@" in x for x in every)
    assert c.ghost("ki") == "ll guarda" and c.ghost("k") == ""  # o mais recente primeiro
    assert ("kill", "2×") in c.words("ki", True, [], [])
    assert c.words("go", False, ["guarda"], ["goblin"])[0] == ("goblin", "na tela")
    assert c.complete("/ro", [], [], COMMANDS) == (0, [("/rota", COMMANDS["/rota"])])
    start, pop = c.complete("/rota taver rama", [], [], COMMANDS)
    assert start == 6 and pop[0][0] == "Taverna Rama Verde"
    c.learn("kill rato")
    assert c.ghost("kill ") == "rato"
    assert completar.text_words(["O guarda está aqui.", "Um guarda velho"]) == ["guarda", "velho"]


def test_pedido_de_senha_sem_eco():
    assert valinor.ASKS_PW.search("Senha (esqueceu? digite ESQUECI): ")
    assert not valinor.ASKS_PW.search("O guarda diz: a senha é segredo.")


def test_prompt_colorido():
    # prompt real do Tolmo, que joga com cores (sem o Modo Aural)
    cor = "\x1b[m<\x1b[m\x1b[1;33m17hp \x1b[36m110m \x1b[32m100mv\x1b[m\x1b[m> \x1b[0;1;36mAs Regras do Jogo"
    assert valinor.PROMPT.search(cor).groups() == ("17", "110", "100")
    assert valinor.PROMPT.search("<84hp 100m 191mv> ").groups() == ("84", "100", "191")
    assert valinor.HOLD.search("texto\n<\x1b[m\x1b[1;33m17hp \x1b[36m11")


def test_barrinha():
    assert painel.bar(84, 84) == ("━" * 8, "")
    assert painel.bar(42, 84) == ("━" * 4, "─" * 4)
    assert painel.bar(48, 84) == ("━" * 4 + "╸", "─" * 3)
    assert painel.bar(-5, 84) == ("", "─" * 8)  # morrendo: hp negativo
    assert painel.bar(30, 250) == ("━", "─" * 7)
    assert painel.bar(1, 250) == ("╸", "─" * 7)
    assert painel.bar(83, 84) == ("━" * 7 + "╸", "")


def test_maximo_do_score():
    cor = "Carisma:        13/13       Vida:             8/17 [>>>>------]\r\n Movimento:     110/200 [>>>>>-----]"
    aural = "Vida: 84 de 84.\r\nMana: 100 de 100.\r\nMovimento: 0 de 250."
    assert [m.groups() for m in valinor.MAXES.finditer(cor)] == [("Vida", "17"), ("Movimento", "200")]
    assert [m[2] for m in valinor.MAXES.finditer(aural)] == ["84", "100", "250"]


def test_logo_da_abertura():
    art = logo.load()
    cs = logo.cells(art)
    assert art and max(map(len, art)) <= logo.COLS
    assert sum(tone == "star" for *_, tone in cs) == 7  # Valacirca
    assert "".join(c for _, _, c, tone in cs if tone == "tag") == logo.TAGLINE.replace(" ", "")
    assert {"ring", "title"} <= {tone for *_, tone in cs}
    escuro = logo.frame(cs, 0)  # abre no escuro e acende
    assert {logo.xterm(rgb) for *_, rgb, _ in escuro} == {logo.xterm(logo.DARK)}
    a, b = logo.frame(cs, 1.0), logo.frame(cs, 1.5)
    assert [c[:2] for c in a] == [c[:2] for c in b] and [c[3] for c in a] != [c[3] for c in b]  # mesmas células, brilho anda
    assert {c for _, _, c, _, tone in a + b if tone == "star"} <= set(logo.TWINKLE)
    assert logo.xterm((255, 255, 255)) == 231 and logo.xterm((128, 128, 128)) == 244


class Andador(painel.Painel):
    def __init__(self, room: str, goal: str) -> None:
        self.base, self.room, self.live, self.sock, self.ingame = mapa.Base(), room, None, True, True
        self.route = self.base.route(room, lambda r: r == goal)
        self.sent, self.msgs = [], []

    def send(self, cmd: str) -> None:
        self.sent.append(cmd)

    def say(self, text: str, style: str = "") -> None:
        self.msgs.append(text)


def test_andar_manda_a_rota_e_para_na_porta():
    a = Andador("room:fosso-branco.estrada-scari-5", "room:fosso-branco.atravessando-fosso-branco")
    a.cmd_andar()
    assert a.sent == [d for d, _ in a.route] and a.sent and not a.msgs
    porta = Andador("room:academia.a-sala-da-preparacao", "room:academia.a-sala-da-atencao")  # u, depois !n
    porta.cmd_andar()
    assert porta.sent == ["u", "open n", "n"] and not porta.msgs  # a porta era o último passo
    volta = Andador("room:academia.a-sala-da-atencao", "room:academia.a-sala-da-preparacao")  # !s, depois d
    volta.cmd_andar()
    assert volta.sent == ["open s", "s"] and "porta s" in volta.msgs[0]  # para do outro lado da porta


def test_direcao_digitada_abre_a_porta_fechada():
    a = Andador("room:academia.a-sala-da-atencao", "room:academia.a-sala-da-atencao")
    a.live, a.last_sent = {"exits": ["e u !n"]}, ""
    a.door_ahead("norte")
    a.door_ahead("e")
    assert a.sent == ["open n"]
    a.last_sent = "open n"  # você já abriu: não manda de novo
    a.door_ahead("n")
    a.live = None  # sem as Saídas do servidor não adivinha
    a.door_ahead("n")
    assert a.sent == ["open n"]


def test_duplo_clique_traca_e_anda():
    from collections import defaultdict
    goal = "room:fosso-branco.atravessando-fosso-branco"
    a = Andador("room:fosso-branco.estrada-scari-5", goal)
    dirs, a.route, a.target = [d for d, _ in a.route], [], None
    a.hits, a.hover, a.scroll, a.th, a.push = {(3, 4): goal}, None, 0, defaultdict(int), lambda line: None
    a.spots, a.spot_hover = {}, None
    events = iter([(0, 4, 3, True), (0, 4, 3, False), (0, 4, 3, True)])  # aperta, solta, aperta: (b, x, y, press)
    a.read_mouse = lambda: next(events)
    a.on_mouse()
    a.on_mouse()
    assert a.target == goal and a.sent == []  # clique simples só traça
    a.on_mouse()
    assert a.sent == dirs


# eq e inv no formato do servidor (do transcript): o cabeçalho às vezes vem colado no prompt
EQ_INV = ("<84hp 100m 199mv> Você está usando:\n<como luz>        (Brilhando) uma lamparina\n"
          "<no corpo>        uma camisa marrom\n<no pulso>        um bracelete\n<empunhando>      uma espada metálica\n"
          "\n<84hp 100m 199mv> \nVocê está carregando:\n     (2x) um pão bem recheado para viagem\n"
          "     (Queimado) um pergaminho de retorno\n\n<84hp 100m 199mv> ")


def test_mochila_le_eq_inv_e_score():
    got = mochila.scan(EQ_INV)
    assert got["equip"][0] == ("como luz", 1, ("Brilhando",), "uma lamparina") and len(got["equip"]) == 4
    assert got["inv"] == [(2, (), "um pão bem recheado para viagem"), (1, ("Queimado",), "um pergaminho de retorno")]
    assert mochila.scan("Você está carregando:\n     Nada.\n\n<1hp 1m 1mv> ")["inv"] == []
    assert mochila.scan("Você está usando:\nNada.\n\n<1hp 1m 1mv> ")["equip"] == []
    aural = ("Carregando 4 itens de um máximo de 5.\nCarregando 13 kg de um máximo de 100 kg.\n"
             "Glória: 0, Peso: 44.6 kg, Estilo: padrão, Ouro: 5")
    assert mochila.scan(aural) == {"items": (4, 5), "kg": (13, 100), "gold": 5}
    assert mochila.scan("Itens:            2/5\nCarreg.:      9/44 kg\nOuro:                      0 moedas") == \
        {"items": (2, 5), "kg": (9, 44), "gold": 0}
    labels = ("nos pés", "no pulso", "como luz", "nas costas", "sobre o corpo", "no corpo", "nas mãos", "na cabeça")
    assert [mochila.spot(lb) for lb in labels] == ["pés", "pulsos", "como luz", "costas", "sobre o corpo", "corpo",
                                                   "mãos", "cabeça"]


def test_mochila_cruza_com_a_base():
    idx = mochila.index(mapa.Base())
    e = idx[mapa.fold("uma espada metálica")]
    assert mochila.price(e) == 101 and e["weight"] == "cerca de 1 kg"
    assert idx[mapa.fold("a mochila dos aventureiros de Halbarion")]["capacity"] == "Gigantesca"
    assert idx[mapa.fold("uma deliciosa maçã")]["category"] in mochila.KIND
    assert mochila.price(None) is None



# who e conversa nos formatos do servidor, com nomes inventados
WHO_TABELA = ("[ Nív Raç Cla ]  Nome                               [ Status ]\n"
              "[   6 Hum Gue ]  Fulano de Bri, o Recruta           [ DESCONECTADO ]\n"
              "[  25 Mei Ran ]  Beltrano, o Rastreador\n"
              "[     Mai Mag ]  Sicrano de Valinor\n"
              "[   3 personagens encontrados   ]\n")
WHO_AURAL = ("Todos os personagens online.\nBeltrano de Imladris, o Rastreador, Meio-elfo, Ranger nível 25\n"
             "Fulano de Bri, o Recruta, Humano, Guerreiro nível 6, NÃO AUTORIZADO\n2 personagens encontrados.\n")


def test_who_nos_dois_formatos():
    assert conversa.who_scan(WHO_TABELA) == [("Fulano", "6", "Hum", "Gue", "DESCONECTADO"),
                                             ("Beltrano", "25", "Mei", "Ran", ""), ("Sicrano", "", "Mai", "Mag", "")]
    assert conversa.who_scan(WHO_AURAL) == [("Beltrano", "25", "Mei", "Ran", ""),
                                            ("Fulano", "6", "Hum", "Gue", "NÃO AUTORIZADO")]
    assert conversa.who_scan("Sem ninguém por aqui.") is None


def test_chat_vai_para_a_aba_certa():
    assert conversa.chat_of("(OOC) Você disse 'boa noite'") == ("global", "você", "boa noite")
    assert conversa.chat_of("(OOC) Beltrano perguntou 'alguém vem?'") == ("global", "Beltrano", "alguém vem?")
    assert conversa.chat_of("(OOC) [OSAY] Beltrano disse 'oi'") == ("global", "Beltrano (sala)", "oi")
    assert conversa.chat_of("(OOC) Beltrano disse telepaticamente 'vem pra Bri'") == ("Beltrano", "Beltrano", "vem pra Bri")
    assert conversa.chat_of("(OOC) Você disse telepaticamente para Beltrano 'indo'") == ("Beltrano", "você", "indo")
    assert conversa.chat_of("Beltrano sussurrou para você 'psiu'") == ("Beltrano", "Beltrano", "psiu")
    assert conversa.chat_of("O guarda sussurrou para você 'cuidado'") is None  # NPC não ganha aba
    assert conversa.chat_of("Beltrano diz 'olá'") is None  # fala na sala fica só no Jogo


class Papo(conversa.Conversa):
    def __init__(self) -> None:
        from collections import defaultdict
        self.th, self.scroll, self.dirty, self.char, self.inp = defaultdict(int), 0, False, "Fulano", ""
        self.sock = self.ingame = True
        self.sent, self.lines, self.partial = [], [], []
        self.talk_init()

    def send(self, cmd: str) -> None:
        self.sent.append(cmd)

    def say(self, text: str, style: str = "") -> None:
        pass


def test_abas_de_conversa_e_clique_no_who():
    p = Papo()
    p.who_seen(WHO_TABELA)
    assert [w[0] for w in p.who] == ["Fulano", "Beltrano", "Sicrano"] and p.sent == []  # ler o who não manda nada
    p.spot_click(("who", "Beltrano"))
    assert p.chan == "beltrano" and p.chan_label() == "tell Beltrano" and p.sent == []  # clicar só abre a aba
    p.spot_click(("who", "Fulano"))
    assert p.chan == "beltrano"  # você mesmo não vira aba
    p.talk_send("indo pra Bri")
    p.set_chan("global")
    p.talk_send("boa noite")
    p.talk_send("   ")
    assert p.sent == ["tell Beltrano indo pra Bri", "chat boa noite"]
    p.talk_seen("(OOC) Beltrano disse telepaticamente 'ok'")
    assert p.talk["beltrano"]["unread"] == 1 and p.talk["global"]["unread"] == 0
    p.next_chan()
    assert p.chan == "beltrano" and p.talk["beltrano"]["unread"] == 0
    assert p.view()[0][-1][1][0] == "Beltrano"
    p.close_tab("beltrano")
    assert p.chan is None and "beltrano" not in p.talk and p.view() == (p.lines, p.partial)
    p.spot_click(("who-refresh", None))
    assert p.sent[-1] == "who"  # o ↻ é o seu clique


class Parado(vigia.Vigia):
    def __init__(self) -> None:
        self.ingame, self.dirty, self.msgs = True, False, []
        self.idle_reset()

    def say(self, text: str, style: str = "") -> None:
        self.msgs.append(text)


def test_aviso_antes_do_vazio_sem_mandar_nada():
    vigia.notify = lambda text: None  # sem notificação na área de trabalho durante o teste
    a = Parado()
    a.idle_tick()
    assert a.idle_label() is None and not a.msgs
    a.typed_at -= vigia.WARN + 1
    a.idle_tick()
    a.idle_tick()
    assert len(a.msgs) == 1 and a.idle_label() == ("◷ parado 6 min · Vazio em ~4 min", "new")
    a.idle_seen("<84hp 100m 5mv> \nVocê desapareceu no Vazio.\nVocê está MORRENDO DE FOME!\n")
    assert len(a.msgs) == 2 and a.idle_label() == ("◷ no Vazio · quit em ~5 min", "bad")
    a.idle_reset()  # você digitou
    assert a.idle_label() is None


def test_keepalive_tcp():
    import socket
    srv = socket.create_server(("127.0.0.1", 0))
    c = socket.create_connection(srv.getsockname())
    vigia.keepalive(c)
    assert c.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE) == 1
    assert c.getsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE) == 60
    c.close()
    srv.close()

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
