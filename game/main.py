import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 800
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Círculo en ventana negra")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Posición y radio del círculo
radio = 50
posicion_circulo = (ANCHO // 2, ALTO // 2)

# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Rellenar la ventana con negro
    VENTANA.fill(NEGRO)

    # Dibujar el círculo blanco
    pygame.draw.circle(VENTANA, BLANCO, posicion_circulo, radio)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar los FPS
    reloj.tick(60)

# Salir de Pygame
pygame.quit()
sys.exit()

def main():
    print("a")