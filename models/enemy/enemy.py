import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import *

class Enemy:
    def __init__(self, coord_x, coord_y, frame_rate = 100, speed_walk = 25, speed_run = 12, gravity = 16, jump = 32, hp = 100):
        self.__iddle_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/enemy/idle/idle.jpg', 5, 1, flip=True)
        self.__iddle_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/enemy/idle/idle.jpg', 5, 1)
        # self.run_r = sf.get_surface_from_spritesheet(*****, *, *)
        # self.run_l = sf.get_surface_from_spritesheet(*****, *, *, *)

        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__enemy_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True
        self.__hp = hp

    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move
    

    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        print(self.__enemy_move_time)
        if self.__enemy_move_time >= self.__frame_rate:
            self.__enemy_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__rect.y += self.__move_y
            # Parte relacionado a saltar
            if self.__rect.y < 350:
                self.__rect.y += self.__gravity

    def update(self, delta_ms, screen: pg.surface.Surface):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.draw(screen)

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                # if self.__is_jumping:
                #     self.__is_jumping = False
                #     self.__move_y = 0

    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'blue', self.__rect)
            #pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

    def take_damage(self, damage):
        self.__hp -= damage
        print(self.__hp)
        if self.__hp <= 0:
            print('MURIO ENEMIGO')

    
    def move(self):
        self.__move_x = self.__speed_walk
