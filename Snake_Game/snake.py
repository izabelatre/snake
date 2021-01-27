from dataclasses import dataclass, field
from typing import List
from random import randrange
import pygame

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

CELL_SIZE = 20
HEAD_INDEX = 0



@dataclass
class Snake:
    length: int
    color: tuple
    snake_placement = [190, 210, 230, 250, 270]

    COLORS = [(255,0, 0), (0, 0, 255), (100, 100, 100), (150, 150, 150), (200, 200, 200)]

    def update_colors(self):
        num = randrange(len(self.COLORS))
        run = True
        while run:
            if not self.is_color_same(self.COLORS[num]):
                self.color = self.COLORS[num]
                run = False

    def is_color_same(self, new_color: tuple) -> bool:
        return new_color == self.color

@dataclass
class World:
    snake: Snake
    num_of_obstacles: int
    obstacles_placements = list()

    list_of_obstacles: list = field(init=False)
    list_of_fruits: list = field(init=False)
    world_data : list = field(init=False)
    world_map: List[int] = field(default_factory=list)
    CELL_SIZE = 20



    def __post_init__(self):
        for i in range(0, self.CELL_SIZE * self.CELL_SIZE):
            self.world_map.append(0)
        self.place_obstacles()
        self.fruit_eaten = False
        self.is_dead = False
        self.num_of_eaten_fruits = 0
        self.head = 190

    # 150, 170
    # 190, 210, 230, 250, 270, 290

    def place_obstacles(self):
        snake_start_placements_ = list([150,170, 190, 210, 230, 250, 270, 290])
        while len(self.obstacles_placements) < self.num_of_obstacles:
            num = randrange(self.CELL_SIZE * self.CELL_SIZE)
            if num not in self.obstacles_placements:
                if num not in snake_start_placements_:
                    self.obstacles_placements.append(num)
                    self.world_map.pop(num)
                    self.world_map.insert(num, 1)

    def place_fruit(self):
        run = True
        num_ = 0
        while run:
            num = randrange(self.CELL_SIZE * self.CELL_SIZE)
            if self.world_map[num] != 1 and self.world_map[num] != 3:
                if num<20:
                    if self.world_map[num+ 380] == 1:
                        num_+=1
                else:
                    if self.world_map[num -20] ==1:
                        num_+=1

                if num > 380:
                    if self.world_map[num-380] == 1:
                        num_+=1
                else:
                    if self.world_map[num+20] == 1:
                        num_+=1
                if num == 0:
                    if self.world_map[399] == 1:
                        num_ += 1
                else:
                    if self.world_map[num-1] == 1:
                        num_+=1

                if num == 399:
                    if self.world_map[0] == 1:
                        num_+=1
                else:
                    if self.world_map[num+1]==1:
                        num_+=1

                if num_<3:
                    run = False
                    self.world_map.pop(num)
                    self.world_map.insert(num, 2)

    def value_at_coordinates(self, row: int, column: int) -> int:
        if row < self.CELL_SIZE and column < self.CELL_SIZE:
            index = row*20 + column
            return self.world_map[index]

    def coordinates(self, value) ->list:
        column = value%20
        row = (value-column)/20
        return [row, column]



    def snake_placement(self):
         for place in self.snake.snake_placement:
            self.world_map.insert(place, 3)

    def move_snake(self, direction: str):

        if direction == UP:
            newHead = self.snake.snake_placement[0] - self.CELL_SIZE
            #print(self.snake.snake_placement[0])
            if (newHead < 0):
                newHead = self.snake.snake_placement[0] + 380

        elif direction == DOWN:
            newHead = self.snake.snake_placement[0] + self.CELL_SIZE
            #print(self.snake.snake_placement[0])
            if(newHead > 400):
                newHead = self.snake.snake_placement[0]-380

        elif direction == LEFT:
            newHead = self.snake.snake_placement[0]-1
            #(self.snake.snake_placement[0])
            if(newHead % 20 == 19):
                newHead = self.snake.snake_placement[0] + 19

        elif direction == RIGHT:
            newHead = self.snake.snake_placement[0]+1
            #print(self.snake.snake_placement[0])
            if (newHead % 20 == 0):
                newHead = self.snake.snake_placement[0] - 19

        self.snake.snake_placement.insert(HEAD_INDEX, newHead)
        self.head = newHead
        self.has_suicided()
        self.has_hit_obstacle(self.world_map[newHead]);
        if (self.has_eaten_fruit(self.world_map[newHead]) == False):
            tail_value = self.snake.snake_placement[len(self.snake.snake_placement) - 1]
            self.world_map.pop(tail_value)
            self.world_map.insert(tail_value, 0)
            self.snake.snake_placement.pop(len(self.snake.snake_placement) - 1)
        self.world_map.pop(newHead)
        self.world_map.insert(newHead, 3)
        check = False
        for var in self.world_map:
            if var == 2:
                check = True
        if check == False:
            self.place_fruit()


    def has_hit_obstacle(self, x):
        if (x == 1):
            self.is_dead = True



    def has_eaten_fruit(self, x) -> bool:
        if (x == 2):
            self.num_of_eaten_fruits+=1
            self.place_fruit()
            if(self.num_of_eaten_fruits == 15):
                self.fruit_eaten = True
            return True
        else:
            return False

    def has_suicided(self):
        isHead = True
        for var in self.snake.snake_placement:
            if var == self.snake.snake_placement[HEAD_INDEX]:
                if isHead:
                    pass
                else:
                    self.is_dead = True
            isHead = False

    def print_world(self):
        for i in range(0, self.CELL_SIZE):
            start: int = 0 + i*20
            end: int = 20 + i*20
            self.world_map[start: end]





