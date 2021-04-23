from sprites import BULLET_IMAGES
import pygame
from settings import DISPLAY, get_hit_list
from tile import BRICK, GRASS, BETON, ICE, WATER
(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)
class Bullet:
    def __init__(self, kind, direction=DIRECTION_UP, position=None, owner=None, level=None):
        self.x = position[0]
        self.y = position[1]
        self.speed = 2
        self.direction = direction
        self.kind = kind
        self.rect = pygame.Rect(self.x, self.y, 4, 4)
        self.image = BULLET_IMAGES[self.direction]
        self.owner = owner
        self.level = level

    def fly(self):
        if 0 < self.rect.x < DISPLAY.get_width() - self.image.get_width() and 0 < self.rect.y < DISPLAY.get_height() - self.image.get_height():
            if self.direction == DIRECTION_LEFT:
                self.x -= self.speed
            if self.direction == DIRECTION_RIGHT:
                self.x += self.speed
            if self.direction == DIRECTION_UP:
                self.y -= self.speed
            if self.direction == DIRECTION_DOWN:
                self.y += self.speed
            self.rect.topleft = round(self.x), round(self.y)
            for tile in get_hit_list(self.rect, self.level.map):
                if tile.type == BRICK:
                    self.level.kill_tile(tile)
                if tile.type == BETON and self.kind == 1:
                    self.level.kill_tile(tile)
                if tile.type != GRASS:
                    self.die()
            if self.owner.role == 0:
                for enemy in get_hit_list(self.rect, self.level.enemies):
                    enemy.health -= 1
                    if enemy.health == 0:
                        enemy.die()
                    self.die()
            else:
                for p in get_hit_list(self.rect, [self.level.player]):
                    p.health -= 1
                    if p.health == 0:
                        p.die()
                    self.die()
            for c in get_hit_list(self.rect, [self.level.castle]):
                self.die()
                c.die()
            for bullet in get_hit_list(self.rect, self.level.bullets[:]):
                if self != bullet:
                    self.die()
                    bullet.die()
        else:
            self.die()

    def die(self):
        if self in self.level.bullets:
            self.level.bullets.remove(self)
            self.owner.current_bullets += 1