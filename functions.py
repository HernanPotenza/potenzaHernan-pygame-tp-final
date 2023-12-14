from models.enemy.enemy import Enemy

def draw_in_screen(text, color, button_pos, screen, font):
    text_to_draw = font.render(text, True, color)
    text_to_draw_rect = text_to_draw.get_rect()
    text_to_draw_rect.center = button_pos
    screen.blit(text_to_draw, text_to_draw_rect)

def create_one_enemy(enemy_data):
    enemy = Enemy(enemy_data)
    return enemy