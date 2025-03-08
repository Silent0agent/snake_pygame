from utils import *
from sprites import *
from settings import *
from render import render_scheme


def start_screen_1(screen, clock):
    fon = pygame.transform.scale(load_image('background_images\\menu_screens\\main_menu.jpg'), (WIDTH, HEIGHT))
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
    fon = pygame.transform.scale(load_image('background_images\\menu_screens\\difficulty_choose_menu.jpg'),
                                 (WIDTH, HEIGHT))
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
    fon = pygame.transform.scale(
        load_image('background_images\\menu_screens\\level_choose_menu.jpg'), (WIDTH, HEIGHT))
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
    font = pygame.font.Font('..\\assets\\fonts\\segoeprint.ttf', 70)
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
        render_scheme(level)
        mini_tiles_group.draw(screen)
        pygame.display.flip()
        clock.tick(START_SCREENS_FPS)


def stats_screen(screen, clock):
    with open('..\\statistics\\stats.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
    intro_text = [line.rstrip() for line in lines]
    easy = intro_text[0:11]
    normal = intro_text[11:22]
    hard = intro_text[22:33]

    font = pygame.font.Font('..\\assets\\fonts\\segoeprint.ttf', 20)
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
    global current_sprite_sheet, current_empty_image, current_apple_image, current_wall_image
    snake_changed_flag = True
    fon = pygame.transform.scale(load_image('background_images\\menu_screens\\settings_menu.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    def load_sprites(current_sprite_sheet, current_empty_image, current_apple_image, current_wall_image):
        cut_sprite_sheet(load_image(sprites_sheets[current_sprite_sheet]), 5, 4, current_snake_images)
        current_images['empty'] = load_image(empty_images[current_empty_image])
        current_images['apple'] = load_image(apple_images[current_apple_image])
        current_images['wall'] = load_image(wall_images[current_wall_image])

    def draw_sprites():
        SnakePart('end_left', 1, 2, scaled=False)
        SnakePart('horizontal', 2, 2, scaled=False)
        SnakePart('head_right', 3, 2, scaled=False)
        Tile('empty', 2, 6, scaled=False)
        Apple(2, 9, scaled=False)
        Tile('wall', 2, 12, scaled=False)
        all_sprites.draw(screen)
        if snake_changed_flag:
            for spr in animated_group:
                spr.kill()
            AnimatedSnakeShowcase(10.5, 2)
        else:
            animated_group.update()
        animated_group.draw(screen)

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
                        snake_changed_flag = True
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
                        snake_changed_flag = True
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
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        load_sprites(current_sprite_sheet, current_empty_image, current_apple_image, current_wall_image)
        draw_sprites()
        snake_changed_flag = False
        clock.tick(START_SCREENS_FPS)
