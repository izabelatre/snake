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
    START_IMG = pygame.image.load('start.png')
    HEAD_UP_IMG = pygame.image.load('head_up.JPG')
    world = snake.World(snake.Snake(5,(200,200,200)), 25)
    window: pygame.display = field(init=False)
    WINDOW_SIZE = 600
    TILE_SIZE = 30
    NEEDED_TO_MOVE = 30
    clock = pygame.time.Clock()
    move_counter = 0
    direction = 'up'
    #left right up down

    def __post_init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        self.GRASS_IMG = pygame.transform.scale(self.GRASS_IMG, (self.TILE_SIZE, self.TILE_SIZE))
        self.OBSTACLE_IMG = pygame.transform.scale(self.OBSTACLE_IMG, (self.TILE_SIZE, self.TILE_SIZE))
        self.APPLE_IMG = pygame.transform.scale(self.APPLE_IMG, (self.TILE_SIZE, self.TILE_SIZE))
        self.HEAD_UP_IMG = pygame.transform.scale(self.HEAD_UP_IMG, (self.TILE_SIZE, self.TILE_SIZE))
        self.START_IMG = pygame.transform.scale(self.START_IMG, (300, 200))
        self.HEAD_LEFT_IMG = pygame.transform.rotate(self.HEAD_UP_IMG, 90)
        self.HEAD_DOWN_IMG = pygame.transform.rotate(self.HEAD_UP_IMG, 180)
        self.HEAD_RIGHT_IMG = pygame.transform.rotate(self.HEAD_UP_IMG, 270)


    def menu(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.GRASS_IMG, (150, 200))
        run = True
        while run:
            pygame.display.update()



    def game(self):
        self.window.fill((0, 0, 0))
        self.world.place_obstacles()
        self.world.place_fruit()
        self.world.snake_placement()

        run = True
        while run:
            for i in range(0, self.world.CELL_SIZE):
                for j in range(0, self.world.CELL_SIZE):
                    self.place_tile(i, j)
            self.move()
            if(self.world.is_dead == True):
                run = False
            if(self.world.fruit_eaten):
                run = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if(self.direction != 'up'):
                            self.direction = 'down'
                            print("DOWN")

                    elif event.key == K_UP:
                        if(self.direction != 'down'):
                            self.direction ='up'
                            print("UP")

                    elif event.key == K_RIGHT:
                        if(self.direction != 'left'):
                            self.direction ='right'
                            print("RIGHT")

                    elif event.key == K_LEFT:
                        if(self.direction != 'right'):
                            self.direction ='left'
                            print("LEFT")

            pygame.display.update()

            self.clock.tick(200)
            self.move_counter += 1

    def place_tile(self, column: int, row: int):
        if self.world.value_at_coordinates(row=row, column=column) == 0:
            self.window.blit(self.GRASS_IMG, (column * self.TILE_SIZE, row * self.TILE_SIZE))
        elif self.world.value_at_coordinates(row=row, column=column) == 1:
            self.window.blit(self.OBSTACLE_IMG, (column * self.TILE_SIZE, row * self.TILE_SIZE))
        elif self.world.value_at_coordinates(row=row, column=column) == 2:
            self.window.blit(self.GRASS_IMG, (column * self.TILE_SIZE, row * self.TILE_SIZE))
            self.window.blit(self.APPLE_IMG, (column * self.TILE_SIZE, row * self.TILE_SIZE))
        elif self.world.value_at_coordinates(row=row, column=column) == 3:
            snake_part = pygame.Rect(column * self.TILE_SIZE, row*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
            snake_part_inner = pygame.Rect(column * self.TILE_SIZE + 4, row*self.TILE_SIZE +4, self.TILE_SIZE-8, self.TILE_SIZE-8)
            pygame.draw.rect(self.window, (150,255,100), snake_part)
            pygame.draw.rect(self.window, (0,255,0), snake_part_inner)
            if self.direction == 'up':
                self.window.blit(self.HEAD_UP_IMG, (self.world.coordinates(self.world.head)[1] * self.TILE_SIZE , self.world.coordinates(self.world.head)[0]* self.TILE_SIZE))
            if self.direction == 'down':
                self.window.blit(self.HEAD_DOWN_IMG, (self.world.coordinates(self.world.head)[1] * self.TILE_SIZE , self.world.coordinates(self.world.head)[0]* self.TILE_SIZE))
            if self.direction == 'right':
                self.window.blit(self.HEAD_RIGHT_IMG, (self.world.coordinates(self.world.head)[1] * self.TILE_SIZE , self.world.coordinates(self.world.head)[0]* self.TILE_SIZE))
            if self.direction == 'left':
                self.window.blit(self.HEAD_LEFT_IMG, (self.world.coordinates(self.world.head)[1] * self.TILE_SIZE , self.world.coordinates(self.world.head)[0]* self.TILE_SIZE))

    def move(self):
        if not self.move_counter < self.NEEDED_TO_MOVE:
            #NUM_OF_FRUITS_TO_WIN, fruit_counter
            #direction right, bottom str...
            self.world.move_snake(self.direction)

            self.move_counter = 0
            self.world.print_world()


g = Game()
g.game()
print(g.world.coordinates(150))
print(g.world.coordinates(170))
print(g.world.coordinates(190))