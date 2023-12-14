import pygame as pg
from models.constantes import CONFIG_JSON
from stage import *
from menu import Menu




start_menu = Menu(CONFIG_JSON)
start_menu.main_menu()
