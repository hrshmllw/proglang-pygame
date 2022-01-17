from cmath import sqrt
import pygame as pg
from pygame.constants import DROPTEXT
from settings import *
from enum import Enum
from math import sqrt

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.direction = Direction.DOWN
        self.game = game
        self.image_directions = {
            Direction.UP: pg.image.load("assets/up.png"),
            Direction.DOWN: pg.image.load("assets/down.png"),
            Direction.RIGHT: pg.image.load("assets/side.png"),
            Direction.LEFT: pg.transform.flip(pg.image.load("assets/side.png"), flip_x=True, flip_y=False)
        }
        for key, value in self.image_directions.items():
            self.image_directions[key] = pg.transform.scale(self.image_directions[key], (TILESIZE, TILESIZE))
        self.image = self.image_directions[Direction.DOWN]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0, direction=Direction.DOWN):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            self.direction = direction
            self.image = self.image_directions[direction]

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def move_towards_player(self, player_x, player_y):
        mob_directions = {
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
            Direction.UP: (0, 1),
            Direction.DOWN: (0, -1)
        }
        shortest_distance = (HEIGHT*WIDTH)/TILESIZE
        best_direction = None
        for key, value in mob_directions.items():
            new_direction = (self.x + mob_directions[key][0], self.y + mob_directions[key][1])
            d = sqrt((player_x-new_direction[0])**2+(player_y-new_direction[1])**2)
            if d < shortest_distance:
                shortest_distance = d
                best_direction = key
            print(d)
            print(shortest_distance)
            print(best_direction)
        if best_direction != None:
            self.x += mob_directions[best_direction][0]
            self.y += mob_directions[best_direction][1]
            print("{},{}".format(self.x, self.y))

        def update(self):
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE