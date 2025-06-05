import random
import pygame
from game.objetos import Circulo
import colorsys

def color_saturado_aleatorio():
    h = random.random()               # Tono (0 a 1)
    s = 1.0                           # Saturación máxima
    v = random.uniform(0.8, 1.0)      # Valor alto (brillante)

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def crear_circulo_aleatorio_fuera_de_escena(ancho_ventana, alto_ventana, radio=30):
    radio = random.randint(25,30)
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


    color = color_saturado_aleatorio()
    masa = random.randint(1, 10)


    return Circulo(x, y, radio, masa, color, velocidad_x, velocidad_y)
