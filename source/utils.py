from datetime import datetime
import os
import sqlite3
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


def cut_snake_sprite_sheet(sheet, columns, rows, snake_images_dict):
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


def cut_apple_sprite_sheet(sheet, columns, rows, apple_images):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            apple_images[f'{j}{i}'] = (sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))


def load_level(filename):
    filename = "..\\levels\\" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def init_db(db_name):
    con, cur = connect_to_db(db_name)
    cur.execute('CREATE TABLE IF NOT EXISTS Difficulties (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS High_scores (id INTEGER  PRIMARY KEY AUTOINCREMENT, difficulty_id '
        'INTEGER REFERENCES difficulties (id), level_num INTEGER, score INTEGER, date DATETIME)')
    cur.execute('INSERT OR IGNORE INTO Difficulties (id, name) VALUES (?, ?)', (1, 'easy'))
    cur.execute('INSERT OR IGNORE INTO Difficulties (id, name) VALUES (?, ?)', (2, 'normal'))
    cur.execute('INSERT OR IGNORE INTO Difficulties (id, name) VALUES (?, ?)', (3, 'hard'))
    for difficulty in range(3):
        for level in range(10):
            cur.execute(
                'INSERT OR IGNORE INTO High_scores (id, difficulty_id, level_num, score, date) VALUES (?, ?, ?, ?, ?)',
                (((difficulty * 10) + (level + 1)),
                 difficulty + 1, level + 1, 0, None))
    con.commit()


def connect_to_db(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    return con, cur


def update_stats(difficulty, level_num, score):
    con, cur = connect_to_db('..\\statistics\\player_statistics.db')
    high_scores_id, org_score = cur.execute(
        'SELECT High_scores.id, score FROM High_scores JOIN Difficulties ON High_scores.difficulty_id = Difficulties.id'
        ' WHERE Difficulties.name = ? AND High_scores.level_num = ?',
        (difficulty, level_num)).fetchone()
    if org_score >= score:
        return
    cur.execute('UPDATE High_scores SET score = ?, date = ? WHERE id = ?', (score, datetime.now(), high_scores_id))
    con.commit()
