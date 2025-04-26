#pgzero
import random 

"""
NOTA 1: El código de este proyecto está publicado en el repo:
        > https://github.com/rodrigovittori/Alien-Atleta-4543
    
NOTA 2: Los assests de este proyecto son del sitio web de Kenney,
        pueden obtener más modelos en: https://kenney.nl/assets/platformer-pack-redux
        y revisar la colección completa en: https://kenney.nl/assets/series:Platformer%20Pack  

---------------------------------------------------------------------------------------------------

    [M7.L2] - Actividad #3: "Enemigos aleatorios"
    # Objetivo: Llamar al próximo obstáculo/enemigo según un valor random

    Modificamos el sistema de obstáculos para actualizar uno a la vez, que se determina de forma aleatoria


    Paso Nº 1) Importar el módulo random
    Paso Nº 2) Crear la vble global "prox_enemigo", que tomará un valor random entre 1 y 2
               (xq sólo tenemos dos tipos de enemigos)
    Paso Nº 3) Modificaremos nuestra función actualizar_enemigos() para que SOLO mueva el enemigo seleccionado
    Paso Nº 4) Agregar a la función reiniciar_juego una condición para reestablecer el valor del prox_enemigo a spwanear

    Nota: Para facilitar las tareas de respawn implementamos posInicial al PJ, abeja y caja
            > Cambiamos spawn a WIDTH + 50

"""

WIDTH = 600 # Ancho de la ventana (en px)
HEIGHT = 300 # Alto de la ventana (en px)

TITLE = "Juego del Alien Atleta y sus piruetas" # Título para la ventana del juego
FPS = 30 # Número de fotogramas por segundo

""" > Vamos a crear nuestro personaje :D """
fondo = Actor("background")           # Nuestro fondo NO tiene posición porque queremos que ocupe TODA la pantalla
cartel_game_over = Actor("GO")        # Splash Screen de Game Over
personaje = Actor("alien", (50, 240)) # Nuestro personaje SI la tiene, las coordenadas se registran en pos(x, y)

personaje.COOLDOWN_SALTO = 0.7        # tiempo de recarga habilidad salto (en segundos)
personaje.timer_salto = 0             # tiempo que debe pasar (en segundos) antes de que nuestro personaje pueda saltar nuevamente
personaje.altura_salto = int(personaje.height * 1.6) # El personaje saltará 1.6 veces su altura

""" Nota: Para evitar que al agacharse se anule la animación de salto DEBERÍAMOS implementar un check para prevenirlo """
personaje.timer_agachado = 0.0        # Tiempo restante (en segundos) antes de poner de pie al personaje
personaje.esta_agachado = False       # Valor que controla si debemos permanecer agachados o no

personaje.velocidad = 5               # velocidad (en px) a la que avanza el personaje por cada frame
personaje.posInicial = personaje.pos

caja = Actor("box", (WIDTH + 50, 265))
caja.posInicial = caja.pos

abeja = Actor("bee", (WIDTH + 50, 150))
abeja.posInicial = abeja.pos

nva_imagen = "alien" # "alien": quieto / "left": mov. izq. / "right" : mov. dcha. / "duck" : agachado / "hurt" : dañado
game_over = False    # Vble que registra si nuestra partida ha finalizado o no
puntuacion = 0       # Cantidad de enemigos esquivados

prox_enemigo = random.randint(1, 2) # 1: Caja / 2: Abeja

##################################################################

"""  #####################
    # FUNCIONES PROPIAS #
   #####################  """

def actualizar_enemigos():
    global puntuacion, prox_enemigo
    """ NOTA: Si cambiamos al velocidad de los enemigos en base a una vble, debemos incluírla """

    if (prox_enemigo == 1): 
        # Mover la caja
        if (caja.x < 0):      # Si la caja salió de la ventana de juego...
            caja.pos = caja.posInicial
            caja.angle = 0
            puntuacion += 1     # Aumento en 1 el contador de eenmigos esquivados
            prox_enemigo = random.randint(1, 2) # Selecciono prox enemigo de forma aleatoria
        else:
            # Si todavía no se escapa de la ventana...
            caja.x -= 5     # mover la caja 5 px a la izquierda en cada frame
            
            # Rotar la caja
            caja.angle = (caja.angle % 360) + 5     # roto la caja 5 grados cada frame sin pasarme de 360º

    elif (prox_enemigo == 2):
        # Mover la abeja
        if (abeja.x < 0):       # Si la caja salió de la ventana de juego...
            abeja.pos = abeja.posInicial
            puntuacion += 1     # Aumento en 1 el contador de eenmigos esquivados
            prox_enemigo = random.randint(1, 2) # Selecciono prox enemigo de forma aleatoria
        else:
            # Si todavía no se escapa de la ventana...
            abeja.x -= 5     # mover la caja 5 px a la izquierda en cada frame

def mover_personaje():
    global nva_imagen

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

