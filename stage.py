import pygame as pg
from models.constantes import *
from models.player.main_player import *
from models.enemy.enemy import *


class Stage:
    def __init__(self, screen, clock) -> None:        
        self.__level = 1
        if self.__level == 1:
            back_img = pg.image.load('jueguito/assets/img/background/fondo1.jpg')
            back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))
            juego_ejecutandose = True
            pjprincipal = Jugador(0, 0, frame_rate=70, speed_walk=25, speed_run=40, hp=100)
            object1_x = 100
            object1_y = 180
            object2_x = 490
            object2_y = 250
            platform_2_damage = 1
            platform_1_heal = 1
            enemy1_x = 500
            enemy1_y = 400
            enemy1_damage = 1
            enemy1 = Enemy(enemy1_x, enemy1_y, hp=50)

            while juego_ejecutandose:
                lista_eventos = pg.event.get()
                for event in lista_eventos:
                    match event.type:
                        case pg.KEYDOWN:
                            if event.key == pg.K_SPACE: #esto se puede usar para acciones que tienen
                                print('Estoy apretando el espacio') #que ocurrir una sola vez
                                pjprincipal.jump(True)
                        case pg.KEYUP:
                            if event.key == pg.K_SPACE:
                                print('Estoy soltando el espacio')
                        case pg.QUIT:
                            print('Estoy cerrando el juego')
                            juego_ejecutandose = False
                            break

                lista_teclas_presionadas = pg.key.get_pressed()
                if not lista_teclas_presionadas[pg.K_LEFT] and lista_teclas_presionadas[pg.K_RIGHT]:
                    pjprincipal.walk('Right')

                if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
                    pjprincipal.walk('Left')

                if not lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
                    pjprincipal.stay()
                if lista_teclas_presionadas[pg.K_UP]:
                    pjprincipal.jump('Up')
                if lista_teclas_presionadas[pg.K_DOWN]:
                    pjprincipal.jump('Down')

                if lista_teclas_presionadas[pg.K_q]:
                    pjprincipal.shoot()


                screen.blit(back_img, back_img.get_rect())
                pg.draw.rect(screen, (1, 1, 1), (object1_x, object1_y, 300, 20))  # Rectángulo blanco de 50x50 para objeto 1
                pg.draw.rect(screen, (1, 1, 1), (object2_x, object2_y, 300, 50))  # Rectángulo blanco de 50x50 para objeto 1

                # pg.draw.rect(screen, (100, 100, 100), (enemy1_x, enemy1_y, 50, 80))  # Rectángulo blanco de 50x50 para objeto 1


                object1_rect = pg.Rect(object1_x, object1_y, 300, 20)
                object2_rect = pg.Rect(object2_x, object2_y, 50, 50)

                # enemy1_rect = pg.Rect(enemy1_x, enemy1_y, 50, 80)

                player_rect = pjprincipal.get_rect()
                if player_rect.colliderect(object2_rect):
                    print('Chocando plataforma 2')
                    pjprincipal.take_damage(platform_2_damage)

                if player_rect.colliderect(object1_rect):
                    print('Chocando plataforma 1')
                    pjprincipal.heal(platform_1_heal)

                if player_rect.colliderect(enemy1.rect):
                    pjprincipal.take_damage(1)
                    enemy1.take_damage(damage=1)


                delta_ms = clock.tick(FPS)
                pjprincipal.update(delta_ms, screen)
                enemy1.update(delta_ms, screen)
                pg.display.update()


                for bullet in pjprincipal.bullet_group:
                    if bullet.rect.colliderect(enemy1.rect):
                        enemy1.take_damage(bullet.damage)
                        bullet.kill()
                        if not enemy1.is_alive:
                            pjprincipal.score += enemy1.score


                print(f'score:{pjprincipal.score}')

            pg.quit()
        elif self.__level == 2:
            pass


