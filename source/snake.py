import random

import pygame

from settings import TILE_SIZE, animated_group
from utils import load_sound
from render import render_particles_on_eat, render_particles_on_collision, render_particles_on_boom


class Snake:
    def __init__(self, snake_coords):
        self.shield_active = False
        self.shield_end_time = 0
        self.snake_coords = snake_coords
        self.direction = 'right'
        self.score = 0
        self.forbidden_moves = {'up': 'down',
                                'down': 'up',
                                'left': 'right',
                                'right': 'left'}
        self.apple_types = {'normal': '@',
                            'bomb': 'b',
                            'swap_head': 's',
                            'multi_fake': 'm',
                            'invincible': 'i',
                            'rock': 'r',
                            'fake': 'f'}

    def create_apple(self, level):
        for spr in animated_group:
            spr.kill()
        free_cells = []
        rows = len(level)
        cols = len(level[0])

        for row in range(rows):
            for col in range(cols):
                if level[row][col] == '.' and (col, row) not in self.snake_coords:
                    free_cells.append((row, col))

        # Случайно выбираем одну из свободных клеток
        if free_cells:
            weights = [0.4, 0.2, 0.1, 0.15, 0.05, 0.1]
            possible_apples = list(self.apple_types.keys())[:-1]
            if self.shield_active:
                possible_apples.remove('invincible')
            apple_type = random.choices(list(self.apple_types.keys())[:-1], weights=weights)[0]
            apple_row, apple_col = random.choice(free_cells)
            level[apple_row][apple_col] = self.apple_types[apple_type]  # @, b, s
            pos = (apple_row, apple_col)
            if apple_type == 'multi_fake':
                free_cells.remove(pos)
                for i in range(random.randrange(3, 5)):
                    if free_cells:
                        apple_row, apple_col = random.choice(free_cells)
                        level[apple_row][apple_col] = 'f'
                        free_cells.remove((apple_row, apple_col))
                    else:
                        break
                load_sound('\\sound_effects\\among_us.mp3').play()
            return pos
        return True  # победа если нет места для яблока

    def change_direction(self, direction):
        if self.forbidden_moves[direction] != self.direction:
            self.direction = direction

    def move(self, level):
        current_time = pygame.time.get_ticks()

        # Проверяем активность щита
        if self.shield_active and current_time > self.shield_end_time:
            self.shield_active = False

        last_x, last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        max_x_y = len(level) - 1
        if self.direction == 'right':
            if last_x + 1 > max_x_y:
                if (level[last_y][0] == '#' or (0, last_y) in self.snake_coords) and not self.shield_active:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE - 5,
                                                  self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                    return 'game_over'
                else:
                    self.snake_coords.append((0, last_y))
            elif (level[last_y][last_x + 1] == '#' or (
                    last_x + 1, last_y) in self.snake_coords) and not self.shield_active:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE - 5,
                                              self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                return 'game_over'
            else:
                self.snake_coords.append((last_x + 1, last_y))
        elif self.direction == 'left':
            if last_x - 1 < 0:
                if (level[last_y][max_x_y] == '#' or (max_x_y, last_y) in self.snake_coords) and not self.shield_active:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE,
                                                  self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                    return 'game_over'
                else:
                    self.snake_coords.append((max_x_y, last_y))
            elif (level[last_y][last_x - 1] == '#' or (last_x - 1, last_y) in self.snake_coords) and not self.shield_active:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE,
                                              self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                return 'game_over'
            else:
                self.snake_coords.append((last_x - 1, last_y))
        elif self.direction == 'up':
            if last_y - 1 < 0:
                if (level[max_x_y][last_x] == '#' or (last_x, max_x_y) in self.snake_coords) and not self.shield_active:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE // 2,
                                                  self.snake_coords[-1][1] * TILE_SIZE)
                    return 'game_over'
                else:
                    self.snake_coords.append((last_x, max_x_y))
            elif (level[last_y - 1][last_x] == '#' or (last_x, last_y - 1) in self.snake_coords) and not self.shield_active:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE // 2,
                                              self.snake_coords[-1][1] * TILE_SIZE)
                return 'game_over'
            else:
                self.snake_coords.append((last_x, last_y - 1))
        elif self.direction == 'down':
            if last_y + 1 > len(level) - 1:
                if (level[0][last_x] == '#' or (last_x, 0) in self.snake_coords) and not self.shield_active:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE,
                                                  self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE - 5)
                    return 'game_over'
                else:
                    self.snake_coords.append((last_x, 0))
            elif (level[last_y + 1][last_x] == '#' or (last_x, last_y + 1) in self.snake_coords) and not self.shield_active:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE // 2,
                                              self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE - 5)
                return 'game_over'
            else:
                self.snake_coords.append((last_x, last_y + 1))
        new_last_x, new_last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        if level[new_last_y][new_last_x] not in self.apple_types.values():
            self.snake_coords.pop(0)
        else:
            apple_value = level[new_last_y][new_last_x]
            level[new_last_y][new_last_x] = '.'
            win = False
            if apple_value == '@':
                self.score += 1
                render_particles_on_eat(new_last_x * TILE_SIZE, new_last_y * TILE_SIZE)
                load_sound('\\sound_effects\\eat_food.mp3').play()
                win = self.create_apple(level)
            elif apple_value == 'b':
                self.score += 1
                render_particles_on_boom(new_last_x * TILE_SIZE, new_last_y * TILE_SIZE)
                self.explode_walls(level, new_last_x, new_last_y)
                load_sound('\\sound_effects\\explosion.mp3').play()
                win = self.create_apple(level)
            elif apple_value == 's':
                self.score += 1
                render_particles_on_eat(new_last_x * TILE_SIZE, new_last_y * TILE_SIZE)
                self.swap_head(level)
                load_sound('\\sound_effects\\swap_head.mp3').play()
                win = self.create_apple(level)
            elif apple_value == 'm':
                self.score += 1
                render_particles_on_eat(new_last_x * TILE_SIZE, new_last_y * TILE_SIZE)
                load_sound('\\sound_effects\\eat_food.mp3').play()
                for y in range(len(level)):
                    for x in range(len(level[0])):
                        if level[y][x] == 'f':
                            level[y][x] = '.'
                win = self.create_apple(level)
            elif apple_value == 'i':
                self.score += 1
                self.shield_active = True
                self.shield_end_time = pygame.time.get_ticks() + 5000  # 5 секунд
                load_sound('\\sound_effects\\power.mp3').play()
                win = self.create_apple(level)
            elif apple_value == 'r':
                self.score += 3
                if len(self.snake_coords) > 3:
                    wall_coordinates = self.snake_coords[:len(self.snake_coords)//2]
                    self.snake_coords = self.snake_coords[len(self.snake_coords) // 2:]
                    for x, y in wall_coordinates:
                        level[y][x] = '#'
                load_sound('\\sound_effects\\vine_boom.mp3').play()
                win = self.create_apple(level)
            elif apple_value == 'f':
                if self.score > 0:
                    self.score -= 1
                render_particles_on_eat(new_last_x * TILE_SIZE, new_last_y * TILE_SIZE, color=(127, 94, 0))
                self.snake_coords.pop(0)
                if len(self.snake_coords) > 2:
                    self.snake_coords.pop(0)
                load_sound('\\sound_effects\\fart.mp3').play()
            if win is True:
                return 'win'
        return 'continue'

    def explode_walls(self, level, x, y):
        """Взрывает стены в радиусе 3 клеток."""
        radius = 3
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(level[0]) and 0 <= ny < len(level):
                    if level[ny][nx] == '#':  # Взрываем только стены
                        level[ny][nx] = '.'
                        render_particles_on_collision(nx * TILE_SIZE, ny * TILE_SIZE)  # Эффект разрушения

    def swap_head(self, level):
        x, y = self.snake_coords[0][0], self.snake_coords[0][1]
        max_x_y = len(level) - 1
        next_x, next_y = self.snake_coords[1][0], self.snake_coords[1][1]
        direction = self.direction
        if not (x == 0 and next_x == max_x_y) and (x < next_x or (x == max_x_y and next_x == 0)):
            direction = 'left'
        elif x > next_x or (x == 0 and next_x == max_x_y):
            direction = 'right'
        elif not (y == 0 and next_y == max_x_y) and (y < next_y or (y == max_x_y and next_y == 0)):
            direction = 'up'
        elif y > next_y or (y == 0 and next_y == max_x_y):
            direction = 'down'
        self.snake_coords.reverse()
        self.direction = direction
