import random
from settings import TILE_SIZE, animated_group
from utils import load_sound
from render import render_particles_on_eat, render_particles_on_collision


class Snake:
    def __init__(self, snake_coords):
        self.snake_coords = snake_coords
        self.direction = 'right'
        self.score = 0
        self.forbidden_moves = {'up': 'down',
                                'down': 'up',
                                'left': 'right',
                                'right': 'left'}

    def create_apple(self, level):
        for spr in animated_group:
            spr.kill()
        free_cells = []
        rows = len(level)
        cols = len(level[0])

        for row in range(rows):
            for col in range(cols):
                if level[row][col] == '.' and (row, col) not in self.snake_coords:
                    free_cells.append((row, col))

        # Случайно выбираем одну из свободных клеток
        if free_cells:
            apple_row, apple_col = random.choice(free_cells)
            level[apple_row][apple_col] = '@'
            pos = (apple_row, apple_col)
            return pos
        return True  # победа если нет места для яблока

    def change_direction(self, direction):
        if self.forbidden_moves[direction] != self.direction:
            self.direction = direction

    def move(self, level):
        last_x, last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        max_x_y = len(level) - 1
        if self.direction == 'right':
            if last_x + 1 > max_x_y:
                if level[last_y][0] == '#' or (0, last_y) in self.snake_coords:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE - 5,
                                                  self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                    return 'game_over'
                else:
                    self.snake_coords.append((0, last_y))
            elif level[last_y][last_x + 1] == '#' or (
                    last_x + 1, last_y) in self.snake_coords:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE - 5,
                                              self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                return 'game_over'
            else:
                self.snake_coords.append((last_x + 1, last_y))
        elif self.direction == 'left':
            if last_x - 1 < 0:
                if level[last_y][max_x_y] == '#' or (max_x_y, last_y) in self.snake_coords:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE,
                                                  self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                    return 'game_over'
                else:
                    self.snake_coords.append((max_x_y, last_y))
            elif level[last_y][last_x - 1] == '#' or (last_x - 1, last_y) in self.snake_coords:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE,
                                              self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE // 2)
                return 'game_over'
            else:
                self.snake_coords.append((last_x - 1, last_y))
        elif self.direction == 'up':
            if last_y - 1 < 0:
                if level[max_x_y][last_x] == '#' or (last_x, max_x_y) in self.snake_coords:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE // 2,
                                                  self.snake_coords[-1][1] * TILE_SIZE)
                    return 'game_over'
                else:
                    self.snake_coords.append((last_x, max_x_y))
            elif level[last_y - 1][last_x] == '#' or (last_x, last_y - 1) in self.snake_coords:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE // 2,
                                              self.snake_coords[-1][1] * TILE_SIZE)
                return 'game_over'
            else:
                self.snake_coords.append((last_x, last_y - 1))
        elif self.direction == 'down':
            if last_y + 1 > len(level) - 1:
                if level[0][last_x] == '#' or (last_x, 0) in self.snake_coords:
                    render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE,
                                                  self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE - 5)
                    return 'game_over'
                else:
                    self.snake_coords.append((last_x, 0))
            elif level[last_y + 1][last_x] == '#' or (last_x, last_y + 1) in self.snake_coords:
                render_particles_on_collision(self.snake_coords[-1][0] * TILE_SIZE + TILE_SIZE // 2,
                                              self.snake_coords[-1][1] * TILE_SIZE + TILE_SIZE - 5)
                return 'game_over'
            else:
                self.snake_coords.append((last_x, last_y + 1))
        new_last_x, new_last_y = self.snake_coords[-1][0], self.snake_coords[-1][1]
        if level[new_last_y][new_last_x] != '@':
            self.snake_coords.pop(0)
        else:
            self.score += 1
            level[new_last_y][new_last_x] = '.'
            win = self.create_apple(level)
            render_particles_on_eat(new_last_x * TILE_SIZE, new_last_y * TILE_SIZE)
            load_sound('\\sound_effects\\eat_food.mp3').play()
            if win is True:
                return 'win'
        return 'continue'
