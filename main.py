import pygame as pg
from models.constantes import *
from models.player.main_player import *
from models.enemy.enemy import *
from stage import *

#from constantes import (
#   ALTO_VENTANA, ANCHO_VENTANA, FPS
#)

screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()
clock = pg.time.Clock()

Stage(screen, clock)