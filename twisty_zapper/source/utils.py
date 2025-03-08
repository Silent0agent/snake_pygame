import os
import sys

import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_sound(name):
    fullname = '..\\assets\\sounds\\' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound


def start_music(name, volume):
    fullname = '..\\assets\\sounds\\' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)


def menu_music(name, vol, flag):
    if flag:
        start_music(name, vol)


def click_sound():
    load_sound('sound_effects\\click.mp3').play()


def load_image(name, colorkey=None):
    fullname = '..\\assets\\images\\' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def cut_sprite_sheet(sheet, columns, rows, snake_images_dict):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    frame_location = (0, 0)
    snake_images_dict['angle1'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (0, 50)
    snake_images_dict['angle2'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (100, 0)
    snake_images_dict['angle3'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (100, 100)
    snake_images_dict['angle4'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (50, 0)
    snake_images_dict['horizontal'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (100, 50)
    snake_images_dict['vertical'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 0)
    snake_images_dict['head_up'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 0)
    snake_images_dict['head_right'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 50)
    snake_images_dict['head_left'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 50)
    snake_images_dict['head_down'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 100)
    snake_images_dict['end_down'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 100)
    snake_images_dict['end_left'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 150)
    snake_images_dict['end_right'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 150)
    snake_images_dict['end_up'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))


def load_level(filename):
    filename = "..\\levels\\" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def update_stats(difficulty, level_num, score):
    difficulty_num = '1'
    if difficulty == 'easy':
        difficulty_num = '1'
    elif difficulty == 'normal':
        difficulty_num = '2'
    elif difficulty == 'hard':
        difficulty_num = '3'
    with open('..\\statistics\\stats.txt', 'r', encoding='UTF-8') as file:
        # Прочитаем файл целиком и сохраним каждую строку в список
        lines = file.readlines()
    new_line = f'{level_num} уровень: {score}\n'
    line_number = level_num + int(difficulty_num) - 1 + (int(difficulty_num) - 1) * 10
    try:
        if int(lines[line_number].rstrip().split(':')[1][1:]) >= score:
            return
        lines[line_number] = new_line
    except IndexError:
        print(f'Ошибка: Строка {line_number} отсутствует.')
    with open('..\\statistics\\stats.txt', 'w', encoding='UTF-8') as file:
        file.writelines(lines)
