"""Modo leitor de tela (`valinor --leitor`): o jogo em texto corrido, como num telnet, sem painel, moldura, barra ou
símbolo. O texto do servidor sai na ordem em que chega e sem cores, e cada linha digitada vai para o jogo: o leitor de
tela lê o que chega e o cursor fica sempre no fim. Ficam o seletor com login automático, os logs, o keepalive TCP e o
aviso antes do Vazio. Nada é mandado sozinho além do login do personagem escolhido."""
from __future__ import annotations

import getpass
import socket
import sys
import threading
import time

from conexao import ANSI, ASKS_PW, LOGS, load_chars, other_connections, secret, telnet
from vigia import WARN, keepalive

try:
    import readline  # noqa: F401  setas, edição e histórico no input() (Linux e macOS)
except ImportError:
    pass

WAIT = 1.0  # segundos esperando a resposta antes de abrir a próxima linha: se for o pedido de senha, ela vem escondida


def clean(text: str) -> str:
    """Texto do servidor para o leitor de tela: sem cores, sem \\r e sem tabulação."""
    return ANSI.sub("", text).replace("\r", "").replace("\t", "    ")


class Leitor:
    def __init__(self, host: str, port: int) -> None:
        self.host, self.port = host, port
        self.sock: socket.socket | None = None
        self.lock, self.got = threading.Lock(), threading.Event()
        self.masked, self.login, self.tail = False, None, ""
        self.typed_at, self.warned = time.time(), False
        LOGS.mkdir(parents=True, exist_ok=True)
        self.raw = open(LOGS / "raw.log", "ab")
        self.tr = open(LOGS / "transcript.log", "a", encoding="utf-8")

    def say(self, text: str) -> None:
        print(f"\n[cliente] {text}", flush=True)

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
        self.sock, self.masked, self.tail, self.typed_at, self.warned = sock, False, "", time.time(), False
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
            text = clean(data.decode("latin1"))
            self.log(text)
            sys.stdout.write(text)
            sys.stdout.flush()
            self.tail = (self.tail + text)[-400:]
            self.autologin()
            self.got.set()
        sock.close()
        self.sock, self.masked = None, False
        self.say("conexão encerrada. Enter escolhe o personagem de novo, Ctrl+D fecha o cliente.")
        self.got.set()

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
                     "minutos depois desconecta. Digite um comando para continuar.")

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
            self.log(f"\n>>> [{time.strftime('%H:%M:%S')}] {cmd}\n")

    def run(self) -> None:
        for f in (sys.stdin, sys.stdout):
            f.reconfigure(errors="replace")  # terminal sem UTF-8 não derruba o cliente
        print(f"Valinor, modo leitor de tela. Logs em {LOGS}. Ctrl+D fecha o cliente; saia do jogo antes com quit.")
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
            if self.sock:
                self.login = None  # você digitou: o login automático para aqui
                self.got.clear()
                self.send(line, hidden)
        if self.sock:
            self.sock.close()
        print("\nCliente fechado.")
