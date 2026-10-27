"""Modo leitor de tela (`valinor --leitor`, e sozinho quando o cliente acha um leitor de tela ligado): o jogo em texto
corrido, como num telnet, sem painel, moldura, barra ou símbolo. O texto do servidor sai na ordem em que chega e sem
cores, e cada linha digitada vai para o jogo: o leitor de tela lê o que chega e o cursor fica sempre no fim.

Feito para ouvir: o prompt só é lido quando vida, mana ou movimento mudam (/prompt troca), linhas em branco seguidas
viram uma e tell, chat ou sussurro de outra pessoa toca o sino. Os comandos do cliente começam com / (/ajuda lista):
reler as últimas linhas ou conversas, ler o prompt, a sala atual pela base, a rota por extenso e o /andar.
Ficam o seletor com login automático, os logs, o keepalive TCP e o aviso antes do Vazio. Nada é mandado sozinho além do
login do personagem escolhido: o /andar e o open da porta fechada saem do seu Enter, como no cliente com painéis."""
from __future__ import annotations

import getpass
import re
import socket
import subprocess
import sys
import threading
import time
from collections import deque
from itertools import groupby
from pathlib import Path

import mapa
from conexao import (ANSI, ASKS_PW, LOGS, STD_PROMPT, WIN, load_chars, other_connections, secret, shape, telnet,
                     vitals)
from conversa import chat_of
from painel import MAX_WALK, NOWHERE, steps
from vigia import WARN, keepalive

try:
    import readline  # noqa: F401  setas, edição e histórico no input() (Linux e macOS)
except ImportError:
    pass

WAIT = 1.0  # segundos esperando a resposta antes de abrir a próxima linha: se for o pedido de senha, ela vem escondida
REREAD = 10  # linhas que /rever e /conversas releem sem número
NAMES = {"n": "norte", "s": "sul", "e": "leste", "w": "oeste", "ne": "nordeste", "nw": "noroeste", "se": "sudeste",
         "sw": "sudoeste", "u": "cima", "d": "baixo"}
READERS = "orca|fenrir|tdsr|VoiceOver"  # nome do processo: Orca, Fenrir e TDSR no Linux, VoiceOver no macOS
COMMANDS = {
    "/ajuda": "esta lista",
    "/rever": f"/rever número: relê as últimas linhas do jogo, {REREAD} sem número",
    "/conversas": f"/conversas número: relê os últimos tells, chats e sussurros, {REREAD} sem número",
    "/status": "lê o prompt agora, mesmo sem mudança",
    "/prompt": "troca entre ler o prompt sempre ou só quando vida, mana ou movimento mudam",
    "/som": "liga ou desliga o sino de tell, chat e sussurro",
    "/sala": "/sala nome: o que a base sabe da sala, a atual sem nome: região, descrição, saídas e o que tem nela",
    "/rota": "/rota sala ou região: o caminho mais curto, por extenso; /rota sozinho apaga",
    "/andar": f"manda a rota de uma vez, até {MAX_WALK} passos; abre a porta do caminho e para depois dela",
    "/busca": "/busca texto: salas, NPCs, criaturas, itens e objetos da base",
}


def clean(text: str) -> str:
    """Texto do servidor para o leitor de tela: sem cores, sem \\r e sem tabulação."""
    return ANSI.sub("", text).replace("\r", "").replace("\t", "    ")


def spoken(dirs: list[str]) -> str:
    """Rota para ouvir: '2 norte, leste' no lugar de '2n e'."""
    return ", ".join(f"{n} {NAMES[d]}" if n > 1 else NAMES[d] for d, n in ((d, len(list(g))) for d, g in groupby(dirs)))


def screen_reader() -> bool:
    """Leitor de tela ligado agora. No Windows, o aviso do sistema que NVDA, JAWS e Narrador ligam
    (SPI_GETSCREENREADER); no Linux e no macOS, o processo do leitor ou o Speakup carregado no kernel."""
    if WIN:
        import ctypes
        on = ctypes.c_int(0)
        return bool(ctypes.windll.user32.SystemParametersInfoW(0x46, 0, ctypes.byref(on), 0) and on.value)
    if Path("/sys/module/speakup").exists():
        return True
    try:
        return subprocess.run(["pgrep", "-x", READERS], capture_output=True).returncode == 0
    except OSError:
        return False


