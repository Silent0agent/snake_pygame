from sprites import *


def render_scheme(level):
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == '.':
                MiniTile('empty', x, y)
            elif level[y][x] == '#':
                MiniTile('wall', x, y)


def render_level(level, snake):
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
                # Apple(x, y)
                if len(animated_group) == 0:
                    AnimatedApple(x, y)
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


def render_particles_on_eat(x, y):
    color = (240, 0, 0)
    for _ in range(10):  # 10 частиц за раз
        particle = AppleParticle(x, y, color)
        particle_group.add(particle)


def render_particles_on_collision(x, y):
    color = (134, 136, 138)
    for _ in range(5):
        particle = WallParticle(x, y)
        particle_group.add(particle)
