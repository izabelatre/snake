import sys
from dataclasses import dataclass, field

import pygame
from pygame.locals import *

from Snake_Game import snake

@dataclass
class Game:
    BACKGROUND = pygame.image.load('apple.png')
    APPLE_IMG = pygame.image.load('apple.png')
    GRASS_IMG = pygame.image.load('grass.JPG')
    OBSTACLE_IMG = pygame.image.load('end.JPG')
    world = snake.World(snake.Snake(5,(200,200,200)),25)
    window: pygame.display = field(init=False)
    WINDOW_SIZE = 600
    TILE_SIZE = 30
    clock = pygame.time.Clock()

    def __post_init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        self.GRASS_IMG = pygame.transform.scale(self.GRASS_IMG, (self.TILE_SIZE, self.TILE_SIZE))
        self.OBSTACLE_IMG = pygame.transform.scale(self.OBSTACLE_IMG, (self.TILE_SIZE, self.TILE_SIZE))
        self.APPLE_IMG = pygame.transform.scale(self.APPLE_IMG, (self.TILE_SIZE, self.TILE_SIZE))

    def game(self):
        self.window.fill((0, 0, 0))
        self.world.place_obstacles()
        self.world.place_fruit()

        while True:
            for i in range(0, self.world.CELL_SIZE):
                for j in range(0, self.world.CELL_SIZE):
                    self.place_tile(i, j)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(60)

    def place_tile(self, column: int, row: int):
        if self.world.value_at_coordinates(row=row, column=column) == 0:
            self.window.blit(self.GRASS_IMG, (column * self.TILE_SIZE, row * self.TILE_SIZE))
        elif self.world.value_at_coordinates(row=row, column=column) == 1:
            self.window.blit(self.OBSTACLE_IMG, (column * self.TILE_SIZE, row * self.TILE_SIZE))
        elif self.world.value_at_coordinates(row=row, column=column) == 2:
            self.window.blit(self.APPLE_IMG, (column * self.TILE_SIZE, row * self.TILE_SIZE))
        elif self.world.value_at_coordinates(row=row, column=column) == 3:
            snake_part = pygame,Rect(column* self.TILE_SIZE, row*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            pygame.draw.rect(self.window, self.world.snake.color, snake_part)

g = Game()
g.game()