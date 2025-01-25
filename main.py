import os
import sys

import pygame
import random

WIDTH, HEIGHT = 750, 800  # размеры окна
TILE_SIZE = 25  # размер игровой плитки
START_SCREENS_FPS = 10

all_sprites = pygame.sprite.Group()
mini_tiles_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()
game_over_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


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


tile_images = {'empty': load_image('tile.jpg'),
               'wall': load_image('wall.jpg')}
snake_images = {}
apple_image = []


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
    frame_location = (0, 150)
    apple_image.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))


cut_sheet(load_image('sprites_sheet_1.png'), 5, 4)


def reset_sprites():
    for spr in all_sprites:
        spr.kill()
    for spr in game_over_group:
        spr.kill()


class MiniTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(mini_tiles_group, all_sprites)
        tile_image = tile_images[tile_type]
        scaled_image = pygame.transform.scale(tile_image, (
            int(tile_image.get_width() / 50 * 15), int(tile_image.get_height() / 50 * 15)))
        self.image = scaled_image
        self.rect = self.image.get_rect().move(
            150 + 15 * pos_x, 125 + 15 * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        tile_image = tile_images[tile_type]
        scaled_image = pygame.transform.scale(tile_image, (
            int(tile_image.get_width() / 50 * 25), int(tile_image.get_height() / 50 * 25)))
        self.image = scaled_image
        self.rect = self.image.get_rect().move(
            25 * pos_x, 25 * pos_y)


class SnakePart(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(snake_group, all_sprites)
        self.frames = []
        snake_image = snake_images[type]
        scaled_image = pygame.transform.scale(snake_image, (
            int(snake_image.get_width() / 50 * 25), int(snake_image.get_height() / 50 * 25)))
        self.image = scaled_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * 25, y * 25)


class Snake:
    def __init__(self, snake_coords):
        self.snake_coords = snake_coords
        self.direction = 'right'
        self.score = 0
        self.unavailable_moves = {'up': 'down',
                                  'down': 'up',
                                  'left': 'right',
                                  'right': 'left'}

    def change_direction(self, direction):
        if self.unavailable_moves[direction] != self.direction:
            self.direction = direction

    def move(self, level):
        last_x, last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        if self.direction == 'right':
            if last_x + 1 > len(level) - 1 or level[last_y][last_x + 1] == '#':
                return 'game_over'
            self.snake_coords.append((last_x + 1, last_y))
        elif self.direction == 'left':
            if last_x - 1 < 0 or level[last_y][last_x - 1] == '#' or (last_x - 1, last_y) in self.snake_coords:
                return 'game_over'
            self.snake_coords.append((last_x - 1, last_y))
        elif self.direction == 'up':
            if last_y - 1 < 0 or level[last_y - 1][last_x] == '#' or (last_x, last_y - 1) in self.snake_coords:
                return 'game_over'
            self.snake_coords.append((last_x, last_y - 1))
        elif self.direction == 'down':
            if last_y + 1 > len(level) - 1 or level[last_y + 1][last_x] == '#' or (
                    last_x, last_y + 1) in self.snake_coords:
                return 'game_over'
            self.snake_coords.append((last_x, last_y + 1))
        new_last_x, new_last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        if level[new_last_y][new_last_x] != '@':
            self.snake_coords.pop(0)
        else:
            self.score += 1
            level[new_last_y][new_last_x] = '.'
            create_apple(level, self)
        return 'continue'


class Apple(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.pos_x = x
        self.pos_y = y
        image = apple_image[0]
        scaled_image = pygame.transform.scale(image, (
            int(image.get_width() / 50 * 25), int(image.get_height() / 50 * 25)))
        self.image = scaled_image
        self.rect = self.image.get_rect().move(
            TILE_SIZE * x, TILE_SIZE * y)


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_over_group)
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
                if 125 <= x < 630 and 250 <= y <= 400:
                    return 'play'
                elif 125 <= x <= 630 and 430 <= y <= 580:
                    return 'stats'
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
                        return 'easy'
                    elif 430 <= y <= 530:
                        return 'normal'
                    elif 590 <= y <= 690:
                        return 'hard'
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
                if 0 <= x <= 50 and 270 <= y <= 430:
                    if curlevel != 0:
                        curlevel -= 1
                    else:
                        curlevel = 9
                    level = load_level(f'level{first_num}_{curlevel}.txt')
                    intro_rect = draw_number(curlevel + 1, intro_rect)
                elif 700 <= x <= 750 and 270 <= y <= 430:
                    if curlevel != 9:
                        curlevel += 1
                    else:
                        curlevel = 0
                    level = load_level(f'level{first_num}_{curlevel}.txt')
                    intro_rect = draw_number(curlevel + 1, intro_rect)
                elif 190 <= x <= 570 and 700 <= y <= 780:
                    # здесь задаются начальные координаты змейки
                    snake_coords = [(0, 0), (1, 0)]
                    return level, curlevel + 1, snake_coords
        generate_scheme(level)
        mini_tiles_group.draw(screen)
        pygame.display.flip()
        clock.tick(START_SCREENS_FPS)


def generate_level(level, snake):
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
        if i == 0:
            next_x, next_y = snake.snake_coords[i + 1][0], snake.snake_coords[i + 1][1]
            if x < next_x:
                SnakePart('end_left', x, y)
            elif x > next_x:
                SnakePart('end_right', x, y)
            elif y < next_y:
                SnakePart('end_up', x, y)
            elif y > next_y:
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
    else:
        print("Нет места для яблока!")


def draw_score(number, screen):
    font = pygame.font.Font('data/segoeprint.ttf', 35)
    string_rendered = font.render(f'Очки: {number}', 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    text_coord_x = 520
    text_coord_y = 745
    intro_rect.top = text_coord_y
    intro_rect.x = text_coord_x
    screen.blit(string_rendered, intro_rect)


def draw_hints(screen):
    font = pygame.font.Font('data/segoeprint.ttf', 20)
    string_rendered = font.render(f"Нажмите 'p', чтобы переиграть", 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 735
    intro_rect.x = 0
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render(f"Нажмите 'ESC', чтобы выйти на главный экран", 1, (255, 106, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 760
    intro_rect.x = 0
    screen.blit(string_rendered, intro_rect)


def update_stats(difficulty, level_num, score):
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

    def draw(x, start_y, text_list):
        text_coord = start_y
        for line in text_list:
            string_rendered = font.render(line, 1, (255, 106, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 1
            intro_rect.top = text_coord
            intro_rect.x = x
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    draw(10, 0, easy)
    draw(400, 0, normal)
    draw(200, 400, hard)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(START_SCREENS_FPS)


def play():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Twisty Zapper')
    clock = pygame.time.Clock()
    mode = start_screen_1(screen, clock)
    if mode == 'play':
        difficulty = start_screen_2(screen, clock)  # от сложности зависит fps
        if difficulty == 'easy':
            fps = 6
        elif difficulty == 'normal':
            fps = 10
        elif difficulty == 'hard':
            fps = 15
        start_level, level_num, start_snake_coords = start_screen_3(screen, clock, difficulty)
        level = [i[:] for i in start_level[:]]
        for spr in mini_tiles_group:
            spr.kill()
        snake = Snake(start_snake_coords[:])
        direction = 'right'
        create_apple(level, snake)
        running = True
        snake_alive = True
        game_over_flag = False
        pygame.init()
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
                    elif event.key == pygame.K_p:
                        screen.fill((0, 0, 0))
                        snake_alive = True
                        game_over_flag = False
                        reset_sprites()
                        level = [i[:] for i in start_level[:]]
                        snake = Snake(start_snake_coords[:])
                        create_apple(level, snake)
                    elif event.key == pygame.K_ESCAPE:
                        reset_sprites()
                        return True  # конец функции play
            snake.change_direction(direction)
            screen.fill((0, 0, 0))
            generate_level(level, snake)
            if snake_alive:
                ongoing = snake.move(level)
            if ongoing == 'game_over':
                snake_alive = False
            if not snake_alive:
                if not game_over_flag:
                    GameOver()
                    game_over_flag = True
            game_over_group.update()
            all_sprites.draw(screen)
            game_over_group.draw(screen)
            if game_over_flag:
                draw_hints(screen)
            draw_score(snake.score, screen)
            update_stats(difficulty, level_num, snake.score)
            pygame.display.flip()
            for spr in all_sprites:
                spr.kill()
    elif mode == 'stats':
        screen.fill((0, 0, 0))
        stats_screen(screen, clock)
        reset_sprites()
        return True  # конец функции play


def main():
    retry = play()
    if retry:
        main()


if __name__ == '__main__':
    main()
