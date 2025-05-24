import random

import pygame.sprite

from settings import *


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


class AppleParticle(pygame.sprite.Sprite):
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


class StarParticle(pygame.sprite.Sprite):
    stars = [load_image(star_image)]
    for scale in (5, 7.5, 10, 15):
        stars.append(pygame.transform.scale(stars[0], (scale, scale)))
    stars.pop(0)

    def __init__(self, x, y, type='wall_collision'):
        super().__init__(particle_group)
        self.image = random.choice(self.stars)
        self.rect = self.image.get_rect(center=(x + 12, y + 12))
        self.velocity = [random.choice(range(-5, 6)), random.choice(range(-5, 6))]
        self.rect.x, self.rect.y = x, y
        if type == 'wall_collision':
            self.lifetime = random.randint(4, 5)
        elif type == 'boom':
            self.lifetime = random.randint(7, 8)
        self.gravity = GRAVITY

    def update(self):
        self.lifetime -= 1
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.lifetime <= 0:
            self.kill()
        elif (pygame.sprite.spritecollideany(self, vertical_borders_group) or
              pygame.sprite.spritecollideany(self, horizontal_borders_group)):
            self.kill()
        self.vel_x = random.uniform(-1, 2)
        self.vel_y = random.uniform(-1, 2)


class ShieldParticle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Инициализируем родительский класс Sprite
        self.color = (0, random.randint(100, 200), 255)
        self.alpha = random.randint(80, 180)
        self.size = random.randint(3, 6)

        # Создаем поверхность для частицы
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            (*self.color, self.alpha),  # RGBA
            (self.size, self.size),
            self.size
        )

        self.rect = self.image.get_rect(center=(x * TILE_SIZE + x // 2 + random.uniform(-5, 5),
                                                y * TILE_SIZE + y // 2 + random.uniform(-5, 5)))
        self.lifetime = random.randint(20, 40)

    def update(self):
        self.lifetime -= 1
        self.rect.x += random.uniform(-0.5, 0.5)
        self.rect.y += random.uniform(-0.5, 0.5)

        # Плавное исчезновение
        if self.lifetime < 20:
            self.alpha = max(0, self.alpha - 10)
            self.image.set_alpha(self.alpha)

        if self.lifetime <= 0:
            self.kill()


class MiniTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(mini_tiles_group, all_sprites)
        tile_image = current_images[tile_type]
        scaled_image = pygame.transform.scale(tile_image, (
            int(tile_image.get_width() / 50 * MINI_TILE_SIZE), int(tile_image.get_height() / 50 * MINI_TILE_SIZE)))
        self.image = scaled_image
        self.rect = self.image.get_rect().move(
            150 + MINI_TILE_SIZE * pos_x, 125 + MINI_TILE_SIZE * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y, scaled=True):
        super().__init__(tiles_group, all_sprites)
        tile_image = current_images[tile_type]
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
        snake_image = current_snake_images[type]
        if scaled:
            scaled_image = pygame.transform.scale(snake_image, (
                int(snake_image.get_width() / 50 * TILE_SIZE), int(snake_image.get_height() / 50 * TILE_SIZE)))
            self.image = scaled_image
            self.rect = self.image.get_rect().move(
                TILE_SIZE * x, TILE_SIZE * y)
        else:
            self.image = snake_image
            self.rect = self.image.get_rect().move(x * 50, y * 50)


class AnimatedSnakeShowcase(pygame.sprite.Sprite):  # критерий анимация
    def __init__(self, x, y):
        super().__init__(animated_group)
        self.frames = list(current_snake_images.values())
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x * 50, y * 50)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class FakeApple(pygame.sprite.Sprite):
    def __init__(self, x, y, scaled=True):
        super().__init__(fake_apples_group, all_sprites)
        self.scaled = scaled
        image = list(current_apple_images.values())[-1]
        if self.scaled:
            scaled_image = pygame.transform.scale(image, (
                int(image.get_width() / 50 * TILE_SIZE), int(image.get_height() / 50 * TILE_SIZE)))
            self.image = scaled_image
            self.rect = self.image.get_rect().move(
                TILE_SIZE * x, TILE_SIZE * y)
        else:
            self.image = image
            self.rect = self.image.get_rect().move(x * 50, y * 50)


class AnimatedApple(pygame.sprite.Sprite):
    def __init__(self, x, y, scaled=True, type='normal'):
        super().__init__(animated_group)
        self.scaled = scaled
        if type == 'normal':
            self.frames = list(current_apple_images.values())
        elif type == 'bomb':
            self.frames = list(bomb_apple_images.values())
        elif type == 'switch_head':
            self.frames = list(switch_head_apple_images.values())
        elif type == 'invincible':
            self.frames = list(invincible_apple_images.values())
        elif type == 'rock':
            self.frames = list(rock_apple_images.values())
        self.cur_frame = 0
        image = self.frames[self.cur_frame]
        if self.scaled:
            scaled_image = pygame.transform.scale(image, (
                int(image.get_width() / 50 * TILE_SIZE), int(image.get_height() / 50 * TILE_SIZE)))
            self.image = scaled_image
            self.rect = self.image.get_rect().move(
                TILE_SIZE * x, TILE_SIZE * y)
        else:
            self.image = image
            self.rect = self.image.get_rect().move(x * 50, y * 50)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        image = self.frames[self.cur_frame]
        if self.scaled:
            scaled_image = pygame.transform.scale(image, (
                int(image.get_width() / 50 * TILE_SIZE), int(image.get_height() / 50 * TILE_SIZE)))
            self.image = scaled_image
        else:
            self.image = image


class GameOver(pygame.sprite.Sprite):
    def __init__(self, type='game_over'):
        super().__init__(game_over_group)
        if type == 'win':
            self.image = load_image('background_images\\game_over_screens\\win_screen.jpg')
        else:
            self.image = load_image("background_images\\game_over_screens\\lose_screen.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = - WIDTH
        self.rect.y = 0
        self.angle = 0
        self.dx = 400

    def update(self):
        if self.rect.x < 0:
            self.rect.x += 50
