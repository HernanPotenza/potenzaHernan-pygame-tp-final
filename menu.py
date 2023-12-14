import json
from stage import Stage
import pygame as pg
from models.constantes import *
from button import Button
from functions import draw_in_screen

class Menu:
    def __init__(self, all_stages_data_config_json):
        pg.init()
        data = open(all_stages_data_config_json)
        self.json_data = json.load(data)
        self.stages_data = self.json_data.get("stages")
        self.stage_selected = self.stages_data.get("stage_1")
        self.is_playing = True
        self.menu_font = pg.font.Font('assets/fonts/font2.ttf', 50)
        self.buttons = []
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.in_settings = True
        self.volume = 1.0
        self.is_music_playing = False
        self.menu_active = True
        self.in_stage_select = False


        self.title_text = self.menu_font.render("MENU PRINCI", True, "white")
        self.title_text_pos = ((WINDOW_WIDTH - self.title_text.get_width()) // 2, 35)


    def main_menu(self):
        self.menu_music = pg.mixer.music.load(MENU_MUSIC)
        while self.menu_active:
            pg.mixer.music.set_volume(self.volume)
            if not self.is_music_playing:
                pg.mixer.music.play()
                self.is_music_playing = True      

            mouse = pg.mouse.get_pos()
            self.screen.fill(MENU_BACKGROUND_COLOR)
            self.buttons.append(Button((WINDOW_WIDTH/2, 250), PLAY_BUTTON_TEXT, self.menu_font, 'black', 'white'))
            self.buttons.append(Button((WINDOW_WIDTH/2, 380), SETTINGS_BUTTON_TEXT, self.menu_font, 'black', 'white'))
            self.buttons.append(Button((WINDOW_WIDTH/2, 510), QUIT_BUTTON_TEXT, self.menu_font, 'black', 'white'))
            draw_in_screen(MENU_TITLE, MENU_BUTTONS_COLOR, SETTINGS_MENU_TITLE_POS, self.screen, self.menu_font)

            for button in self.buttons:
                button.change_color(mouse)
                button.update(self.screen)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.buttons[0].is_mouse_on_top(mouse):
                            self.in_stage_select = True
                            self.stage_select()
                        if self.buttons[1].is_mouse_on_top(mouse):
                            self.in_settings = True
                            self.settings()
                        if self.buttons[2].is_mouse_on_top(mouse):
                            self.menu_active = False
            pg.display.flip()


    def stage_select(self):
        while self.in_stage_select:
            mouse = pg.mouse.get_pos()
            self.screen.fill(MENU_BACKGROUND_COLOR)
            
            draw_in_screen(STAGE_SELECT_MENU_TITLE, MENU_BUTTONS_COLOR, STAGE_SELECT_MENU_TITLE_POS, self.screen, self.menu_font)            
            stage_1 = Button(STAGE_SELECT_MENU_STAGE_1_POS, STAGE_SELECT_MENU_STAGE_1, self.menu_font, MENU_BUTTONS_COLOR, MENU_HOVERING_COLOR)
            stage_2 = Button(STAGE_SELECT_MENU_STAGE_2_POS, STAGE_SELECT_MENU_STAGE_2, self.menu_font, MENU_BUTTONS_COLOR, MENU_HOVERING_COLOR)
            stage_3 = Button(STAGE_SELECT_MENU_STAGE_3_POS, STAGE_SELECT_MENU_STAGE_3, self.menu_font, MENU_BUTTONS_COLOR, MENU_HOVERING_COLOR)
            back_to_menu_button = Button(STAGE_SELECT_MENU_BACK_BUTTON_POS, STAGE_SELECT_MENU_BACK_BUTTON, self.menu_font, MENU_BUTTONS_COLOR, MENU_HOVERING_COLOR)

            self.update_stage_select_buttons(mouse, stage_1, stage_2, stage_3, back_to_menu_button)      

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if stage_1.is_mouse_on_top(mouse):
                        self.stage_selected = self.stages_data.get("stage_1")
                        pg.mixer.music.stop()
                        self.start_stage()

                    if stage_2.is_mouse_on_top(mouse):
                        self.stage_selected = self.stages_data.get("stage_2")
                        self.start_stage()

                    if stage_3.is_mouse_on_top(mouse):
                        self.stage_selected = self.stages_data.get("stage_3")
                        self.start_stage()

                    if back_to_menu_button.is_mouse_on_top(mouse):
                        self.in_stage_select = False

            pg.display.flip()         

    def start_stage(self):
        actual_stage = Stage(self.stage_selected, self.screen)
        actual_stage.start(self.menu_font)


    def settings(self):
        while self.in_settings:
            mouse = pg.mouse.get_pos()
            self.screen.fill(MENU_BACKGROUND_COLOR)
            
            draw_in_screen(SETTINGS_MENU_TITLE, MENU_BUTTONS_COLOR, SETTINGS_MENU_TITLE_POS, self.screen, self.menu_font)            
            back_to_menu_button = Button(SETTINGS_MENU_BACK_BUTTON_POS, SETTINGS_MENU_BACK_BUTTON, self.menu_font, MENU_BUTTONS_COLOR, MENU_HOVERING_COLOR)
            volume_up_button = Button(SETTINGS_MENU_VOLUME_UP_POS, SETTINGS_MENU_VOLUME_UP, self.menu_font, MENU_BUTTONS_COLOR, MENU_HOVERING_COLOR)
            volume_down_button = Button(SETTINGS_MENU_VOLUME_DOWN_POS, SETTINGS_MENU_VOLUME_DOWN, self.menu_font, MENU_BUTTONS_COLOR, MENU_HOVERING_COLOR)

            self.update_settings_buttons(mouse, back_to_menu_button, volume_up_button, volume_down_button)     

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back_to_menu_button.is_mouse_on_top(mouse):
                        self.in_settings = False

                    if volume_up_button.is_mouse_on_top(mouse):
                        self.volume += 0.1

                    if volume_down_button.is_mouse_on_top(mouse):
                        self.volume -= 0
            pg.display.flip()
            
    def update_stage_select_buttons(self, mouse, stage_1, stage_2, stage_3, back_to_menu_button):
        stage_1.change_color(mouse)            
        stage_1.update(self.screen)
        
        stage_2.change_color(mouse)            
        stage_2.update(self.screen)
        
        stage_3.change_color(mouse)            
        stage_3.update(self.screen)
        
        back_to_menu_button.change_color(mouse)
        back_to_menu_button.update(self.screen)


    def update_settings_buttons(self, mouse, back_to_menu_button, volume_up_button, volume_down_button):
        back_to_menu_button.change_color(mouse)            
        back_to_menu_button.update(self.screen)
        
        volume_up_button.change_color(mouse)
        volume_up_button.update(self.screen)
        
        volume_down_button.change_color(mouse)
        volume_down_button.update(self.screen)

