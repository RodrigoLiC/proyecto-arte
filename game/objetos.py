import pygame

class Circulo:
    def __init__(self, x, y, radio, masa, color, velocidad_x=0, velocidad_y=0):
        self.posicion = pygame.math.Vector2(x, y)
        self.radio = radio
        self.color = color
        self.colorBase = color
        self.velocidad = pygame.math.Vector2(velocidad_x, velocidad_y)
        self.masa = masa
        self.pairs = []
        self.minVel = 1
        self.maxVel = 5

    def actualizar(self):
        if self.velocidad.length() == 0:
            return
        
        self.velocidad = self.velocidad.normalize() * max(min(self.velocidad.length(),self.maxVel),self.minVel)


        # Actualiza la posición sumando la velocidad
        self.posicion += self.velocidad

    def dibujar(self, superficie):
        # Crear superficie temporal con canal alpha (tamaño suficientemente grande)
        tam = int(self.radio * 3)
        capa = pygame.Surface((tam * 2, tam * 2), pygame.SRCALPHA)

        # Centrar la posición del círculo en la superficie
        centro = (tam, tam)
        col = self.color

        coef = (self.masa * 0.05)


        pygame.draw.circle(capa, (*col, 15), centro, int((1 + coef/2) * self.radio * 2.2))
        pygame.draw.circle(capa, (*col, 30), centro, int((1 + coef/2) * self.radio * 1.8))
        pygame.draw.circle(capa, (*col, 50), centro, int((1 + coef/4) * self.radio * 1.4))
        pygame.draw.circle(capa, (*col, 100), centro, int((1 + coef/7) * self.radio * 1.3))
        pygame.draw.circle(capa, (*col, 180), centro, int((1 + coef/10) * self.radio * 1.2))
        pygame.draw.circle(capa, (*col, 255), centro, int(self.radio))

        # Blitear la capa sobre la superficie principal
        superficie.blit(capa, (int(self.posicion.x - tam), int(self.posicion.y - tam)))


    def setVelLimit(self, minVel, maxVel):
        self.minVel = minVel
        self.maxVel = maxVel