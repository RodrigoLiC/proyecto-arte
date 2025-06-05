import random
import pygame
from game.objetos import Circulo

def crear_circulo_aleatorio_fuera_de_escena(ancho_ventana, alto_ventana, radio=30):
    # Decide por qué lado aparecerá: 0=izquierda, 1=derecha, 2=arriba, 3=abajo
    lado = random.randint(0, 3)

    velocidad_min = 1
    velocidad_max = 4

    if lado == 0:  # Aparece a la izquierda
        x = -radio
        y = random.randint(0, alto_ventana)
        velocidad_x = random.uniform(velocidad_min, velocidad_max)  # hacia la derecha
        velocidad_y = random.uniform(-velocidad_max, velocidad_max)
    elif lado == 1:  # Aparece a la derecha
        x = ancho_ventana + radio
        y = random.randint(0, alto_ventana)
        velocidad_x = -random.uniform(velocidad_min, velocidad_max)  # hacia la izquierda
        velocidad_y = random.uniform(-velocidad_max, velocidad_max)
    elif lado == 2:  # Aparece arriba
        x = random.randint(0, ancho_ventana)
        y = -radio
        velocidad_x = random.uniform(-velocidad_max, velocidad_max)
        velocidad_y = random.uniform(velocidad_min, velocidad_max)  # hacia abajo
    else:  # Aparece abajo
        x = random.randint(0, ancho_ventana)
        y = alto_ventana + radio
        velocidad_x = random.uniform(-velocidad_max, velocidad_max)
        velocidad_y = -random.uniform(velocidad_min, velocidad_max)  # hacia arriba


    color = (random.randint(200,255), random.randint(100,255), random.randint(100,255))
    masa = random.randint(1, 10)


    return Circulo(x, y, radio, masa, color, velocidad_x, velocidad_y)
