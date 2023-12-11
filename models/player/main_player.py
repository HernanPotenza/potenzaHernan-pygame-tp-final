from models.auxiliar import SurfaceManager as sf
import pygame as pg
from models.constantes import *
from projectile import *

        # self.__iddle_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/idle/iddle.png', 10, 1)
        # self.__iddle_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/idle/iddle.png', 10, 1, flip=True)

        # self.__walk_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/walk/walk_right.png', 12, 1)
        # self.__walk_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/walk/walk_right.png', 12 , 1, flip=True)
        
        # self.__jump_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/jump/jump.png', 10, 1, flip=True)
        # self.__jump_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/jump/jump.png', 10, 1, flip=True)

class Jugador(pg.sprite.Sprite): #proyectil y enemigo tambien tienen que heredar de Sprite hay que usar dos cosas: update y draw
    #grupo_de_enemigos.add()
    #grupo_de_enemigos.update(no recibe nada)
    #grupo_de_enemigos.draw(screen)
    #self.__grupo_de_proyectiles
    def __init__(self, coord_x, coord_y, frame_rate = 100, speed_walk = 25, speed_run = 12, gravity = 16, jump = 32, hp = 100):
        super().__init__()
        self.__iddle_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/idle/iddle.png', 10, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/idle/iddle.png', 10, 1, flip=True)

        self.__walk_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/walk/walk_right.png', 12, 1)
        self.__walk_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/walk/walk_right.png', 12 , 1, flip=True)
        
        self.__jump_l = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/jump/jump.png', 10, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet('jueguito_secundario/assets/img/player/jump/jump.png', 10, 1, flip=True)


        # self.__grupo_de_proyectiles = pg.sprite.Group()
        # self.__grupo_de_proyectiles.update()
        # self.__grupo_de_proyectiles.draw(screen) #bullet.kill() para eliminar las balas


        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x = 10
        self.__rect.y = 300
        self.__is_looking_right = True
        self.__hp = hp
        self.score = 0

        self.bullet_speed = 15
        self.bullet_size_x = 10
        self.bullet_size_y = 10
        self.bullet_group = pg.sprite.Group()


    def get_rect(self):
        return self.__rect
        #objeto1_rect = pygame.Rect(x_objeto1, y_objeto1, 20, 20)


    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r


    def __set_y_animations_preset(self):
        self.__move_y = -self.__jump
        self.__move_x = self.__speed_run if self.__is_looking_right else -self.__speed_run
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        self.__is_jumping = True


    def walk(self, direction: str = 'Right'):
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=look_right)


    def run(self, direction: str = 'Right'):
        self.__initial_frame = 0
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r=look_right)


    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0


    def jump(self, jumping=True):
        if jumping and not self.__is_jumping:
            self.__set_y_animations_preset()
        else:
            self.__is_jumping = False
            self.stay()


    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move


    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__rect.y += self.__move_y
            # Parte relacionado a saltar
            if self.__rect.y < 335:
                self.__rect.y += self.__gravity


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


    def take_damage(self, damage):
        self.__hp -= damage
        print(self.__hp)
        if self.__hp <= 0:
            print('MURIO PERSONAJE')


    def heal(self, heal):
        self.__hp += heal
        print(self.__hp)


    def update(self, delta_ms, screen: pg.surface.Surface):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.draw(screen)
        self.bullet_group.update()
        self.bullet_group.draw(screen)

        # self.__grupo_de_proyectiles.update()
        # self.__grupo_de_proyectiles.draw(screen)


    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
            #pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)


    def shoot(self):
            self.bullet_group.add(self.create_bullet(self.bullet_speed, self.bullet_size_x, self.bullet_size_y))

    def create_bullet(self, speed, size_x, size_y):
        return Projectile(speed, size_x, size_y, self.__rect.centerx, self.__rect.centery, self.__is_looking_right)

