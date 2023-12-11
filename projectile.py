import pygame as pg
from models.constantes import *

class Projectile(pg.sprite.Sprite):
    def __init__(self, speed, size_x, size_y, pos_x, pos_y, direction:bool):
        super().__init__()
        self.image = pg.Surface((size_x, size_y)) 
        self.image.fill((255, 0, 0))
        self.direction = direction
        self.velocity = speed
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.damage = 20

    def update(self):
        match self.direction:
            case True:
                self.rect.x += self.velocity
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case False:
                self.rect.x -= self.velocity
                if self.rect.x <= 0:
                    self.kill()