import pygame
from utils import load_image, cut_sprite_sheet

WIDTH, HEIGHT = 750, 800  # размеры окна
TILE_SIZE = 25  # размер игровой плитки
MINI_TILE_SIZE = 15  # размер плитки схемы уровня
START_SCREENS_FPS = 10  # fps на статичных экранах

music_menu_flag = True
current_sprite_sheet = 0
current_empty_image = 0
current_apple_image = 0
current_wall_image = 0

all_sprites = pygame.sprite.Group()
mini_tiles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()
horizontal_borders_group = pygame.sprite.Group()
vertical_borders_group = pygame.sprite.Group()

# Следующие группы не относятся к all_sprites
particle_group = pygame.sprite.Group()
game_over_group = pygame.sprite.Group()
animated_group = pygame.sprite.Group()

sprites_sheets = ['sprite_sheets\\sprites_sheet_1.png', 'sprite_sheets\\sprites_sheet_2.png']
empty_images = ['sprite_images\\tiles\\tile1.jpg', 'sprite_images\\tiles\\tile2.jpg', 'sprite_images\\tiles\\tile3.jpg']
wall_images = ['sprite_images\\walls\\wall1.jpg', 'sprite_images\\walls\\wall2.jpg']
apple_images = ['sprite_images\\apples\\apple1.png', 'sprite_images\\apples\\apple2.png']
current_images = {'empty': load_image('sprite_images\\tiles\\tile1.jpg'),
                  'wall': load_image('sprite_images\\walls\\wall1.jpg'),
                  'apple': load_image('sprite_images\\apples\\apple1.png')}
current_snake_images = {}
cut_sprite_sheet(load_image('sprite_sheets\\sprites_sheet_1.png'), 5, 4, current_snake_images)