class Leitor:
    def __init__(self, host: str, port: int) -> None:
        self.host, self.port = host, port
        self.sock: socket.socket | None = None
        self.lock, self.got = threading.Lock(), threading.Event()
        self.login, self.typed_at, self.warned = None, time.time(), False
        self.base = mapa.Base()
        self.lines: deque = deque(maxlen=500)  # o que o jogo escreveu, para o /rever
        self.talk: deque = deque(maxlen=200)
        self.every, self.bell = False, True  # prompt lido sempre? sino nas conversas?
        self.reset()
        LOGS.mkdir(parents=True, exist_ok=True)
        self.raw = open(LOGS / "raw.log", "ab")
        self.tr = open(LOGS / "transcript.log", "a", encoding="utf-8")

    def reset(self) -> None:
        """Estado de uma conexão: prompt aprendido, sala, rota."""
        self.masked, self.tail, self.part, self.roomtxt, self.nl = False, "", "", "", 2
        self.prompt_re: re.Pattern | None = None
        self.prompt, self.heard = "", None
        self.room = self.live = self.moved = self.target = self.arrived = None
        self.route: list = []
        self.last_sent = ""

    def say(self, text: str) -> None:
        print(f"\nCliente: {text}", flush=True)
        self.nl = 1

    def log(self, text: str) -> None:
        with self.lock:
            self.tr.write(text)
            self.tr.flush()

    def pick(self) -> None:
        opts = load_chars() + [("Outro", "nome e senha digitados na mão", None)]
        print("Escolha o personagem:")
        for i, (name, desc, _) in enumerate(opts, 1):
            print(f"{i}. {name}" + (f", {desc.replace(' · ', ', ')}" if desc else ""))
        while True:
            got = input("Número e Enter: ").strip()
            if not (got.isdigit() and 1 <= int(got) <= len(opts)):
                print(f"Digite um número de 1 a {len(opts)}.")
                continue
            others = other_connections()
            if not others or input(f"Já há outra conexão aberta ({', '.join(others)}) e o Valinor não deixa dois "
                                   "personagens ao mesmo tempo. Entrar mesmo assim? s ou n: ").strip().lower() == "s":
                break
        name, _, suf = opts[int(got) - 1]
        self.login = {"name": name, "suf": suf, "step": 0} if suf is not None else None
        print(f"Entrando com {name}." if suf is not None else "Digite o nome e a senha quando o jogo pedir.")

    def connect(self) -> None:
        print(f"Conectando a {self.host}, porta {self.port}.", flush=True)
        try:
            sock = socket.create_connection((self.host, self.port), timeout=10)
        except OSError as e:
            return self.say(f"não conectou: {e}")
        sock.settimeout(5)  # o laço de leitura acorda de vez em quando para olhar o tempo parado
        keepalive(sock)
        self.reset()
        self.sock, self.typed_at, self.warned = sock, time.time(), False
        self.got.clear()
        self.log(f"=== NOVA CONEXÃO {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        threading.Thread(target=self.read, args=(sock,), daemon=True).start()

    def read(self, sock: socket.socket) -> None:
        buf = b""
        while True:
            try:
                raw = sock.recv(65536)
            except socket.timeout:
                self.idle()
                continue
            except OSError:
                raw = b""
            if not raw:
                break
            self.raw.write(raw)
            self.raw.flush()
            data, echo, buf = telnet(buf + raw)
            if echo is not None:
                self.masked = echo
            self.take(data.decode("latin1"))
        sock.close()
        self.sock, self.masked = None, False
        self.say("conexão encerrada. Enter escolhe o personagem de novo, Ctrl+D fecha o cliente.")
        self.got.set()

    def take(self, data: str) -> None:
        """Um pedaço do servidor: log, sala, tela e login."""
        text = clean(data)
        self.log(text)
        self.tail = (self.tail + text)[-400:]
        self.track(ANSI.sub("", data))
        self.show(text)
        if self.arrived:  # depois da sala, não antes
            self.say(f"chegou em {self.arrived}.")
            self.arrived = None
        self.autologin()
        self.got.set()

    # ------------------------------------------------------------------ o que chega
    def track(self, plain: str) -> None:
        """Junta o texto (com \\r, como o parser da base quer) até o prompt e, se veio uma sala, acha ela na base. O
        prompt é a linha sem quebra no fim com hp, m e mv: o molde dele também serve para calar o repetido."""
        self.roomtxt = (self.roomtxt + plain)[-30000:]
        cut = self.roomtxt.rfind("\n") + 1
        tail = self.roomtxt[cut:].strip()
        if self.masked or len(tail) > 160 or not vitals(tail):
            return
        self.prompt_re = shape(tail)
        done, self.roomtxt = self.prompt_re.sub(STD_PROMPT, self.roomtxt), self.roomtxt[cut:]  # o título vem nela
        seen = mapa.last_room(done) if "Saídas:" in done else None
        if not seen:
            return
        exits = {e.lstrip("!") for e in next(iter(seen["exits"]), "").split()}
        self.room = self.base.identify(seen["title"], seen["description"], exits, self.room, self.moved)
        self.live, self.moved = seen, None
        self.reroute()

    def mute(self, m: re.Match) -> str:
        """Prompt com a mesma vida, mana e movimento do último lido sai calado (a não ser no /prompt sempre)."""
        v, self.prompt = vitals(m[0]), m[0].strip()
        keep, self.heard = self.every or v != self.heard, v
        return m[0] if keep else ""

    def show(self, text: str) -> None:
        """Escreve o que chegou sem o prompt repetido e com uma linha em branco no máximo; guarda as linhas para o
        /rever e as conversas para o /conversas, e toca o sino quando outra pessoa fala com você."""
        done = (self.part + text).split("\n")
        self.part, ring = done.pop()[-400:], False
        for line in done:
            line = (self.prompt_re.sub("", line) if self.prompt_re else line).strip()
            if not line or vitals(line):
                continue
            self.lines.append(line)
            talk = chat_of(line)
            if talk:
                self.talk.append(line)
                ring = ring or talk[1] != "você"
        out = re.sub(r" +\n", "\n", "\n".join(self.prompt_re.sub(self.mute, p) if self.prompt_re else p
                                              for p in text.split("\n")))
        lead = "\n" * self.nl
        both = re.sub(r"\n{3,}", "\n\n", lead + out)
        if both != lead:
            self.nl = min(2, len(both) - len(both.rstrip("\n")))
        sys.stdout.write(both[len(lead):] + ("\a" if ring and self.bell else ""))
        sys.stdout.flush()

    def autologin(self) -> None:
        """Nome, senha e o Enter da tela de novidades, uma vez só, quando o servidor pede cada um."""
        lg, last = self.login, self.tail.rsplit("\n", 1)[-1]
        if not lg:
            return
        if lg["step"] == 0 and last.rstrip().endswith("Personagem:"):
            lg["step"] = 1
            self.send(lg["name"])
        elif lg["step"] == 1 and "Senha" in last:
            pw = secret("Senha" + lg["suf"])
            if not pw:
                self.login = None
                return self.say("senha não encontrada no .credenciais: digite na mão.")
            lg["step"] = 2
            self.send(pw, hidden=True)
        elif lg["step"] == 2 and "Tecle ENTER" in self.tail:
            self.login = None
            self.send("")
        if "incorreta" in self.tail.lower():
            self.login = None

    def idle(self) -> None:
        if self.sock and not self.warned and time.time() - self.typed_at >= WARN:
            self.warned = True
            self.say(f"parado há {WARN // 60} minutos: lá pelos 8 a 10 minutos o servidor põe você no Vazio e uns 4 "
                     "minutos depois desconecta. Digite um comando para continuar.\a")

    # ------------------------------------------------------------------ o que sai
    def send(self, cmd: str, hidden: bool = False) -> None:
        sock = self.sock
        if not sock:
            return self.say("desconectado.")
        try:
            with self.lock:
                sock.sendall(cmd.encode("latin1", "replace") + b"\r\n")
        except OSError as e:
            return self.say(f"erro ao enviar: {e}")
        self.typed_at, self.warned = time.time(), False
        if not hidden:  # senha não vai para o transcript
            self.last_sent = cmd
            self.log(f"\n>>> [{time.strftime('%H:%M:%S')}] {cmd}\n")

    def door_ahead(self, cmd: str) -> None:
        """Direção digitada que o servidor acabou de mostrar fechada: o open vai antes, no mesmo Enter."""
        d = mapa.DIRS.get(cmd.strip().lower())
        if d and self.live and self.base.closed(self.room, d, self.live) and self.last_sent != f"open {d}":
            self.send(f"open {d}")

    def typed(self, line: str) -> None:
        """Uma linha sua para o jogo: o login automático para aqui, e a direção anda no mapa."""
        self.login = None
        self.got.clear()
        self.door_ahead(line)
        self.moved = mapa.DIRS.get(line.strip().lower())
        self.send(line)

    # ------------------------------------------------------------------ comandos do cliente
    def slash(self, line: str) -> None:
        name, _, arg = line.partition(" ")
        name = name if name in COMMANDS else next((c for c in COMMANDS if c.startswith(name)), name)
        cmd = getattr(self, "cmd_" + name[1:], None) if name in COMMANDS else None
        if not cmd:
            return self.say(f"{name} não é comando do cliente. /ajuda lista os comandos.")
        cmd(arg.strip())

    def cmd_ajuda(self, arg: str) -> None:
        print("Comandos do cliente; o resto vai para o jogo.")
        for name, what in COMMANDS.items():
            print(f"{name}: {what}.")
        print("No jogo, config +aural troca as tabelas e símbolos do Valinor por frases, e desliga as cores.")

    def cmd_rever(self, arg: str) -> None:
        print("\n".join(list(self.lines)[-(int(arg) if arg.isdigit() else REREAD):]) or "Nada ainda.")

    def cmd_conversas(self, arg: str) -> None:
        print("\n".join(list(self.talk)[-(int(arg) if arg.isdigit() else REREAD):]) or "Nenhuma conversa ainda.")

    def cmd_status(self, arg: str) -> None:
        print(self.prompt or "Ainda sem prompt.")

    def cmd_prompt(self, arg: str) -> None:
        self.every = not self.every
        self.say("prompt lido sempre." if self.every else "prompt lido só quando vida, mana ou movimento mudam.")

    def cmd_som(self, arg: str) -> None:
        self.bell = not self.bell
        self.say("sino das conversas ligado." if self.bell else "sino das conversas desligado.")

    def cmd_sala(self, arg: str) -> None:
        rid = (self.base.nearest(self.room, arg) or (None,))[0] if arg else self.room
        if not rid:
            return self.say(f"nenhuma sala da base com {arg}." if arg else NOWHERE + ".")
        r, links = self.base.rooms[rid], self.base.links[rid]
        print(f"{r['title']}, {self.base.region(rid)}.")
        print(r["description"])
        for d in mapa.sort_dirs(mapa.exits_of(r)):
            dest = self.base.rooms.get(links.get(d, ""), {}).get("title", "não percorrida")
            print(f"{NAMES[d]}: {dest}" + (", com porta fechada." if self.base.closed(rid, d) else "."))
        for key, label in (("mobs", "Seres"), ("objects", "Objetos")):
            if r.get(key):
                print(f"{label}: {'; '.join(r[key])}.")

    def cmd_rota(self, arg: str) -> None:
        if not arg:
            self.target, self.route = None, []
            return self.say("rota apagada.")
        if self.room is None:
            return self.say(NOWHERE + ".")
        hit = self.base.nearest(self.room, arg)
        if not hit or (hit[0] != self.room and not hit[1]):
            return self.say(f"nenhuma sala alcançável com {arg}.")
        if hit[0] == self.room:
            return self.say("você já está lá.")
        self.target, self.route = hit
        self.say(f"rota até {self.base.rooms[self.target]['title']}, {self.base.region(self.target)}, "
                 f"{steps(len(self.route))}: {spoken([d for d, _ in self.route])}. /andar vai até lá.")

    def cmd_andar(self, arg: str) -> None:
        if not self.sock or self.room is None:
            return self.say("entre no jogo e dê um look antes de andar.")
        if not self.route:
            return self.say("sem rota: use /rota e o nome da sala.")
        walk, door = self.base.walk(self.room, self.route, self.live, MAX_WALK)
        for cmd in walk:
            self.send(cmd)
        self.moved = None  # vários passos de uma vez: a sala é achada pelo texto, não pela última direção
        left = len(self.route) - len(walk) + bool(door)
        if left:
            self.say(f"abri a {door} e parei do outro lado: /andar continua." if door
                     else f"faltam {steps(left)}: /andar continua.")

    def cmd_busca(self, arg: str) -> None:
        if not arg:
            return self.say("use /busca e o texto.")
        hits = self.base.search(arg)
        for kind, name, where in hits:
            print(f"{kind}: {name}" + (f", {where}." if where else "."))
        if not hits:
            self.say(f"nada na base com {arg}.")

    def reroute(self) -> None:
        if not self.target or not self.room:
            return
        if self.room == self.target:
            self.arrived = self.base.rooms[self.target]["title"]
            self.target, self.route = None, []
            return
        self.route = self.base.route(self.room, lambda r: r == self.target) or []

    def run(self) -> None:
        for f in (sys.stdin, sys.stdout):
            f.reconfigure(errors="replace")  # terminal sem UTF-8 não derruba o cliente
        print(f"Valinor, modo leitor de tela. /ajuda lista os comandos do cliente. Logs em {LOGS}. Ctrl+D fecha o "
              "cliente; saia do jogo antes com quit. Para a tela com painéis, rode com --visual.")
        while True:
            try:
                if not self.sock:
                    self.pick()
                    self.connect()
                    continue
                self.got.wait(WAIT)
                hidden = self.masked or bool(ASKS_PW.search(self.tail))
                line = getpass.getpass("") if hidden else input()
            except (EOFError, KeyboardInterrupt):
                break
            self.nl = 1  # o Enter já pulou a linha
            if not self.sock:
                continue
            if hidden:
                self.login = None  # você digitou: o login automático para aqui
                self.got.clear()
                self.send(line, hidden=True)
            elif line.startswith("/"):
                self.slash(line)
            else:
                self.typed(line)
        if self.sock:
            self.sock.close()
        print("\nCliente fechado.")
