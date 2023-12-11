import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import *

class Enemy:
    def __init__(self, coord_x, coord_y, frame_rate = 100, speed_walk = 25, speed_run = 12, gravity = 15, jump = 32, hp = 100):
        self.__iddle_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/enemy/idle/idle.jpg', 4, 1, flip=True)
        for imagen in range(len(self.__iddle_r)):
            self.__iddle_r[imagen] = pg.transform.scale(self.__iddle_r[imagen], (93, 101))  
        self.__iddle_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/enemy/idle/idle.jpg', 4, 1)
        for imagen in range(len(self.__iddle_r)):
            self.__iddle_r[imagen] = pg.transform.scale(self.__iddle_r[imagen], (93, 101))
        
        self.__walk_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/enemy/walk/walk.jpg', 5, 1, flip=True)
        for imagen in range(len(self.__walk_r)):
            self.__walk_r[imagen] = pg.transform.scale(self.__walk_r[imagen], (93, 101))  
        self.__walk_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/enemy/walk/walk.jpg', 5, 1)
        for imagen in range(len(self.__walk_l)):
            self.__walk_l[imagen] = pg.transform.scale(self.__walk_l[imagen], (93, 101))


        # self.run_r = sf.get_surface_from_spritesheet(*****, *, *)
        # self.run_l = sf.get_surface_from_spritesheet(*****, *, *, *)

        self.__coord_x = coord_x
        self.__coord_y = coord_y
        self.__move_x = 0
        self.__move_y = 0
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__enemy_move_time = 0
        self.__enemy_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.rect = self.__actual_img_animation.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.__is_looking_right = True
        self.__going_right = True
        self.__hp = hp
        self.__flag = True
        self.is_alive = True
        self.score = 100


    def get_hp(self):
        return self.__hp
    
    def set_hp(self, nuevo_hp):
        self.__hp += nuevo_hp





    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            if self.rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width():
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
            if self.rect.y < 350:
                self.rect.y += self.__gravity


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


    def kill(self):
        self.is_alive = False
        self.rect.x = 800
        self.rect.y = 600
        


    def take_damage(self, damage):
        self.__hp -= damage
        print(self.__hp)
        if self.__hp <= 0:
            self.kill()


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




    # def move(self):
    #     self.__move_x = self.__speed_walk
