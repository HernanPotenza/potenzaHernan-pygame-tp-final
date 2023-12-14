import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import *
from models.enemy.enemy import *
from functions import create_one_enemy

class Spawn(pg.sprite.Sprite):
    def __init__(self, spawn_data):
        super().__init__()        
        self.__iddle_l = sf.get_surface_from_spritesheet('assets/img/spawn/spawn.png', 1, 1)
        for imagen in range(len(self.__iddle_l)):
            self.__iddle_l[imagen] = pg.transform.scale(self.__iddle_l[imagen], (ENEMY_WIDTH, ENEMY_HEIGHT))


        self.coord_x = spawn_data.get('pos_x')
        self.coord_y = spawn_data.get('pos_y')
        self.__frame_rate = FPS
        self.__hp = spawn_data.get('hp')        
        self.floor_level = spawn_data.get('floor_level')
        self.damage = spawn_data.get('damage')
        self.score = spawn_data.get('score')
        self.hp = spawn_data.get('hp')
        self.spawn_cooldown = spawn_data.get('spawn_cooldown')
        self.time_cooldown = 0
        self.enemy_data = spawn_data.get('spawn_enemy_data')
        self.enemies_spawned = pg.sprite.Group()
        self.enemy_spawned = False
        self.frame_rate = 100

        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_l
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.rect = self.__actual_img_animation.get_rect()
        self.rect.x = self.coord_x
        self.rect.y = self.coord_y
        self.__is_looking_right = True
        self.is_alive = True
        self.score = 100

    def get_hp(self):
        return self.__hp
    
    def set_hp(self, nuevo_hp):
        self.__hp += nuevo_hp


    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0


    def update(self, delta_ms, screen: pg.surface.Surface, bullet_group, pjprincipal):
        if self.is_alive:
            self.draw(screen)
            self.time_cooldown += delta_ms-3
            if pg.time.get_ticks()/1000 > self.spawn_cooldown:
                self.spawn_cooldown += 5
                enemy = create_one_enemy(self.enemy_data)
                self.enemies_spawned.add(enemy)
            self.enemies_spawned.update(delta_ms, screen)
            self.check_colision(delta_ms, bullet_group, pjprincipal)


    def check_colision(self, delta_ms, bullet_group, pjprincipal):
        for enemy in self.enemies_spawned:
            for bullet in bullet_group:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(bullet.damage)
                    bullet.kill()
                    if not enemy.is_alive:
                        pjprincipal.score += enemy.score
                        enemy.kill()

            if enemy.rect.colliderect(pjprincipal.get_rect()):
                pjprincipal.take_damage_again += delta_ms
                if pjprincipal.take_damage_again >= self.frame_rate:
                    pjprincipal.take_damage_again = 0
                    pjprincipal.hp -= enemy.damage


    def take_damage(self, damage):
        self.__hp -= damage
        if self.__hp <= 0:
            self.is_alive = False


    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'blue', self.rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)

