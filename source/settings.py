import pygame
from utils import load_image, cut_snake_sprite_sheet, cut_apple_sprite_sheet

WIDTH, HEIGHT = 750, 800  # размеры окна
TILE_SIZE = 25  # размер игровой плитки
MINI_TILE_SIZE = 15  # размер плитки схемы уровня
START_SCREENS_FPS = 10  # fps на статичных экранах
GRAVITY = 6.67 * (10 ** (-11))

music_menu_flag = True
current_snake_sprite_sheet = 0
current_empty_image = 0
current_apple_sprite_sheet = 0
current_wall_image = 0

all_sprites = pygame.sprite.Group()
mini_tiles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()
horizontal_borders_group = pygame.sprite.Group()
vertical_borders_group = pygame.sprite.Group()
fake_apples_group = pygame.sprite.Group()

# Следующие группы не относятся к all_sprites
particle_group = pygame.sprite.Group()
game_over_group = pygame.sprite.Group()
animated_group = pygame.sprite.Group()

snake_sprites_sheets = ['sprite_sheets\\snakes\\sprites_sheet_1.png', 'sprite_sheets\\snakes\\sprites_sheet_2.png',
                        'sprite_sheets\\snakes\\sprites_sheet_3.png']
apple_sprites_sheets = ['sprite_sheets\\apples\\sprites_sheet_1.png', 'sprite_sheets\\apples\\sprites_sheet_2.png',
                        'sprite_sheets\\apples\\sprites_sheet_3.png', 'sprite_sheets\\apples\\sprites_sheet_4.png']
empty_images = ['sprite_images\\tiles\\tile1.jpg', 'sprite_images\\tiles\\tile2.jpg', 'sprite_images\\tiles\\tile3.jpg',
                'sprite_images\\tiles\\tile4.jpg', 'sprite_images\\tiles\\tile5.jpg']
wall_images = ['sprite_images\\walls\\wall1.jpg', 'sprite_images\\walls\\wall2.jpg', 'sprite_images\\walls\\wall3.jpg',
               'sprite_images\\walls\\wall4.jpg']
star_image = 'sprite_images\\particles\\star.png'
shield_image = 'sprite_images\\particles\\shield.png'
current_images = {'empty': load_image(empty_images[current_empty_image]),
                  'wall': load_image(wall_images[current_wall_image])}
current_snake_images, current_apple_images = {}, {}
bomb_apple_images, switch_head_apple_images, invincible_apple_images, rock_apple_images = {}, {}, {}, {}
cut_snake_sprite_sheet(load_image(snake_sprites_sheets[current_snake_sprite_sheet]), 5, 4,
                       current_snake_images)
cut_apple_sprite_sheet(load_image(apple_sprites_sheets[current_apple_sprite_sheet]), 5, 2,
                       current_apple_images)
cut_apple_sprite_sheet(load_image('sprite_sheets\\apples\\sprites_sheet_5.png'), 5, 2, bomb_apple_images)
cut_apple_sprite_sheet(load_image('sprite_sheets\\apples\\sprites_sheet_6.png'), 5, 2, switch_head_apple_images)
cut_apple_sprite_sheet(load_image('sprite_sheets\\apples\\sprites_sheet_7.png'), 5, 2, invincible_apple_images)
cut_apple_sprite_sheet(load_image('sprite_sheets\\apples\\sprites_sheet_8.png'), 5, 2, rock_apple_images)
