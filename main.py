#pgzero
# [M6.L3] - Actividad #1: "Introducción"
# Nota: NO enseñar archivos personalizados hasta el final de la clase

WIDTH  = 770 # Ancho de la ventana (en px)
HEIGHT = 450 # Alto de la ventana  (en px)

TITLE = "IMG" # Título de la ventana de juego
FPS = 30      # Fotogramas (MAX) por segundo

fondo = Actor("picture") # Creamos un Actor con la imagen "picture.jpg"

""" >> Funciones de pgzero << """

def draw():
    fondo.draw()