#pgzero
# [M6.L3] Actividad 8 "Cristales (adicional)"

WIDTH = 200 # Ancho de la ventana
HEIGHT = 200 # Altura de la ventana

TITLE = "Cristales 🔮" # Título para la ventana del juego
FPS = 30 # Número de fotogramas por segundo

# Crea un personaje aquí
blue = Actor('blue', (20, 20))
red = Actor('red', (180, 20))
yellow = Actor('yellow', (180, 180))
green = Actor('green', (20, 180))
s = 1

def draw():
    screen.fill('white')
    blue.draw()
    red.draw()
    yellow.draw()
    green.draw()

    screen.draw.text(str(s), (30,30), color = "black" )

def update(dt):
    global s
    # Escribe tu código debajo
    blue.pos    = (blue.x    + (1 * s), blue.y   + (1 * s))
    red.pos     = (red.x     - (1 * s), red.y    + (1 * s))
    yellow.pos  = (yellow.x  - (1 * s), yellow.y - (1 * s))
    green.pos   = (green.x   + (1 * s), green.y  - (1 * s))

    # Rebote / cambiar sentido (s)
    if ( ( blue.pos == ((WIDTH/2), (HEIGHT/2)) ) or 
         ( blue.pos == (19, 19)) ):
        s *= -1