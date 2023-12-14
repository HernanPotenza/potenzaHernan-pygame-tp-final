import pygame as pg
from models.constantes import *
from models.player.main_player import *
from models.enemy.enemy import *
from plataforma import Platform
from functions import draw_in_screen
from coin import Coin
from models.enemy.spawn import Spawn

class Stage:
    def __init__(self, stage_data_config, screen) -> None:        
        self.__level = 1
        if self.__level == 1:
            self.back_img = pg.image.load(stage_data_config.get('background_img'))
            self.back_img = pg.transform.scale(self.back_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.is_playing = True
            self.pjprincipal = Jugador(stage_data_config.get('player_data'))
            self.platforms_data = stage_data_config.get('platforms_data')
            self.stage_platforms = pg.sprite.Group()
            self.enemies_data = stage_data_config.get('enemies_data')
            self.stage_enemies = pg.sprite.Group()
            self.coins_data = stage_data_config.get('coins_data')
            self.stage_coins = pg.sprite.Group()
            self.screen = screen
            self.frame_rate = FPS
            self.fps_time = 0
            self.fps_time_sprites = 0
            self.clock = pg.time.Clock()
            self.delta_ms = self.clock.tick(FPS)
            self.game_over = False
            self.start_time = 0
            self.countdown = 0
            self.ready_to_next_level = False
            self.id = stage_data_config.get('id')
            self.spawn_data = 0
            self.stage_spawn = pg.sprite.Group()
            self.stage_data_config = stage_data_config
            self.stage_music = 0
            self.is_music_playing = False
            self.volume = 0.2


    def start(self, font):
        self.stage_music = pg.mixer.music.load(STAGE_1_MUSIC)
        pg.mixer.music.set_volume(self.volume)
        if not self.is_music_playing:
            pg.mixer.music.play()
            self.is_music_playing = True      
        if self.id == 3:
            self.spawn_data = self.stage_data_config.get('spawn_data')
            self.stage_spawn = pg.sprite.Group()
        self.start_time = pg.time.get_ticks()
        self.create_platforms()
        self.create_enemies()
        self.create_coins()
        if self.id == 3:
            self.create_spawn()

        while self.is_playing and not self.ready_to_next_level:
            self.fps_time += self.delta_ms
            if self.is_playing and self.fps_time >= self.frame_rate:
                self.fps_time = 0
                self.update(font)
                if len(self.stage_coins) == 0 and len(self.stage_enemies) == 0:
                    self.ready_to_next_level = True


    def events_update(self):
        lista_eventos = pg.event.get()
        for event in lista_eventos:
            match event.type:
                case pg.KEYDOWN:
                    if event.key == pg.K_SPACE and self.pjprincipal.ready_to_jump:
                        self.pjprincipal.is_jumping = True
                        self.pjprincipal.jump_time = pg.time.get_ticks()
                case pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        pass
                case pg.QUIT:
                    self.is_playing = False
                    break
        lista_teclas_presionadas = pg.key.get_pressed()
        if not lista_teclas_presionadas[pg.K_LEFT] and lista_teclas_presionadas[pg.K_RIGHT] and self.pjprincipal.is_jumping == False:
            self.pjprincipal.walk('Right')
        if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT] and self.pjprincipal.is_jumping == False:
            self.pjprincipal.walk('Left')

        if not lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT] and not self.pjprincipal.is_jumping and self.pjprincipal.ready_to_stay:
            self.pjprincipal.stay()
        
        if lista_teclas_presionadas[pg.K_LEFT]:
            self.pjprincipal.__is_looking_right = False
        if lista_teclas_presionadas[pg.K_RIGHT]:
            self.pjprincipal.__is_looking_right = True

        if lista_teclas_presionadas[pg.K_q] and self.pjprincipal.ready_to_shoot == True:
            self.pjprincipal.attack()
            self.pjprincipal.shoot_time = pg.time.get_ticks()
            self.pjprincipal.stay_time = pg.time.get_ticks()
            self.pjprincipal.ready_to_shoot = False
            

    def create_platforms(self):
        if len(self.stage_platforms) == 0:
            for x in range(len(self.platforms_data)):
                self.create_one_platform(self.platforms_data['platform_{0}'.format(x+1)])


    def create_one_platform(self, platform_data):
        platform = Platform(platform_data)
        platform.create(self.screen)
        self.stage_platforms.add(platform)


    def create_enemies(self):
        if len(self.stage_enemies) == 0:
            for x in range(len(self.enemies_data)):
                self.create_one_enemy(self.enemies_data['enemy_{0}'.format(x+1)])
    
    def create_one_enemy(self, enemy_data):
        enemy = Enemy(enemy_data)
        self.stage_enemies.add(enemy)


    def create_coins(self):
        if len(self.stage_coins) == 0:
            for x in range(len(self.coins_data)):
                self.create_one_coin(self.coins_data['coin_{0}'.format(x+1)])


    def create_one_coin(self, coin_data):
        coin = Coin(coin_data)
        self.stage_coins.add(coin)


    def create_spawn(self):
        spawn = Spawn(self.spawn_data)
        self.stage_spawn.add(spawn)


    def update(self, font):
        if self.is_playing:
            self.screen.blit(self.back_img, self.back_img.get_rect())
            self.stage_enemies.update(self.delta_ms, self.screen)
            self.events_update()
            self.fps_time_sprites += self.delta_ms
            if self.is_playing and self.fps_time_sprites >= self.frame_rate:
                self.stage_platforms.update(self.screen)
                self.pjprincipal.update(self.delta_ms, self.screen)
                self.stage_coins.update(self.delta_ms, self.screen)
                self.stage_spawn.update(self.delta_ms, self.screen, self.pjprincipal.bullet_group, self.pjprincipal)
                self.check_colision()
            self.timer_points_hp(font)
            pg.display.update()


    def check_colision(self):
        for enemy in self.stage_enemies:
            for bullet in self.pjprincipal.bullet_group:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(bullet.damage)
                    bullet.kill()
                    if not enemy.is_alive:
                        self.pjprincipal.score += enemy.score
                        enemy.kill()

            if enemy.rect.colliderect(self.pjprincipal.get_rect()):
                self.pjprincipal.take_damage_again += self.delta_ms
                if self.pjprincipal.take_damage_again >= self.frame_rate:
                    self.pjprincipal.take_damage_again = 0
                    self.pjprincipal.hp -= enemy.damage
                    
                if self.pjprincipal.hp <= 0:
                    self.is_playing = False

        for spawn in self.stage_spawn:
            for bullet in self.pjprincipal.bullet_group:
                if bullet.rect.colliderect(spawn.rect):
                    spawn.take_damage(bullet.damage)
                    bullet.kill()
                    if not spawn.is_alive:
                        self.pjprincipal.score += spawn.score
                        spawn.kill()
                        
        for coin in self.stage_coins:
            if coin.rect.colliderect(self.pjprincipal.get_rect()):
                self.pjprincipal.hp += coin.heal
                self.pjprincipal.score += coin.points
                coin.kill()

        
        if self.pjprincipal.get_rect().y + PJ_HEIGHT == self.pjprincipal.floor_level:
            self.pjprincipal.is_on_floor = True
        else:
            self.pjprincipal.is_on_floor = False

        for platform in self.stage_platforms:
            if self.pjprincipal.get_rect().colliderect(platform):
                if platform.rect.top - self.pjprincipal.get_rect().bottom >= -25:
                    self.pjprincipal.get_rect().x, self.pjprincipal.get_rect().y = self.pjprincipal.get_rect().x, platform.get_rect().top - PJ_HEIGHT
                    self.pjprincipal.is_on_floor = True
                    self.pjprincipal.is_jumping = False
                    
                elif platform.rect.bottom - self.pjprincipal.get_rect().top > -20 and platform.rect.bottom - self.pjprincipal.get_rect().top < 20:
                    self.pjprincipal.get_rect().x, self.pjprincipal.get_rect().y = self.pjprincipal.get_rect().x, platform.get_rect().bottom + PJ_HEIGHT
                    self.pjprincipal.is_on_floor = False
                    self.pjprincipal.is_jumping = False
                    
                elif platform.get_rect().left - self.pjprincipal.get_rect().right >= -50:
                    self.pjprincipal.get_rect().x, self.pjprincipal.get_rect().y = platform.get_rect().left - PJ_WIDTH, self.pjprincipal.get_rect().y
                elif platform.get_rect().right - self.pjprincipal.get_rect().left <= 50:
                    
                    self.pjprincipal.get_rect().x, self.pjprincipal.get_rect().y = self.pjprincipal.get_rect().right, self.pjprincipal.get_rect().y


    def timer_points_hp(self, font):
        if not self.game_over:
            timer = int((pg.time.get_ticks() - self.start_time)/1000)
            self.countdown -= self.delta_ms / 1000
            draw_in_screen(f"Timer: {timer}", INGAME_TEXT_COLOR, INGAME_TIMER_POS, self.screen, font)
            draw_in_screen(f"Points: {self.pjprincipal.score}", INGAME_TEXT_COLOR, INGAME_POINTS_POS, self.screen, font)
            draw_in_screen(f"Hp: {self.pjprincipal.hp}", INGAME_TEXT_COLOR, INGAME_HP_POS, self.screen, font)
