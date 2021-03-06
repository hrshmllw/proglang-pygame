from re import I
from tkinter import W
import pygame as pg
from pygame.constants import DROPTEXT
from settings import *
from enum import Enum
from collections import deque

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
        self.moves = 0
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

        self.next_move = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.invalid_moves = []

    def move(self, dx=0, dy=0, direction=Direction.DOWN):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            self.direction = direction
            self.image = self.image_directions[direction]
            self.moves += 1
            self.invalid_moves = []
        
            for mob in self.game.mobs:
                for player_move in self.next_move:
                    next_player_position = (self.x + player_move[0], self.y + player_move[1])

                    if mob.x == next_player_position[0]+1 and mob.y == next_player_position[1]+1:
                        self.invalid_moves.append(next_player_position)
                        
            print(self.invalid_moves)

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
        invalid_image = pg.image.load("assets/invalid.png")
        invalid_image = pg.transform.scale(invalid_image, (TILESIZE, TILESIZE))

        for move in self.invalid_moves:
            self.game.screen.blit(invalid_image, (move[0]*TILESIZE, move[1]*TILESIZE))

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

        self.directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def find_neighbors(self, node):
        neighbors = [(node[0] + direction[0], node[1] + direction[1]) for direction in self.directions]
        if (node[0] + node[1]) % 2:
            neighbors.reverse()
        neighbors = [node for node in neighbors if not self.collide_with_walls(node)]
        return neighbors

    def breadth_first_search(self, start, end, path=[], exclude=[]):
        if start == end:
            return path

        neighbors_d = {}
        
        neighbors = self.find_neighbors(start)
        for to_remove in exclude:
            if to_remove in neighbors:
                neighbors.remove(to_remove)

        for neighbor in neighbors:
            # if len(path) > 0 and neighbors == path[-1]:
            #     continue
            if neighbor in path:
                continue
            d = abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])
            neighbors_d[neighbor] = d
        if not neighbors_d:
            return {}
        min_d = min(neighbors_d, key=neighbors_d.get)
        path.append(min_d)
        return self.breadth_first_search(min_d, end, path)

    def move_towards_player(self, player):
        current = (self.x, self.y)

        path = self.breadth_first_search(current, player, path=[])
        if len(path) > 0:
            next = path[0]
            if not (next[0] == player[0] and next[1] == player[1]):
                self.x = path[0][0]
                self.y = path[0][1]

    def collide_with_walls(self, node):
        for wall in self.game.walls:
            if wall.x == node[0] and wall.y == node[1]:
                return True
        return False

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