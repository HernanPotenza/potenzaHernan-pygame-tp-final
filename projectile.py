import pygame as pg
from models.constantes import *
from models.auxiliar import SurfaceManager as sf


class Projectile(pg.sprite.Sprite):
    def __init__(self, speed, pos_x, pos_y, direction:bool):
        super().__init__()
        self.__projectile = sf.get_surface_from_spritesheet('assets/img/projectile/fireball.png', 1, 1)
        for imagen in range(len(self.__projectile)):
            self.__projectile[imagen] = pg.transform.scale(self.__projectile[imagen], (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))  
        self.image = self.__projectile[0]
        self.direction = direction
        self.velocity = speed
        self.damage = 20
        self.__actual_animation = self.__projectile
        self.__initial_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.rect = self.__actual_img_animation.get_rect(center=(pos_x, pos_y))
        self.player_shoot_time = 0


    def update(self, delta_ms):
        self.player_shoot_time += delta_ms
        if self.player_shoot_time >= FPS:
            self.player_shoot_time = 0
            match self.direction:
                case True:
                    self.rect.x += self.velocity
                    if self.rect.x >= WINDOW_WIDTH:
                        self.kill()
                case False:
                    self.rect.x -= self.velocity
                    if self.rect.x <= 0:
                        self.kill()

    def draw2(self, screen: pg.surface.Surface):

        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)