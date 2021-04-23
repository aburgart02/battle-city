import pygame
from sprites import TANKS_IMAGES
(BASIC, FAST, RAPID, ARMORED) = range(4)
(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)
from settings import DISPLAY
from bullet import Bullet
class Tank:
    def __init__(self, role, kind=0, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        self.x = position[0]
        self.y = position[1]
        self.role = role
        self.kind = kind
        self.speed = speed
        self.get_type()
        self.level = level
        self.image = TANKS_IMAGES[role][kind][direction]
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.current_bullets = self.max_bullets
        self.moving_state = False

    def get_type(self):
        if self.kind == 3:
            self.health = 4
            self.bullet_type = 1
        else:
            self.health = 1
            self.bullet_type = 0
        if self.kind == 1:
            self.speed = self.speed * 2
        if self.kind == 2 or self.kind == 3:
            self.max_bullets = 2
        else:
            self.max_bullets = 1

    def fire(self):
        if self.max_bullets >= self.current_bullets > 0:
            if self.direction == DIRECTION_UP:
                self.level.bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x + 5, self.rect.y), self, self.level))
            if self.direction == DIRECTION_DOWN:
                self.level.bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x + 5, self.rect.y + 12), self, self.level))
            if self.direction == DIRECTION_RIGHT:
                self.level.bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x + 12, self.rect.y + 6), self, self.level))
            if self.direction == DIRECTION_LEFT:
                self.level.bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x, self.rect.y + 6), self, self.level))
            self.current_bullets -= 1

    def make_step(self):
        if self.direction == DIRECTION_LEFT:
            self.x -= self.speed
        if self.direction == DIRECTION_RIGHT:
            self.x += self.speed
        if self.direction == DIRECTION_UP:
            self.y -= self.speed
        if self.direction == DIRECTION_DOWN:
            self.y += self.speed
        self.rect.topleft = round(self.x), round(self.y)

    def align_collision(self, entity):
        if self.rect.bottom >= entity.rect.top and self.rect.bottom <= entity.rect.bottom and self.direction == DIRECTION_DOWN:
            self.rect.bottom = entity.rect.top
        if self.rect.top <= entity.rect.bottom and self.rect.top >= entity.rect.top and self.direction == DIRECTION_UP:
            self.rect.top = entity.rect.bottom
        if self.rect.left <= entity.rect.right and self.rect.left >= entity.rect.left and self.direction == DIRECTION_LEFT:
            self.rect.left = entity.rect.right
        if self.rect.right >= entity.rect.left and self.rect.right <= entity.rect.right and self.direction == DIRECTION_RIGHT:
            self.rect.right = entity.rect.left
        self.x, self.y = self.rect.topleft

    def turn_back(self):
        self.direction = 2 * (self.direction // 2) + (self.direction + 1) % 2

    def on_map(self):
        return 0 <= self.x <= DISPLAY.get_width() - self.image.get_width() and 0 <= self.y <= DISPLAY.get_height() - self.image.get_height()

    def return_on_map(self):
        if self.x < 0: self.x = 0
        if self.x > DISPLAY.get_width() - self.image.get_width(): self.x = DISPLAY.get_width() - self.image.get_width()
        if self.y < 0: self.y = 0
        if self.y > DISPLAY.get_height() - self.image.get_height(): self.y = DISPLAY.get_height() - self.image.get_height()
