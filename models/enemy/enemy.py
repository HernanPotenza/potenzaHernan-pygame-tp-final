import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import *

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_data):
        super().__init__()
        self.__iddle_r = sf.get_surface_from_spritesheet('assets/img/enemy/idle/idle.jpg', 4, 1, flip=True)
        for imagen in range(len(self.__iddle_r)):
            self.__iddle_r[imagen] = pg.transform.scale(self.__iddle_r[imagen], (ENEMY_WIDTH, ENEMY_HEIGHT))  
        self.__iddle_l = sf.get_surface_from_spritesheet('assets/img/enemy/idle/idle.jpg', 4, 1)
        for imagen in range(len(self.__iddle_r)):
            self.__iddle_r[imagen] = pg.transform.scale(self.__iddle_r[imagen], (ENEMY_WIDTH, ENEMY_HEIGHT))
        
        self.__walk_r = sf.get_surface_from_spritesheet('assets/img/enemy/walk/walk.png', 9, 1)
        for imagen in range(len(self.__walk_r)):
            self.__walk_r[imagen] = pg.transform.scale(self.__walk_r[imagen], (ENEMY_WIDTH, ENEMY_HEIGHT))  
        self.__walk_l = sf.get_surface_from_spritesheet('assets/img/enemy/walk/walk.png', 9, 1, flip=True)
        for imagen in range(len(self.__walk_l)):
            self.__walk_l[imagen] = pg.transform.scale(self.__walk_l[imagen], (ENEMY_WIDTH, ENEMY_HEIGHT))

        self.coord_x = enemy_data.get('pos_x')
        self.coord_y = enemy_data.get('pos_y')
        self.__frame_rate = FPS
        self.speed_walk = enemy_data.get('speed_walk')
        self.speed_run = enemy_data.get('speed_run')
        self.__gravity = enemy_data.get('gravity') 
        self.__jump = enemy_data.get('jump')
        self.__hp = enemy_data.get('hp')        
        self.floor_level = enemy_data.get('floor_level')
        self.damage = enemy_data.get('damage')
        self.score = enemy_data.get('score')
        
        self.__move_x = 0
        self.__move_y = 0
        self.__enemy_move_time = 0
        self.__enemy_animation_time = 0
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.rect = self.__actual_img_animation.get_rect()
        self.rect.x = self.coord_x
        self.rect.y = self.coord_y
        self.__is_looking_right = True
        self.__going_right = True
        self.is_alive = True
        self.score = 100


    def get_hp(self):
        return self.__hp

    def set_hp(self, nuevo_hp):
        self.__hp += nuevo_hp


    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            if self.rect.x < WINDOW_WIDTH - self.__actual_img_animation.get_width():
                pixels_move = self.__move_x
            else:
                    self.__move_x = 0
                    pixels_move = self.__move_x
        elif self.__move_x < 0:        
            if self.rect.x > 0:
                pixels_move = self.__move_x
            else:
                self.__move_x = 0
                pixels_move = self.__move_x
        return pixels_move


    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate:
            self.__enemy_move_time = 0
            if self.__set_borders_limits() == 0 and self.__going_right == True:
                self.__move_x = -5
                self.walk('Left')
                
            elif self.__set_borders_limits() == 0 and self.__going_right == False:
                self.__move_x = 5
                self.walk('Right')
            
            self.rect.x += self.__move_x
            self.rect.y += self.__move_y
            # Parte relacionado a saltar

            if self.rect.y + ENEMY_HEIGHT < (self.floor_level - self.__gravity):
                self.rect.y += self.__gravity
            elif self.rect.y + ENEMY_HEIGHT < self.floor_level:
                self.rect.y += self.floor_level - (self.rect.y + ENEMY_HEIGHT)


    def walk(self, direction: str = 'Right'):
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__walk_r, look_r=look_right)
                self.__going_right = True
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(self.__walk_l, look_r=look_right)
                self.__going_right = False


    def __set_x_animations_preset(self, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r 


    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0


    def update(self, delta_ms, screen: pg.surface.Surface):
        if self.is_alive:
            self.do_movement(delta_ms)
            self.do_animation(delta_ms)
            self.draw(screen)


    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.is_alive = False


    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        if self.__enemy_animation_time >= self.__frame_rate:
            self.__enemy_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                # if self.__is_jumping:
                #     self.__is_jumping = False
                #     self.__move_y = 0


    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'blue', self.rect)
            #pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)

