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
    
    if tick % 120 == 0:
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
            
            if circulos[i].posicion.distance_to(circulos[j].posicion) > 100:
                aplicar_gravedad(circulos[i], circulos[j], G=2)

            repulsion(circulos[i], circulos[j], G=3)


            pair_interact(i, j, circulos)

        circulos[i].actualizar()
        circulos[i].dibujar(ventana)

    for circulo in circulos:
        if circulo is None:
            continue
        
        c1 = circulo.colorBase
        c2 = circulo.color
        fraq = 100
        circulo.color = (
            (c1[0] + c2[0]*(fraq-1)) // fraq,
            (c1[1] + c2[1]*(fraq-1)) // fraq,
            (c1[2] + c2[2]*(fraq-1)) // fraq
        )


        fraq = 40

        if len(circulo.pairs) > 0:
            c3 = [0, 0, 0]
            size = len(circulo.pairs)
            for pair in circulo.pairs:
                if circulos[pair] is None:
                    size -= 1
                    continue
                    
                c3[0] += circulos[pair].color[0]
                c3[1] += circulos[pair].color[1]
                c3[2] += circulos[pair].color[2]
            
            

            if size > 0:
                c1 = circulo.color
                circulo.color = (
                    (c1[0]*(fraq - 1) + c3[0]/size) // fraq,
                    (c1[1]*(fraq - 1) + c3[1]/size) // fraq,
                    (c1[2]*(fraq - 1) + c3[2]/size) // fraq
                )


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
