#pgzero
""" [M6.L3] - Actividad 2: "Ventana del Juego"
    Objetivo: presentar el sistema de pgzero a los alumnos """

WIDTH = 600  # Ancho de la ventana (en px)
HEIGHT = 300 # Alto de la ventana  (en px)

FPS = 30
TITLE = "TÍTULO ÉPICO"

def draw():
    screen.fill(("#d6af66"))
    screen.draw.text(TITLE, center=(WIDTH/2, HEIGHT/2), color="white", background="black", fontsize = 48)