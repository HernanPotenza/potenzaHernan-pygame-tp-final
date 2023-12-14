import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import PLATFORM_WIDTH, PLATFORM_HEIGHT, DEBUG


class Platform(pg.sprite.Sprite):
    def __init__(self, platform_data):
        super().__init__()
        self.__platform_start = sf.get_surface_from_spritesheet('assets/img/platform/platform_start.png', 1, 1)
        for imagen in range(len(self.__platform_start)):
            self.__platform_start[imagen] = pg.transform.scale(self.__platform_start[imagen], (PLATFORM_WIDTH, PLATFORM_HEIGHT))  

        self.__platform_middle = sf.get_surface_from_spritesheet('assets/img/platform/platform_middle.png', 1, 1)
        for imagen in range(len(self.__platform_middle)):
            self.__platform_middle[imagen] = pg.transform.scale(self.__platform_middle[imagen], (PLATFORM_WIDTH, PLATFORM_HEIGHT)) 

        self.__platform_end = sf.get_surface_from_spritesheet('assets/img/platform/platform_end.png', 1, 1)
        for imagen in range(len(self.__platform_end)):
            self.__platform_end[imagen] = pg.transform.scale(self.__platform_end[imagen], (PLATFORM_WIDTH, PLATFORM_HEIGHT))  

        self.id = platform_data.get('id')
        self.pos_x = platform_data.get('pos_x')
        self.pos_y = platform_data.get('pos_y')
        self.size_x = platform_data.get('size_x')
        self.size_y = platform_data.get('size_y')
        self.rect = 0
        self.start_rect = 0
        self.middle_rect = 0
        self.end_rect = 0
        self.image = 0


    def create(self, screen):
        pg.draw.rect(screen, (100, 100, 100), (self.pos_x, self.pos_y, self.size_x, self.size_y))
        self.image = pg.Surface((self.size_x*PLATFORM_WIDTH, self.size_y*PLATFORM_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.start_rect = pg.Rect(self.pos_x, self.pos_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.middle_rect = pg.Rect(self.pos_x+PLATFORM_WIDTH, self.pos_y, PLATFORM_WIDTH*(self.size_x-2), PLATFORM_HEIGHT)
        self.end_rect = pg.Rect(self.pos_x+PLATFORM_WIDTH*(self.size_x-1), self.pos_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


    def get_rect(self):
            return self.rect


    def update(self, screen):
        self.draw(screen)



    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'blue', self.rect)

        screen.blit(self.__platform_start[0], self.start_rect)

        self.middle_rect = pg.Rect(self.pos_x+PLATFORM_WIDTH, self.pos_y, PLATFORM_WIDTH*(self.size_x-2), PLATFORM_HEIGHT)

        for x in range(self.size_x-2):
            screen.blit(self.__platform_middle[0], self.middle_rect)
            self.middle_rect.x+=PLATFORM_WIDTH
        

        screen.blit(self.__platform_end[0], self.end_rect)

