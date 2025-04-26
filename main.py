#pgzero
"""
NOTA 1: El código de este proyecto está publicado en el repo:
        > https://github.com/rodrigovittori/Alien-Atleta-4543
    
NOTA 2: Los assests de este proyecto son del sitio web de Kenney,
        pueden obtener más modelos en: https://kenney.nl/assets/platformer-pack-redux
        y revisar la colección completa en: https://kenney.nl/assets/series:Platformer%20Pack  

---------------------------------------------------------------------------------------------------

    [M7.L1] - Actividad #7 (Extra): "Dividir a los enemigos"
    # Objetivo: En la pantalla de Game Over mostrar un mensaje que cambie
                según el tipo de enemigo/obstáculo que nos venció

    Paso Nº 1) Creamos una variable (global) que almacene el texto a mostrar según el tipo de colisión
    Paso Nº 2) Modifico el bloque de colisiones
    Paso Nº 3) Modifico el draw() para que muestre un mensaje según la colisión
    Paso Nº 4) Modifico el reset para que reinicie la variable de colision

    NOTA: Esta tarea no cuenta con el sprite "hurt", por lo que podemos recibir el siguiente error:
          > ValueError: Image hurt not found
    
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

""" Nota: Si quisieramos facilitar la tarea de "reiniciar"/"resetear"
          la posición del personaje o los obstáculos/enemigos a su estado
          inicial, podemos hacerlo de la siguiente manera:

    Paso 1) Creamos un atributo del actor donde registramos su posición inicial:

            personaje.posInicial = personaje.pos # almacenamos la posición inicial

    Paso 2) Cuando querramos resetear la posición, usaremos:

            personaje.pos = personaje.posInicial
"""

caja = Actor("box", (WIDTH - 50, 265))
abeja = Actor("bee", (WIDTH + 200, 150))

nva_imagen = "alien" # "alien": quieto / "left": mov. izq. / "right" : mov. dcha. / "duck" : agachado / "hurt" : dañado
game_over = False    # Vble que registra si nuestra partida ha finalizado o no
puntuacion = 0       # Cantidad de enemigos esquivados


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
    global nva_imagen, game_over, puntuacion, texto_colision

    if (game_over):
        # En caso de game over
        if (keyboard.enter):
            """ Reiniciar el juego """ # Nota: migrar a función
            game_over = False
            puntuacion = 0
            texto_colision = ""
            # Reseteamos personaje
            personaje.pos = (50, 240)
            personaje.timer_salto = 0
            personaje.timer_agachado = 0.0
            personaje.esta_agachado = False
            personaje.velocidad = 5
            nva_imagen = "alien"
            # Reseteamos caja
            caja.pos = (WIDTH - 50, 265)
            caja.angle = 0
            # Reseteamos abeja
            abeja.pos = (WIDTH + 200, 150)
            # Resetear velocidad enelmigos/obstáculos

    else:
        
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
            #nva_imagen = "hurt"
            texto_colision = "¡Entrega letal!"
            game_over = True

        elif personaje.colliderect(abeja):
            #nva_imagen = "hurt"
            texto_colision = "¡Eres alérgico a las abejas!"
            game_over = True

        """ POST INPUT """
        personaje.image = nva_imagen # Actualizamos el sprite del personaje
        
        ###################################################################################
    
        """  ####################
            # MOVER OBSTÁCULOS #
           ####################   """
        
        # Mover la caja - NOTA/TO-DO: Migrar a una función
        
        if (caja.x < 0):      # Si la caja salió de la ventana de juego...
            caja.x += WIDTH   # La llevamos a la otra punta de la pantalla
            puntuacion += 1     # Aumento en 1 el contador de eenmigos esquivados
        else:
            # Si todavía no se escapa de la ventana...
            caja.x -= 5     # mover la caja 5 px a la izquierda en cada frame
    
        # Rotar la caja
        caja.angle = (caja.angle % 360) + 5     # roto la caja 5 grados cada frame sin pasarme de 360º
    
    
        # Mover la abeja - NOTA/TO-DO: Migrar a una función
        
        if (abeja.x < 0):       # Si la caja salió de la ventana de juego...
            abeja.x += WIDTH    # La llevamos a la otra punta de la pantalla
            puntuacion += 1     # Aumento en 1 el contador de eenmigos esquivados
        else:
            # Si todavía no se escapa de la ventana...
            abeja.x -= 5     # mover la caja 5 px a la izquierda en cada frame

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