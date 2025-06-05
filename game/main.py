import pygame
import sys
from game.objetos import Circulo
from game.crearCirculo import crear_circulo_aleatorio_fuera_de_escena
from game.funciones import *
import random

pygame.init()
ANCHO, ALTO = 1200, 700
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Huellas")

# Crear un círculo con velocidad hacia la derecha y abajo
circulo = Circulo(x=ANCHO//2, y=ALTO//2, radio=30, masa=0, color=(255, 255, 255), velocidad_x=0, velocidad_y=0)

reloj = pygame.time.Clock()
ejecutando = True
tick = 0

circulos = [circulo]

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    if tick % 60 == 0:
        # Crear un nuevo círculo aleatorio fuera de la escena
        circulos.append(crear_circulo_aleatorio_fuera_de_escena(ANCHO, ALTO, radio=30))

    ventana.fill((0, 0, 0))

    for i in range(len(circulos)):
        if circulos[i] == None:
            continue
        for j in range(len(circulos)):
            if i == 0: # circulos[0] es estatico
                continue
            if circulos[j] == None or i == j:
                continue
            
            aplicar_gravedad(circulos[i], circulos[j], G=2)

            


            pair_interact(i, j, circulos)

        circulos[i].actualizar()
        circulos[i].dibujar(ventana)

    print(interacciones)

    #for circulo in circulos:
    #    if circulo is None:
    #        print("X ", end="")
    #    else:
    #        print("O ", end="")
    #print()

    eliminar_fueras(circulos, ANCHO, ALTO)

    pygame.display.flip()

    reloj.tick(60)
    tick += 1

pygame.quit()
sys.exit()
