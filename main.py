#pgzero
"""
NOTA 1: El código de este proyecto está publicado en el repo:
        > https://github.com/rodrigovittori/Alien-Atleta-4543
    
NOTA 2: Los assests de este proyecto son del sitio web de Kenney,
        pueden obtener más modelos en: https://kenney.nl/assets/platformer-pack-redux
        y revisar la colección completa en: https://kenney.nl/assets/series:Platformer%20Pack  

---------------------------------------------------------------------------------------------------

    [M7.L1] - Actividad Nº 1: Método Colliderect
    Objetivo: Cambiar el sprite del personaje cuando éste entre en colisión con la caja

    Paso Nº 1) Agregar condición en update() que chequee si se dá una colisión entre PJ y caja
    Paso Nº 2) Si se dá la colisión, cambiamos la imágen a "hurt"

"""

WIDTH = 600 # Ancho de la ventana (en px)
HEIGHT = 300 # Alto de la ventana (en px)

TITLE = "Juego del Alien Atleta y sus piruetas" # Título para la ventana del juego
FPS = 30 # Número de fotogramas por segundo

""" > Vamos a crear nuestro personaje :D """
fondo = Actor("background")           # Nuestro fondo NO tiene posición porque queremos que ocupe TODA la pantalla
personaje = Actor("alien", (50, 240)) # Nuestro personaje SI la tiene, las coordenadas se registran en pos(x, y)

personaje.COOLDOWN_SALTO = 0.7        # tiempo de recarga habilidad salto (en segundos)
personaje.timer_salto = 0             # tiempo que debe pasar (en segundos) antes de que nuestro personaje pueda saltar nuevamente
personaje.altura_salto = int(personaje.height * 1.6) # El personaje saltará 1.6 veces su altura

""" Nota: Para evitar que al agacharse se anule la animación de salto DEBERÍAMOS implementar un check para prevenirlo """
personaje.timer_agachado = 0.0        # Tiempo restante (en segundos) antes de poner de pie al personaje
personaje.esta_agachado = False       # Valor que controla si debemos permanecer agachados o no

personaje.velocidad = 5               # velocidad (en px) a la que avanza el personaje por cada frame

""" Nota: Si quisieramos facilitar la tarea de "reiniciar"/"resetear"
          la posición del personaje o los obstáculos/enemigos a su estado
          inicial, podemos hacerlo de la siguiente manera:

    Paso 1) Creamos un atributo del actor donde registramos su posición inicial:

            personaje.posInicial = personaje.pos # almacenamos la posición inicial

    Paso 2) Cuando querramos resetear la posición, usaremos:

            personaje.pos = personaje.posInicial
"""

caja = Actor("box", (WIDTH - 50, 265))

nva_imagen = "alien" # "alien": quieto / "left": mov. izq. / "right" : mov. dcha.

##################################################################

def draw(): # draw() como su nombre lo indica es el método de pgzero que dibuja objetos en pantalla
    fondo.draw()
    personaje.draw()
    caja.draw()
    
    if (personaje.timer_salto <= 0):
        screen.draw.text("¡LISTO!", midleft=(20,20), color = (0, 255, 0), fontsize=24)
    else:
        screen.draw.text(str(personaje.timer_salto), midleft=(20,20), color = "red", fontsize=24)    

def update(dt): # update(dt) es el bucle ppal de nuestro juego, dt significa delta time (tiempo en segundos entre cada frame)
    # Podemos traducir "update" como "actualizar", es decir, en ella contendremos el código que produzca cambios en nuestro juego
    global nva_imagen
    
      #######################
     # CAMBIOS AUTOMATICOS #
    #######################

    nva_imagen = "alien"           # Si el personaje NO se mueve, tomamos este sprite por defecto
    personaje.timer_salto -= dt    # restamos al timer del cooldown de salto del persoanje el tiempo desde el último frame
    personaje.timer_agachado -= dt # restamos al timer para resetar la altura del persoanje el tiempo desde el último frame

    if ((personaje.timer_agachado <= 0) and (personaje.esta_agachado)):
        personaje.y = 240       # Reseteamos la altura del PJ (Si hemos creado una vble posInicial, lo tomamos de ese valor)
        personaje.esta_agachado = False

      ################
     # LEER TECLADO #
    ################
    
    # Movimiento del personaje:
    if ( (keyboard.right or keyboard.d) and ( personaje.x < ( WIDTH - int(personaje.width / 2) ) ) ):
        personaje.x += personaje.velocidad
        nva_imagen = "right"

    if ( (keyboard.left or keyboard.a) and ( personaje.x > int(personaje.width / 2) ) ):
        personaje.x -= personaje.velocidad
        nva_imagen = "left"

    if (keyboard.down or keyboard.s):
        personaje.y = 260    # Bajamos el pj
        nva_imagen = "duck"
        personaje.timer_agachado = 0.1 # tiempo que nuestro PJ seguirá agachado DESPUÉS de soltar la tecla
        personaje.esta_agachado = True
        
    # Salto: lo implementamos en OnKeyDown(key)

    """  ########################
        # COMPROBAR COLISIONES #
       ########################   """

    # Nota: migrar a función comprobar_colisiones()

    if personaje.colliderect(caja):
        if (nva_imagen != "hurt"):
            nva_imagen = "hurt"
    
    """ POST INPUT """
    personaje.image = nva_imagen # Actualizamos el sprite del personaje
    
    ###################################################################################
    
    # Mover la caja - NOTA/TO-DO: Migrar a una función
    
    if (caja.x < 0):       # Si la caja salió de la ventana de juego...
        caja.x += WIDTH    # La llevamos a la otra punta de la pantalla
    else:
        # Si todavía no se escapa de la ventana...
        caja.x -= 5     # mover la caja 5 px a la izquierda en cada frame

    # Rotar la caja
    caja.angle = (caja.angle % 360) + 5     # roto la caja 5 grados cada frame sin pasarme de 360º

def on_key_down(key): # Este método se activa al presionar una tecla
    # https://pygame-zero.readthedocs.io/en/stable/hooks.html?highlight=on_key_down#on_key_down

    if (
         (keyboard.space or keyboard.w or keyboard.up) and   # Parte 1 de la cond: presionar tecla
         (personaje.timer_salto <= 0) and                    # Parte 2 de la cond: timer listo
         (personaje.y > int(personaje.height / 2))           # Parte 3 de la cond: el PJ NO ha salido de la pantalla
       ):
        
        personaje.timer_salto = personaje.COOLDOWN_SALTO                # Reseteamos cooldown
        personaje.y -= personaje.altura_salto                           # El PJ "salta" (cambiamos su altura)
        # TO-DO: Agregar cambio de sprite al saltar
        animate(personaje, tween="bounce_end", duration = 2, y = 240)   # Activamos la animación de caída 