def detectar_colisiones():
    global texto_colision, nva_imagen, game_over
    
    if personaje.colliderect(caja):
        #nva_imagen = "hurt"
        texto_colision = "¡Entrega letal!"
        game_over = True
    
    elif personaje.colliderect(abeja):
        #nva_imagen = "hurt"
        texto_colision = "¡Eres alérgico a las abejas!"
        game_over = True

def reiniciar_juego():
    global game_over, puntuacion, texto_colision, nva_imagen, prox_enemigo
    
    game_over = False
    puntuacion = 0
    texto_colision = ""
    prox_enemigo = random.randint(1, 2) # Selecciono prox enemigo de forma aleatoria
    # Reseteamos personaje
    nva_imagen = "alien"
    personaje.image = nva_imagen
    personaje.pos = (50, 240)
    personaje.timer_salto = 0
    personaje.timer_agachado = 0.0
    personaje.esta_agachado = False
    personaje.velocidad = 5
    
    # Reseteamos caja
    caja.pos = caja.posInicial
    caja.angle = 0
    # Reseteamos abeja
    abeja.pos = abeja.posInicial
    # Resetear velocidad enelmigos/obstáculos

##################################################################

def draw(): # draw() como su nombre lo indica es el método de pgzero que dibuja objetos en pantalla
    if (game_over):
        # Si bien en este caso el cartel de Game Over cubre toda la pantalla, 
        # sería mejor solamente agregar el texto GAME OVER y dibjar el fondo
        fondo.draw() 
        cartel_game_over.draw()
        # Nota: modificamos la altura del otro mensaje para mostrar más info:
        screen.draw.text(("Enemigos esquivados: " + str(puntuacion)), center= (int(WIDTH/2), 2* int(HEIGHT/3)), color = "yellow", fontsize = 24)
        screen.draw.text("Presiona [Enter] para reiniciar", center= (int(WIDTH/2), 4* int(HEIGHT/5)), color = "white", fontsize = 32)
        screen.draw.text(texto_colision, center= (int(WIDTH/2), int(HEIGHT/5)), color = "red", background = "black", fontsize = 24)
        
    else:
        fondo.draw()
        personaje.draw()
        caja.draw()
        abeja.draw()
        
        if (personaje.timer_salto <= 0):
            screen.draw.text("¡LISTO!", midleft=(20,20), color = (0, 255, 0), fontsize=24)
        else:
            screen.draw.text(str(personaje.timer_salto), midleft=(20,20), color = "red", fontsize=24)

        screen.draw.text(("Enemigos esquivados: " + str(puntuacion)), midright=(WIDTH-20, 20), color ="black", background="white", fontsize=24)

def update(dt): # update(dt) es el bucle ppal de nuestro juego, dt significa delta time (tiempo en segundos entre cada frame)
    # Podemos traducir "update" como "actualizar", es decir, en ella contendremos el código que produzca cambios en nuestro juego
    global nva_imagen, puntuacion, texto_colision

    if not game_over:
        #######################
         # CAMBIOS AUTOMATICOS #
          #######################
        
        texto_colision = ""            # Texto que indica el motivo de nuestro Game Over
        nva_imagen = "alien"           # Si el personaje NO se mueve, tomamos este sprite por defecto
        personaje.timer_salto -= dt    # restamos al timer del cooldown de salto del persoanje el tiempo desde el último frame
        personaje.timer_agachado -= dt # restamos al timer para resetar la altura del persoanje el tiempo desde el último frame
    
        if ((personaje.timer_agachado <= 0) and (personaje.esta_agachado)):
            personaje.y = 240       # Reseteamos la altura del PJ (Si hemos creado una vble posInicial, lo tomamos de ese valor)
            personaje.esta_agachado = False
    
        mover_personaje()
        detectar_colisiones()

        """ POST INPUT """
        personaje.image = nva_imagen # Actualizamos el sprite del personaje
        
        ###################################################################################
    
        actualizar_enemigos()

def on_key_down(key):
    global game_over
    # Este método se activa al presionar una tecla
    # https://pygame-zero.readthedocs.io/en/stable/hooks.html?highlight=on_key_down#on_key_down
    if (not game_over):
        if (
             (keyboard.space or keyboard.w or keyboard.up) and   # Parte 1 de la cond: presionar tecla
             (personaje.timer_salto <= 0) and                    # Parte 2 de la cond: timer listo
             (personaje.y > int(personaje.height / 2))           # Parte 3 de la cond: el PJ NO ha salido de la pantalla
           ):
            
            personaje.timer_salto = personaje.COOLDOWN_SALTO                # Reseteamos cooldown
            personaje.y -= personaje.altura_salto                           # El PJ "salta" (cambiamos su altura)
            # TO-DO: Agregar cambio de sprite al saltar
            animate(personaje, tween="bounce_end", duration = 2, y = 240)   # Activamos la animación de caída
    else:
        # En caso de game over, si presiono Enter, reiniciamos el juego
        if (keyboard.enter):
            reiniciar_juego()