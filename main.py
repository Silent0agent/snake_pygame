import os
import random
import sys

import pygame

WIDTH, HEIGHT = 750, 800  # размеры окна
TILE_SIZE = 25  # размер игровой плитки
MINI_TILE_SIZE = 15  # размер плитки схемы уровня
START_SCREENS_FPS = 10

music_menu_flag = True

all_sprites = pygame.sprite.Group()
mini_tiles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()
horizontal_borders_group = pygame.sprite.Group()
vertical_borders_group = pygame.sprite.Group()

# Следующие группы не относятся к all_sprites
particle_group = pygame.sprite.Group()
game_over_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def load_sound(name):
    fullname = os.path.join('data', 'sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    sound = pygame.mixer.Sound(fullname)
    return sound


def start_music(name, volume):
    fullname = os.path.join('data', 'sounds', name)
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
    load_sound('click.mp3').play()


def spawn_particles_on_eat(x, y):
    color = (240, 0, 0)
    for _ in range(10):  # 10 частиц за раз
        particle = Particle(x, y, color)
        particle_group.add(particle)


# Функция для создания частиц при ударе об стену
def spawn_particles_on_wall_collision(x, y):
    color = (0, 0, 0)
    for _ in range(20):  # Больше частиц при ударе о стену
        particle = Particle(x, y, color)
        particle_group.add(particle)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


sprites_sheets = ['sprites_sheet_1.png', 'sprites_sheet_2.png']
empty_images = ['tile1.jpg', 'tile2.jpg', 'tile3.jpg']
wall_images = ['wall1.jpg', 'wall2.jpg']
apple_images = ['apple1.png', 'apple2.png']
snake_images = {}
other_images = {'empty': load_image('tile1.jpg'),
                'wall': load_image('wall1.jpg'),
                'apple': load_image('apple1.png')}


def cut_sheet(sheet, columns, rows):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    frame_location = (0, 0)
    snake_images['angle1'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (0, 50)
    snake_images['angle2'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (100, 0)
    snake_images['angle3'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (100, 100)
    snake_images['angle4'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (50, 0)
    snake_images['horizontal'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (100, 50)
    snake_images['vertical'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 0)
    snake_images['head_up'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 0)
    snake_images['head_right'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 50)
    snake_images['head_left'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 50)
    snake_images['head_down'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 100)
    snake_images['end_down'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 100)
    snake_images['end_left'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (150, 150)
    snake_images['end_right'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))
    frame_location = (200, 150)
    snake_images['end_up'] = sheet.subsurface(pygame.Rect(frame_location, rect.size))


cut_sheet(load_image('sprites_sheet_1.png'), 5, 4)


def reset_sprites():
    for spr in all_sprites:
        spr.kill()
    for spr in game_over_group:
        spr.kill()
    for spr in particle_group:
        spr.kill()


class Border(pygame.sprite.Sprite):  # класс Border используется, чтобы частицы не выходили за экран (критерий collide)
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders_group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders_group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__(particle_group)
        part_side = random.randint(3, 9)
        self.image = pygame.Surface((part_side, part_side))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x + 12, y + 12))
        self.lifetime = random.randint(5, 15)
        self.vel_x = random.uniform(-1, 2)
        self.vel_y = random.uniform(-1, 2)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.kill()  # Удаляем спрайт, когда его время жизни заканчивается
        elif (pygame.sprite.spritecollideany(self, vertical_borders_group) or
              pygame.sprite.spritecollideany(self, horizontal_borders_group)):
            self.kill()  # Удаляем спрайт, если он заходит за пределы игрового поля


class MiniTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(mini_tiles_group, all_sprites)
        tile_image = other_images[tile_type]
        scaled_image = pygame.transform.scale(tile_image, (
            int(tile_image.get_width() / 50 * MINI_TILE_SIZE), int(tile_image.get_height() / 50 * MINI_TILE_SIZE)))
        self.image = scaled_image
        self.rect = self.image.get_rect().move(
            150 + MINI_TILE_SIZE * pos_x, 125 + MINI_TILE_SIZE * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y, scaled=True):
        super().__init__(tiles_group, all_sprites)
        tile_image = other_images[tile_type]
        if scaled:
            scaled_image = pygame.transform.scale(tile_image, (
                int(tile_image.get_width() / 50 * TILE_SIZE), int(tile_image.get_height() / 50 * TILE_SIZE)))
            self.image = scaled_image
            self.rect = self.image.get_rect().move(
                TILE_SIZE * x, TILE_SIZE * y)
        else:
            self.image = tile_image
            self.rect = self.image.get_rect().move(
                50 * x, 50 * y)


class SnakePart(pygame.sprite.Sprite):
    def __init__(self, type, x, y, scaled=True):
        super().__init__(snake_group, all_sprites)
        self.frames = []
        snake_image = snake_images[type]
        if scaled:
            scaled_image = pygame.transform.scale(snake_image, (
                int(snake_image.get_width() / 50 * TILE_SIZE), int(snake_image.get_height() / 50 * TILE_SIZE)))
            self.image = scaled_image
            self.rect = self.image.get_rect().move(
                TILE_SIZE * x, TILE_SIZE * y)
        else:
            self.image = snake_image
            self.rect = self.image.get_rect().move(x * 50, y * 50)


class Snake:
    def __init__(self, snake_coords):
        self.snake_coords = snake_coords
        self.direction = 'right'
        self.score = 0
        self.forbidden_moves = {'up': 'down',
                                'down': 'up',
                                'left': 'right',
                                'right': 'left'}

    def change_direction(self, direction):
        if self.forbidden_moves[direction] != self.direction:
            self.direction = direction

    def move(self, level):
        last_x, last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        max_x_y = len(level) - 1
        if self.direction == 'right':
            if last_x + 1 > max_x_y:
                if level[last_y][0] == '#' or (0, last_y) in self.snake_coords:
                    return 'game_over'
                else:
                    self.snake_coords.append((0, last_y))
            elif level[last_y][last_x + 1] == '#' or (
                    last_x + 1, last_y) in self.snake_coords:
                return 'game_over'
            else:
                self.snake_coords.append((last_x + 1, last_y))
        elif self.direction == 'left':
            if last_x - 1 < 0:
                if level[last_y][max_x_y] == '#' or (max_x_y, last_y) in self.snake_coords:
                    return 'game_over'
                else:
                    self.snake_coords.append((max_x_y, last_y))
            elif level[last_y][last_x - 1] == '#' or (last_x - 1, last_y) in self.snake_coords:
                return 'game_over'
            else:
                self.snake_coords.append((last_x - 1, last_y))
        elif self.direction == 'up':
            if last_y - 1 < 0:
                if level[max_x_y][last_x] == '#' or (last_x, max_x_y) in self.snake_coords:
                    return 'game_over'
                else:
                    self.snake_coords.append((last_x, max_x_y))
            elif level[last_y - 1][last_x] == '#' or (last_x, last_y - 1) in self.snake_coords:
                return 'game_over'
            else:
                self.snake_coords.append((last_x, last_y - 1))
        elif self.direction == 'down':
            if last_y + 1 > len(level) - 1:
                if level[0][last_x] == '#' or (last_x, 0) in self.snake_coords:
                    return 'game_over'
                else:
                    self.snake_coords.append((last_x, 0))
            elif level[last_y + 1][last_x] == '#' or (last_x, last_y + 1) in self.snake_coords:
                return 'game_over'
            else:
                self.snake_coords.append((last_x, last_y + 1))
        new_last_x, new_last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        if level[new_last_y][new_last_x] != '@':
            self.snake_coords.pop(0)
        else:
            self.score += 1
            level[new_last_y][new_last_x] = '.'
            win = create_apple(level, self)
            spawn_particles_on_eat(new_last_x * TILE_SIZE, new_last_y * TILE_SIZE)
            load_sound('eat_food.mp3').play()
            if win:
                return 'win'
        return 'continue'


class Apple(pygame.sprite.Sprite):
    def __init__(self, x, y, scaled=True):
        super().__init__(all_sprites)
        self.pos_x = x
        self.pos_y = y
        image = other_images['apple']
        if scaled:
            scaled_image = pygame.transform.scale(image, (
                int(image.get_width() / 50 * TILE_SIZE), int(image.get_height() / 50 * TILE_SIZE)))
            self.image = scaled_image
            self.rect = self.image.get_rect().move(
                TILE_SIZE * x, TILE_SIZE * y)
        else:
            self.image = image
            self.rect = self.image.get_rect().move(x * 50, y * 50)


class GameOver(pygame.sprite.Sprite):
    def __init__(self, type='game_over'):
        super().__init__(game_over_group)
        if type == 'win':
            self.image = load_image('win_screen.jpg')
        else:
            self.image = load_image("game_over_screen.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = - WIDTH
        self.rect.y = 0
        self.angle = 0
        self.dx = 400

    def update(self):
        if self.rect.x < 0:
            self.rect.x += 50


def generate_scheme(level):
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == '.':
                MiniTile('empty', x, y)
            elif level[y][x] == '#':
                MiniTile('wall', x, y)


def start_screen_1(screen, clock):
    fon = pygame.transform.scale(load_image('menu_1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 125 <= x <= 630:
                    if 250 <= y <= 400:
                        click_sound()
                        return 'play'
                    elif 430 <= y <= 580:
                        click_sound()
                        return 'stats'
                    elif 610 <= y <= 760:
                        click_sound()
                        return 'settings'

        pygame.display.flip()
        clock.tick(START_SCREENS_FPS)


def start_screen_2(screen, clock):
    fon = pygame.transform.scale(load_image('menu_2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 190 <= x <= 560:
                    if 270 <= y <= 370:
                        click_sound()
                        return 'easy'
                    elif 430 <= y <= 530:
                        click_sound()
                        return 'normal'
                    elif 590 <= y <= 690:
                        click_sound()
                        return 'hard'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_sprites()
                    return 'escape'  # выход на главный экран
        pygame.display.flip()
        clock.tick(START_SCREENS_FPS)


def start_screen_3(screen, clock, difficulty):
    fon = pygame.transform.scale(load_image('menu_3.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    curlevel = 0
    first_num = '1'
    if difficulty == 'easy':
        first_num = '1'
    elif difficulty == 'normal':
        first_num = '2'
    elif difficulty == 'hard':
        first_num = '3'
    level = load_level(f'level{first_num}_{curlevel}.txt')
    font = pygame.font.Font('data/segoeprint.ttf', 70)
    string_rendered = font.render(str(curlevel + 1), 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    text_coord_x = 425
    text_coord_y = 575
    intro_rect.top = text_coord_y
    intro_rect.x = text_coord_x
    screen.blit(string_rendered, intro_rect)

    def draw_number(number, intro_rect):
        screen.blit(fon, (text_coord_x, text_coord_y),
                    (text_coord_x, text_coord_y, intro_rect.width, intro_rect.height))
        string_rendered = font.render(str(number), 1, (255, 106, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord_y
        intro_rect.x = text_coord_x
        screen.blit(string_rendered, intro_rect)
        return intro_rect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 0 <= x <= 50 and 270 + abs(x - 50) <= y <= 430 - abs(x - 50):
                    if curlevel != 0:
                        curlevel -= 1
                    else:
                        curlevel = 9
                    level = load_level(f'level{first_num}_{curlevel}.txt')
                    intro_rect = draw_number(curlevel + 1, intro_rect)
                    click_sound()
                elif 700 <= x <= 750 and 270 + abs(x - 700) <= y <= 430 - abs(x - 700):
                    if curlevel != 9:
                        curlevel += 1
                    else:
                        curlevel = 0
                    level = load_level(f'level{first_num}_{curlevel}.txt')
                    intro_rect = draw_number(curlevel + 1, intro_rect)
                    click_sound()
                elif 190 <= x <= 570 and 700 <= y <= 780:
                    # здесь задаются начальные координаты змейки
                    snake_coords = [(0, 0), (1, 0)]
                    click_sound()
                    return level, curlevel + 1, snake_coords
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_sprites()
                    return 'escape', 0, 0  # выход на главный экран
        generate_scheme(level)
        mini_tiles_group.draw(screen)
        pygame.display.flip()
        clock.tick(START_SCREENS_FPS)


def generate_level(level, snake):
    Border(0, 0, 0, HEIGHT - 50)
    Border(WIDTH, 0, WIDTH, HEIGHT - 50)
    Border(0, 0, WIDTH, 0)
    Border(0, HEIGHT - 50, WIDTH, HEIGHT - 50)
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                Apple(x, y)
    for i in range(len(snake.snake_coords)):
        x, y = snake.snake_coords[i][0], snake.snake_coords[i][1]
        max_x_y = len(level) - 1
        if i == 0:
            next_x, next_y = snake.snake_coords[i + 1][0], snake.snake_coords[i + 1][1]
            if not (x == 0 and next_x == max_x_y) and (x < next_x or (x == max_x_y and next_x == 0)):
                SnakePart('end_left', x, y)
            elif x > next_x or (x == 0 and next_x == max_x_y):
                SnakePart('end_right', x, y)
            elif not (y == 0 and next_y == max_x_y) and (y < next_y or (y == max_x_y and next_y == 0)):
                SnakePart('end_up', x, y)
            elif y > next_y or (y == 0 and next_y == max_x_y):
                SnakePart('end_down', x, y)
        elif i == len(snake.snake_coords) - 1:
            if snake.direction == 'right':
                SnakePart('head_right', x, y)
            elif snake.direction == 'left':
                SnakePart('head_left', x, y)
            elif snake.direction == 'up':
                SnakePart('head_up', x, y)
            elif snake.direction == 'down':
                SnakePart('head_down', x, y)
        else:
            next_x, next_y = snake.snake_coords[i + 1][0], snake.snake_coords[i + 1][1]
            prev_x, prev_y = snake.snake_coords[i - 1][0], snake.snake_coords[i - 1][1]
            # если змейка заходит за границы, меняем значения координат следующего/прошлого куска в переменных
            if x == 0 and next_x == max_x_y:
                next_x = -1
            elif x == 0 and prev_x == max_x_y:
                prev_x = -1
            elif x == max_x_y and next_x == 0:
                next_x = x + 1
            elif x == max_x_y and prev_x == 0:
                prev_x = x + 1
            if y == 0 and next_y == max_x_y:
                next_y = -1
            elif y == 0 and prev_y == max_x_y:
                prev_y = -1
            elif y == max_x_y and next_y == 0:
                next_y = y + 1
            elif y == max_x_y and prev_y == 0:
                prev_y = y + 1

            if prev_x == x == next_x:
                SnakePart('vertical', x, y)
            elif prev_y == y == next_y:
                SnakePart('horizontal', x, y)
            elif (prev_x < x and y < next_y) or (next_x < x and y < prev_y):
                SnakePart('angle3', x, y)
            elif (prev_y > y and x < next_x) or (next_y > y and x < prev_x):
                SnakePart('angle1', x, y)
            elif (prev_y < y and x > next_x) or (next_y < y and x > prev_x):
                SnakePart('angle4', x, y)
            elif (prev_x > x and y > next_y) or (next_x > x and y > prev_y):
                SnakePart('angle2', x, y)


def create_apple(level, snake):
    snake_coords = snake.snake_coords
    free_cells = []
    rows = len(level)
    cols = len(level[0])

    for row in range(rows):
        for col in range(cols):
            if level[row][col] == '.' and (row, col) not in snake_coords:
                free_cells.append((row, col))

    # Случайно выбираем одну из свободных клеток
    if free_cells:
        apple_row, apple_col = random.choice(free_cells)
        level[apple_row][apple_col] = '@'
        return False
    return True  # победа если нет места для яблока


def draw_score(number, screen):
    font = pygame.font.Font('data/segoeprint.ttf', 28)
    string_rendered = font.render(f'Очки: {number}', 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 755
    intro_rect.x = 575
    screen.blit(string_rendered, intro_rect)


def draw_record(difficulty, level_num, screen):
    difficulty_num = '1'
    if difficulty == 'easy':
        difficulty_num = '1'
    elif difficulty == 'normal':
        difficulty_num = '2'
    elif difficulty == 'hard':
        difficulty_num = '3'
    with open('stats.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
    line_number = level_num + int(difficulty_num) - 1 + (int(difficulty_num) - 1) * 10
    number = int(lines[line_number].rstrip().split(':')[1][1:])
    font = pygame.font.Font('data/segoeprint.ttf', 20)
    string_rendered = font.render(f'Рекорд: {number}', 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 740
    intro_rect.x = 575
    screen.blit(string_rendered, intro_rect)


def draw_pause_hints(screen, pause_flag):
    font = pygame.font.Font('data/segoeprint.ttf', 20)
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
    font = pygame.font.Font('data/segoeprint.ttf', 20)
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


def update_stats(difficulty, level_num, score):
    difficulty_num = '1'
    if difficulty == 'easy':
        difficulty_num = '1'
    elif difficulty == 'normal':
        difficulty_num = '2'
    elif difficulty == 'hard':
        difficulty_num = '3'
    with open('stats.txt', 'r', encoding='UTF-8') as file:
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
    with open('stats.txt', 'w', encoding='UTF-8') as file:
        file.writelines(lines)


def stats_screen(screen, clock):
    with open('stats.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
    intro_text = [line.rstrip() for line in lines]
    easy = intro_text[0:11]
    normal = intro_text[11:22]
    hard = intro_text[22:33]

    font = pygame.font.Font('data/segoeprint.ttf', 20)
    stats_color = (255, 106, 0)

    def draw(x, start_y, text_list, color):
        text_coord = start_y
        for line in text_list:
            string_rendered = font.render(line, 1, color)
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = x
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    draw(10, 0, easy, stats_color)
    draw(400, 0, normal, stats_color)
    draw(200, 400, hard, stats_color)
    draw(425, 760, ['Нажмите ESC, чтобы выйти'], (255, 255, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_sprites()
                    return  # выход на главный экран
        pygame.display.flip()
        clock.tick(START_SCREENS_FPS)


def settings_screen(screen, clock):
    fon = pygame.transform.scale(load_image('settings_screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    current_sprite_sheet = 0
    current_empty_image = 0
    current_apple_image = 0
    current_wall_image = 0

    def load_sprites(current_sprite_sheet, current_empty_image, current_apple_image, current_wall_image):
        cut_sheet(load_image(sprites_sheets[current_sprite_sheet]), 5, 4)
        other_images['empty'] = load_image(empty_images[current_empty_image])
        other_images['apple'] = load_image(apple_images[current_apple_image])
        other_images['wall'] = load_image(wall_images[current_wall_image])

    def draw_sprites():
        SnakePart('end_left', 1, 2, scaled=False)
        SnakePart('horizontal', 2, 2, scaled=False)
        SnakePart('head_right', 3, 2, scaled=False)
        Tile('empty', 2, 6, scaled=False)
        Apple(2, 9, scaled=False)
        Tile('wall', 2, 12, scaled=False)
        all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 400 <= x <= 550:
                    if 25 <= y <= 80:
                        if current_sprite_sheet == 0:
                            current_sprite_sheet = len(sprites_sheets) - 1
                        else:
                            current_sprite_sheet -= 1
                        click_sound()
                    elif 190 <= y <= 245:
                        if current_empty_image == 0:
                            current_empty_image = len(empty_images) - 1
                        else:
                            current_empty_image -= 1
                        click_sound()
                    elif 360 <= y <= 420:
                        if current_apple_image == 0:
                            current_apple_image = len(apple_images) - 1
                        else:
                            current_apple_image -= 1
                        click_sound()
                    elif 530 <= y <= 580:
                        if current_wall_image == 0:
                            current_wall_image = len(wall_images) - 1
                        else:
                            current_wall_image -= 1
                        click_sound()
                elif 565 <= x <= 710:
                    if 25 <= y <= 80:
                        if current_sprite_sheet == len(sprites_sheets) - 1:
                            current_sprite_sheet = 0
                        else:
                            current_sprite_sheet += 1
                        click_sound()
                    elif 190 <= y <= 245:
                        if current_empty_image == len(empty_images) - 1:
                            current_empty_image = 0
                        else:
                            current_empty_image += 1
                        click_sound()
                    elif 360 <= y <= 420:
                        if current_apple_image == len(apple_images) - 1:
                            current_apple_image = 0
                        else:
                            current_apple_image += 1
                        click_sound()
                    elif 530 <= y <= 580:
                        if current_wall_image == len(wall_images) - 1:
                            current_wall_image = 0
                        else:
                            current_wall_image += 1
                        click_sound()
                if 500 <= x <= 700 and 700 <= y <= 780:
                    click_sound()
                    current_sprite_sheet, current_empty_image, current_apple_image, current_wall_image = 0, 0, 0, 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_sprites()
                    return  # выход на главный экран
        pygame.display.flip()
        reset_sprites()
        load_sprites(current_sprite_sheet, current_empty_image, current_apple_image, current_wall_image)
        draw_sprites()
        clock.tick(START_SCREENS_FPS)


def play():
    global music_menu_flag
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Twisty Zapper')
    clock = pygame.time.Clock()
    fps = 60
    menu_music('menu_music.mp3', 0.1, music_menu_flag)
    music_menu_flag = False
    pause_flag = False
    ongoing = 'continue'
    mode = start_screen_1(screen, clock)
    if mode == 'play':
        difficulty = start_screen_2(screen, clock)  # от сложности зависит fps
        if difficulty == 'escape':
            reset_sprites()
            return True  # конец функции play
        if difficulty == 'easy':
            fps = 6
        elif difficulty == 'normal':
            fps = 9
        elif difficulty == 'hard':
            fps = 14
        start_level, level_num, start_snake_coords = start_screen_3(screen, clock, difficulty)
        if start_level == 'escape':
            return True  # конец функции play
        level = [i[:] for i in start_level[:]]
        for spr in mini_tiles_group:
            spr.kill()
        snake = Snake(start_snake_coords[:])
        direction = 'right'
        create_apple(level, snake)
        running = True
        snake_alive = True
        game_over_flag = False
        start_music('game_music.wav', 0.1)
        while running:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if snake_alive:
                        if event.key == pygame.K_LEFT:
                            direction = 'left'
                        elif event.key == pygame.K_RIGHT:
                            direction = 'right'
                        elif event.key == pygame.K_UP:
                            direction = 'up'
                        elif event.key == pygame.K_DOWN:
                            direction = 'down'
                    if event.key == pygame.K_r:
                        # перезапуск уровня
                        snake_alive = True
                        game_over_flag = False
                        pause_flag = False
                        reset_sprites()
                        direction = 'right'
                        level = [i[:] for i in start_level[:]]
                        snake = Snake(start_snake_coords[:])
                        create_apple(level, snake)
                        start_music('game_music.wav', 0.1)
                    elif event.key == pygame.K_p:
                        # пауза
                        if snake_alive:
                            if not pause_flag:
                                pause_flag = True
                                draw_pause_hints(screen, pause_flag)
                            else:
                                pause_flag = False
                    elif event.key == pygame.K_ESCAPE:
                        # выход на главный экран
                        reset_sprites()
                        pygame.mixer.music.stop()
                        music_menu_flag = True
                        return True  # конец функции play

            if not pause_flag:
                snake.change_direction(direction)
                screen.fill((0, 0, 0))
                generate_level(level, snake)
                if snake_alive:
                    ongoing = snake.move(level)
                if ongoing == 'game_over' or ongoing == 'win':
                    snake_alive = False
                if not snake_alive:
                    if not game_over_flag:
                        GameOver(type=ongoing)
                        pygame.mixer.music.stop()
                        load_sound('game_over.mp3').play()
                        game_over_flag = True
                game_over_group.update()
                particle_group.update()
                # Рисование всех спрайтов
                all_sprites.draw(screen)
                particle_group.draw(screen)
                game_over_group.draw(screen)
                if game_over_flag:
                    draw_game_over_hints(screen)
                else:
                    draw_pause_hints(screen, pause_flag)
                draw_score(snake.score, screen)
                update_stats(difficulty, level_num, snake.score)
                draw_record(difficulty, level_num, screen)
                pygame.display.flip()
                for spr in all_sprites:
                    spr.kill()
            else:
                draw_pause_hints(screen, pause_flag)
                pygame.display.flip()
    elif mode == 'stats':
        screen.fill((0, 0, 0))
        stats_screen(screen, clock)
        reset_sprites()
        return True  # конец функции play
    elif mode == 'settings':
        screen.fill((0, 0, 0))
        settings_screen(screen, clock)
        reset_sprites()
        return True  # конец функции play


def main():
    retry = play()
    if retry:
        main()


if __name__ == '__main__':
    main()
