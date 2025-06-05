import pygame

class Circulo:
    def __init__(self, x, y, radio, masa, color, velocidad_x=0, velocidad_y=0):
        self.posicion = pygame.math.Vector2(x, y)
        self.radio = radio
        self.color = color
        self.velocidad = pygame.math.Vector2(velocidad_x, velocidad_y)
        self.masa = masa
        self.pairs = []

    def actualizar(self):
        if self.velocidad.length() == 0:
            return
        
        self.velocidad = self.velocidad.normalize() * max(min(self.velocidad.length(),2),5)


        # Actualiza la posición sumando la velocidad
        self.posicion += self.velocidad

    def dibujar(self, superficie):
        # Dibuja el círculo en la superficie dada
        pygame.draw.circle(superficie, self.color, (int(self.posicion.x), int(self.posicion.y)), self.radio)