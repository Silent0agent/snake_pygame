import pygame

from utils import connect_to_db


def draw_score(number, screen):
    font = pygame.font.Font('..\\assets\\fonts\\segoeprint.ttf', 28)
    string_rendered = font.render(f'Очки: {number}', 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 755
    intro_rect.x = 575
    screen.blit(string_rendered, intro_rect)


def draw_record(difficulty, level_num, screen):
    con, cur = connect_to_db('..\\statistics\\player_statistics.db')
    number = cur.execute(
        'SELECT score FROM High_scores JOIN Difficulties ON High_scores.difficulty_id = Difficulties.id '
        'WHERE name = ? AND level_num = ?',
        (difficulty, level_num)).fetchone()[0]
    font = pygame.font.Font('..\\assets\\fonts\\segoeprint.ttf', 20)
    string_rendered = font.render(f'Рекорд: {number}', 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 740
    intro_rect.x = 575
    screen.blit(string_rendered, intro_rect)


def draw_pause_hints(screen, pause_flag):
    font = pygame.font.Font('..\\assets\\fonts\\segoeprint.ttf', 20)
    if not pause_flag:
        string_rendered = font.render(f"Нажмите 'p' для паузы", 1, (255, 106, 0))
    else:
        string_rendered = font.render(f"ПАУЗА", 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 740
    if not pause_flag:
        intro_rect.x = 0
    else:
        intro_rect.x = 350
    screen.blit(string_rendered, intro_rect)


def draw_game_over_hints(screen):
    font = pygame.font.Font('..\\assets\\fonts\\segoeprint.ttf', 20)
    string_rendered = font.render(f"Нажмите 'r', чтобы переиграть", 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 740
    intro_rect.x = 0
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render(f"Нажмите 'ESC', чтобы выйти на главный экран", 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 764
    intro_rect.x = 0
    screen.blit(string_rendered, intro_rect)
