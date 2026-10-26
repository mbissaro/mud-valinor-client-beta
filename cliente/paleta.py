"""Cores do cliente, tiradas do FC-pallete.png: o pôr do sol laranja e vermelho, o céu lilás, a casa azul, a parede
acesa, a calçada molhada e a poça que reflete tudo.

Cada cor diz de onde veio no quadro (mediana dos pixels da região, ou o pico mais vivo daquela matiz). As cores de texto
foram clareadas para ler bem no fundo escuro do terminal. Em 256 cores o curses usa a mais próxima da paleta xterm;
em 8/16 cores fica o tema básico do terminal. `python3 paleta.py` mostra as amostras."""
from __future__ import annotations

SUNSET = (241, 155, 10)  # céu laranja
SUN = (253, 235, 7)  # a parede da casa acesa pela luz do poste, o amarelo mais vivo
EMBER = (236, 67, 10)  # vermelho-laranja do céu
CRIMSON = (245, 80, 85)  # vermelho do céu (220, 27, 11), clareado
HOUSE = (30, 170, 225)  # a casa azul (0, 143, 201), clareada
SHADOW = (25, 135, 205)  # a casa na sombra (0, 119, 183), clareada
TEAL = (16, 175, 160)  # verde-água da poça (16, 175, 126), puxado para o azul
LIME = (133, 198, 34)  # verde do reflexo na parede acesa
GRASS = (71, 178, 94)  # verde da poça
PINK = (221, 92, 168)  # magenta da poça (148, 4, 63), clareado
PLUM = (170, 60, 140)  # céu entre o vermelho e o lilás (143, 44, 113), clareado
LILAC = (112, 82, 152)  # céu lilás (97, 62, 136), clareado
STREET = (140, 165, 178)  # calçada molhada (97, 133, 150), clareada
CURB = (89, 110, 119)  # calçada na sombra
SAND = (181, 166, 155)  # os claros quentes da calçada
MIST = (228, 220, 235)  # os claros do quadro puxam para o lilás (189, 179, 203), clareados
GLARE = (255, 240, 200)  # o brilho da lâmpada
POLE = (24, 22, 30)  # postes e telhado

# o que o servidor pinta com ESC[3Xm (0-7) e com negrito (8-15)
ANSI = (POLE, CRIMSON, GRASS, SUNSET, SHADOW, PLUM, TEAL, SAND,
        CURB, EMBER, LIME, SUN, HOUSE, PINK, (90, 200, 225), MIST)

if __name__ == "__main__":
    for name, rgb in list(globals().items()):
        if isinstance(rgb, tuple) and len(rgb) == 3:
            r, g, b = rgb
            print(f"\x1b[48;2;{r};{g};{b}m      \x1b[0m \x1b[38;2;{r};{g};{b}m{name}\x1b[0m")
