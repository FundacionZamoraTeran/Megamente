get_sprite_path = lambda x, y: 'assets/img/%s/%s' % (x, y)


FONT_PATH = 'assets/fonts/PatuaOne-Regular.ttf'

DEDUCCION_ASSETS = {
    'background': get_sprite_path('deduccion', 'background.png'),
    'arrow': get_sprite_path('deduccion', 'arrow.png'),
    'horizontal_panel': get_sprite_path('deduccion', 'horizontal-panel.png'),
    'vertical_panel': get_sprite_path('deduccion', 'vertical-panel.png'),
}

#messages
WIN_MESSAGE = "Felicidades, pasas al siguiente nivel!"
GAME_OVER_MESSAGE = 'Vuelve a Intentarlo'


CURSOR = (
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  ",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
        "XXX.........................XXXX",
        "XXX..........................XXX",
        "XXX..........................XXX",
        "XXX.........................XXXX",
        "XXX.......XXXXXXXXXXXXXXXXXXXXX ",
        "XXX........XXXXXXXXXXXXXXXXXXX  ",
        "XXX.........XXX                 ",
        "XXX..........XXX                ",
        "XXX...........XXX               ",
        "XXX....X.......XXX              ",
        "XXX....XX.......XXX             ",
        "XXX....XXX.......XXX            ",
        "XXX....XXXX.......XXX           ",
        "XXX....XXXXX.......XXX          ",
        "XXX....XXXXXX.......XXX         ",
        "XXX....XXX XXX.......XXX        ",
        "XXX....XXX  XXX.......XXX       ",
        "XXX....XXX   XXX.......XXX      ",
        "XXX....XXX    XXX.......XXX     ",
        "XXX....XXX     XXX.......XXX    ",
        "XXX....XXX      XXX.......XXX   ",
        "XXX....XXX       XXX.......XXX  ",
        "XXX....XXX        XXX.......XXX ",
        "XXX....XXX         XXX.......XXX",
        "XXX....XXX          XXX......XXX",
        "XXX....XXX           XXX.....XXX",
        "XXX....XXX            XXX...XXXX",
        " XXX..XXX              XXXXXXXX ",
        "  XXXXXX                XXXXXX  ",
        "   XXXX                  XXXX   "
)

COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'grey': (130, 130, 130),
    'yellow': (252, 185, 24),
}

FONT_PATH = 'assets/fonts/PatuaOne-Regular.ttf'
