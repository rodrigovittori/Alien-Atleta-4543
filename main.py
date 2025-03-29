#pgzero
# [M6.L3] Actividad 7 "Engranaje (adicional)"
# Nota: La activdad 6 fue Kahoot! (no lleva código)

WIDTH = 600 # Ancho de la ventana
HEIGHT = 300 # Altura de la ventana

TITLE = "Adicional: Engranaje ⚙️" # Título para la ventana del juego
FPS = 30 # Número de fotogramas por segundo

engranaje = Actor("detail", (WIDTH/2, HEIGHT/2))
engranaje.sentido = "izquierda"

def draw():
    screen.fill(("#8B0000"))
    engranaje.draw()

def update(dt):
    
    # Movimiento del engranaje
    if (engranaje.sentido == "izquierda"):
        engranaje.angle += 5 # Rotar engranaje
        if (engranaje.x > int(engranaje.width / 2)):
            engranaje.x -= 5
        else:
            engranaje.sentido = "derecha"

    elif (engranaje.sentido == "derecha"):
        engranaje.angle -= 5 # Rotar engranaje
        if (engranaje.x < WIDTH - int(engranaje.width / 2)):
            engranaje.x += 5
        else:
            engranaje.sentido = "izquierda"


    
    