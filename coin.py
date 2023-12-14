import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import *

class Coin(pg.sprite.Sprite):
    def __init__(self, coin_data):
        super().__init__()

        self.pos_x = coin_data.get('pos_x')        
        self.pos_y = coin_data.get('pos_y')
        self.size_x = coin_data.get('size_x')
        self.size_y = coin_data.get('size_y')
        self.heal = coin_data.get('coin_heal')
        self.points = coin_data.get('coin_points')
        
        self.idle = sf.get_surface_from_spritesheet(coin_data.get("coin_img"), 6, 1)
        for imagen in range(len(self.idle)):
            self.idle[imagen] = pg.transform.scale(self.idle[imagen], (self.size_x, self.size_x))  
        self.frame_rate = coin_data.get("frame_rate")
        self.initial_frame = 0
        self.image = self.idle[self.initial_frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.coin_animation_time = 0


    def do_animation(self, delta_ms):
        self.coin_animation_time += delta_ms
        if self.coin_animation_time >= self.frame_rate:
            self.coin_animation_time = 0
            if self.initial_frame < len(self.idle) - 1:
                self.initial_frame += 1
            else:
                self.initial_frame = 0


    def update(self, delta_ms, screen):
        self.do_animation(delta_ms)
        self.image = self.idle[self.initial_frame]
        screen.blit(self.image, self.rect)

