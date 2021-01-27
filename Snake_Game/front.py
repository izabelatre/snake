import datetime
import sys
from dataclasses import dataclass, field

import pygame
from pygame.locals import *

from Snake_Game import snake

pygame.display.set_caption('Snake Game')



@dataclass
class Game:
    pygame.font.init()
    m_font = pygame.font.Font('freesansbold.ttf', 18)
    BACKGROUND = pygame.image.load('apple.png')
    APPLE_IMG = pygame.image.load('apple.png')
    GRASS_IMG = pygame.image.load('grass.JPG')
    OBSTACLE_IMG = pygame.image.load('end.JPG')
    START_IMG = pygame.image.load('start.png')
    HEAD_UP_IMG = pygame.image.load('head_up.JPG')
    GAME_OVER_IMG = pygame.image.load('gameOver.png')
    VICTORY_IMG = pygame.image.load('VICTORY.png')
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
        self.GAME_OVER_IMG = pygame.transform.scale(self.GAME_OVER_IMG, (self.WINDOW_SIZE, self.WINDOW_SIZE))
        self.VICTORY_IMG = pygame.transform.scale(self.VICTORY_IMG, (self.WINDOW_SIZE-200, self.WINDOW_SIZE-400))
        self.start_time = field(default=datetime.datetime.now())


    def checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            pygame.quit()
            sys.exit()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        return keyUpEvents[0].key


    def menu(self):

        run = True
        while run:
            self.window.fill((0,0,0))
            self.window.blit(self.START_IMG,(150,100))
            pressKeySurf = self.m_font.render('Press a key to play.', True, (0,255,0))
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.topleft = (400, 570)
            self.window.blit(pressKeySurf, pressKeyRect)
            self.world.apples_to_win = 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        pygame.event.get()  # clear event queue
                        run = False
                        self.game()


            pygame.display.update()
            self.clock.tick(20)

    def game(self):
        self.window.fill((0, 0, 0))
        self.world.place_obstacles()
        self.world.place_fruit()
        self.world.snake_placement()
        self.start_time = datetime.datetime.now()
        run = True
        while run:
            for i in range(0, self.world.CELL_SIZE):
                for j in range(0, self.world.CELL_SIZE):
                    self.place_tile(i, j)
            self.move()
            if(self.world.is_dead == True):
                run = False
                self.end_game()
            if(self.world.fruit_eaten):
                run = False
                self.happy_end_game()

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

    def happy_end_game(self):
        running = True
        end_time = datetime.datetime.now()
        diff = end_time - self.start_time
        print(diff)
        while running:
            self.window.fill((10, 10, 10))
            self.window.blit(self.VICTORY_IMG, (100, 200))

            pressKeySurf = self.m_font.render('Your time: {}'.format(diff), True, (255, 155, 0))
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.topleft = (180, 420)
            self.window.blit(pressKeySurf, pressKeyRect)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        pygame.event.get()  # clear event queue
                        running = False

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(20)

    def end_game(self):
        running = True
        end_time = datetime.datetime.now()
        diff = end_time - self.start_time
        print(diff)
        while running:
            self.window.fill((0,0,0))
            self.window.blit(self.GAME_OVER_IMG,(0,0))

            pressKeySurf = self.m_font.render('Your time: {}'.format(diff), True, (255, 155, 0))
            pressKeyRect = pressKeySurf.get_rect()
            pressKeyRect.topleft = (180, 420)
            self.window.blit(pressKeySurf, pressKeyRect)


            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        pygame.event.get()  # clear event queue
                        running = False

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(20)

        self.game()

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
g.menu()