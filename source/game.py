from screens import *
from draw import *
from snake import Snake
from render import render_level
from utils import init_db


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill((0, 0, 0))
        pygame.display.set_caption('Twisty Zapper')
        self.clock = pygame.time.Clock()
        self.fps = 60

    def play(self):
        global music_menu_flag
        pygame.init()
        pygame.mixer.init()
        init_db('..\\statistics\\player_statistics.db')
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill((0, 0, 0))
        pygame.display.set_caption('Twisty Zapper')
        clock = pygame.time.Clock()
        fps = 60
        menu_music('background_music\\menu_music.mp3', 0.1, music_menu_flag)
        music_menu_flag = False
        pause_flag = False
        ongoing = 'continue'
        mode = start_screen_1(screen, clock)
        if mode == 'play':
            difficulty = start_screen_2(screen, clock)  # от сложности зависит fps
            if difficulty == 'escape':
                reset_sprites()
                return True
            if difficulty == 'easy':
                fps = 6
            elif difficulty == 'normal':
                fps = 9
            elif difficulty == 'hard':
                fps = 14
            start_level, level_num, start_snake_coords = start_screen_3(screen, clock, difficulty)
            if start_level == 'escape':
                return True
            level = [i[:] for i in start_level[:]]
            for spr in mini_tiles_group:
                spr.kill()
            snake = Snake(start_snake_coords[:])
            direction = 'right'
            snake.create_apple(level)
            running = True
            snake_alive = True
            game_over_flag = False
            start_music('background_music\\game_music.wav', 0.1)
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
                            snake.create_apple(level)
                            start_music('background_music\\game_music.wav', 0.1)
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
                            return True

                if not pause_flag:
                    snake.change_direction(direction)
                    screen.fill((0, 0, 0))
                    render_level(level, snake)
                    if snake_alive:
                        ongoing = snake.move(level)
                    if ongoing == 'game_over' or ongoing == 'win':
                        snake_alive = False
                    if not snake_alive:
                        if not game_over_flag:
                            GameOver(type=ongoing)
                            pygame.mixer.music.stop()
                            load_sound('sound_effects\\game_over.mp3').play()
                            game_over_flag = True
                    game_over_group.update()
                    particle_group.update()
                    animated_group.update()
                    # Рисование всех спрайтов
                    all_sprites.draw(screen)
                    animated_group.draw(screen)
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
            return True
        elif mode == 'settings':
            screen.fill((0, 0, 0))
            settings_screen(screen, clock)
            reset_sprites()
            for spr in animated_group:
                spr.kill()
            return True
