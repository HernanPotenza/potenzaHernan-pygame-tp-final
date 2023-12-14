from models.auxiliar import SurfaceManager as sf
import pygame as pg
from models.constantes import *
from projectile import *

class Jugador(pg.sprite.Sprite): 
    def __init__(self, player_data):
        super().__init__()
        self.__iddle_r = sf.get_surface_from_spritesheet('assets/img/player/idle/iddle.png', 3, 1, flip=True)
        for imagen in range(len(self.__iddle_r)):
            self.__iddle_r[imagen] = pg.transform.scale(self.__iddle_r[imagen], (PJ_WIDTH, PJ_HEIGHT))

        self.__iddle_l = sf.get_surface_from_spritesheet('assets/img/player/idle/iddle.png', 3, 1)
        for imagen in range(len(self.__iddle_l)):
            self.__iddle_l[imagen] = pg.transform.scale(self.__iddle_l[imagen], (PJ_WIDTH, PJ_HEIGHT))

        self.__walk_r = sf.get_surface_from_spritesheet('assets/img/player/walk/walk.png', 3, 1)
        for imagen in range(len(self.__walk_r)):
            self.__walk_r[imagen] = pg.transform.scale(self.__walk_r[imagen], (PJ_WIDTH, PJ_HEIGHT))

        self.__walk_l = sf.get_surface_from_spritesheet('assets/img/player/walk/walk.png', 3 , 1, flip=True)
        for imagen in range(len(self.__walk_l)):
            self.__walk_l[imagen] = pg.transform.scale(self.__walk_l[imagen], (PJ_WIDTH, PJ_HEIGHT))

        self.__jump_r = sf.get_surface_from_spritesheet('assets/img/player/jump/jump.png', 3, 1, flip=True)
        for imagen in range(len(self.__jump_r)):
            self.__jump_r[imagen] = pg.transform.scale(self.__jump_r[imagen], (PJ_WIDTH, PJ_HEIGHT))

        self.__jump_l = sf.get_surface_from_spritesheet('assets/img/player/jump/jump.png', 3, 1)
        for imagen in range(len(self.__jump_l)):
            self.__jump_l[imagen] = pg.transform.scale(self.__jump_l[imagen], (PJ_WIDTH, PJ_HEIGHT))

        self.__attack_l = sf.get_surface_from_spritesheet('assets/img/player/attack/attack.png', 3, 1)
        for imagen in range(len(self.__attack_l)):
            self.__attack_l[imagen] = pg.transform.scale(self.__attack_l[imagen], (PJ_WIDTH, PJ_HEIGHT))

        self.__attack_r = sf.get_surface_from_spritesheet('assets/img/player/attack/attack.png', 3, 1, flip=True)
        for imagen in range(len(self.__attack_r)):
            self.__attack_r[imagen] = pg.transform.scale(self.__attack_r[imagen], (PJ_WIDTH, PJ_HEIGHT))


        self.__move_x = player_data.get('coord_x')
        self.__move_y = player_data.get('coord_y')
        self.__frame_rate = FPS
        self.__speed_walk = player_data.get('speed_walk')
        self.__gravity = player_data.get('gravity')
        self.__jump = player_data.get('jump')
        self.hp = player_data.get('hp')
        self.floor_level = player_data.get('floor_level')
        self.take_damage_again = player_data.get('take_damage_again')

        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.is_jumping = False
        self.jump_direction = 'left'
        self.jump_duration = 450
        self.jump_time = 0
        self.last_jump_time = 0
        self.jump_cooldown = 1000
        self.ready_to_jump = True
        self.is_on_floor = False
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__rect.x = 10
        self.__rect.y = 300
        self.__is_looking_right = True
        self.score = 0
        self.ready_to_stay = True
        self.stay_time = 0
        self.stay_cooldown = 200

        self.bullet_speed = 25
        self.bullet_size_x = 15
        self.bullet_size_y = 15
        self.bullet_group = pg.sprite.Group()
        self.ready_to_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 500
        self.player_update_time = 0

    def get_rect(self):
        return self.__rect


    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r


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
            if self.is_on_floor:
                self.ready_to_jump = True
                self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
                self.__initial_frame = 0
                self.__move_x = 0
                self.__move_y = 0


    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.x < WINDOW_WIDTH - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move


    def __set_y_animations_preset(self):
        self.__move_x = self.__speed_walk if self.__is_looking_right else -self.__speed_walk
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0


    def jump(self):
        self.__speed_walk = 10
        self.__set_y_animations_preset()
        if pg.time.get_ticks() - self.jump_time < self.jump_duration:
            self.__rect.y -= self.__jump
            self.ready_to_jump = False
        else:
            self.is_jumping = False



    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate + 50:

            if self.is_jumping:
                self.jump()
            else:
                self.__speed_walk = 20
                
            self.__player_move_time = 0
            self.__rect.x += self.__set_borders_limits()
            self.__rect.y += self.__move_y
            if not self.is_jumping and not self.is_on_floor:
                if self.__rect.y + PJ_HEIGHT < (self.floor_level - self.__gravity):
                    self.__rect.y += self.__gravity
                elif self.__rect.y + PJ_HEIGHT <  self.floor_level:
                    self.__rect.y +=  self.floor_level-(self.__rect.y + PJ_HEIGHT)
            else:
                pass


    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0


    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print('MURIO PERSONAJE')


    def heal(self, heal):
        self.hp += heal


    def update(self, delta_ms, screen):
        self.player_update_time += delta_ms
        if self.player_update_time >= self.__frame_rate - 20:
            self.do_animation(delta_ms)
            self.draw(screen)
        if self.player_update_time >= self.__frame_rate:
            self.do_movement(delta_ms)
            self.bullet_group.update(delta_ms)
            self.bullet_group.draw(screen)
            self.reload()
            self.stay_reload()
            self.jump_reload()


    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)


    def attack(self):
        self.ready_to_stay = False
        self.shoot()
        match self.__is_looking_right:
            case True:
                self.__set_x_animations_preset(0, self.__attack_r, look_r=self.__is_looking_right)        
            case False:
                self.__set_x_animations_preset(0, self.__attack_l, look_r=self.__is_looking_right)


    def shoot(self):
            self.bullet_group.add(self.create_bullet(self.bullet_speed))


    def create_bullet(self, speed):
        return Projectile(speed, self.__rect.centerx, self.__rect.centery, self.__is_looking_right)


    def reload(self):
        if not self.ready_to_shoot:
            current_time = pg.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.ready_to_shoot = True

    def stay_reload(self):
        if not self.ready_to_stay:
            current_time = pg.time.get_ticks()
            if current_time - self.stay_time >= self.stay_cooldown:
                self.ready_to_stay = True

    def jump_reload(self):
        if not self.ready_to_jump:
            current_time = pg.time.get_ticks()
            if current_time - self.jump_time >= self.jump_cooldown:
                self.ready_to_jump = True
