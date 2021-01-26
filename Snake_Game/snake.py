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
        fruit_eaten = False

    # 150, 170
    # 190, 210, 230, 250, 270, 290

    def place_obstacles(self):
        snake_start_placements_ = list([170, 190, 210, 230, 250, 270, 290])
        while len(self.obstacles_placements) < self.num_of_obstacles:
            num = randrange(self.CELL_SIZE * self.CELL_SIZE)
            if num not in self.obstacles_placements:
                if num not in snake_start_placements_:
                    self.obstacles_placements.append(num)
                    self.world_map.pop(num)
                    self.world_map.insert(num, 1)

    def place_fruit(self):
        if 2 in self.world_map:
            index = self.world_map.index(2)
            self.world_map.pop(index)
            self.world_map.insert(index, 0)
        run = True
        while run:
            num = randrange(self.CELL_SIZE * self.CELL_SIZE)
            if self.world_map[num] != 1 and self.world_map[num] != 3:
                run = False
                self.world_map.pop(num)
                self.world_map.insert(num, 2)

    def value_at_coordinates(self, row: int, column: int) -> int:
        if row < self.CELL_SIZE and column < self.CELL_SIZE:
            index = row*20 + column
            return self.world_map[index]


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
        tail_value = self.snake.snake_placement[len(self.snake.snake_placement)-1]
        self.world_map.pop(tail_value)
        self.world_map.insert(tail_value, 0)
        self.snake.snake_placement.pop(len(self.snake.snake_placement)-1)
        self.world_map.pop(newHead)
        self.world_map.insert(newHead, 3)


    def has_hit_obstacle(self, direction) -> bool:
            for var in self.place_obstacles():
                if(self.snake.snake_placement[HEAD_INDEX] == var):
                    return True

    def has_eaten_fruit(self):
        if(self.world_map[self.snake.snake_placement[HEAD_INDEX]] == 2):
            self.fruit_eaten = True


    def has_suicided(self) -> bool:
        isHead = True
        for var in self.snake.snake_placement:
            if var == self.snake.snake_placement[HEAD_INDEX]:
                if(isHead):
                    pass
                else:
                    return True
            isHead = False
        pass

    def print_world(self):
        for i in range(0, self.CELL_SIZE):
            start: int = 0 + i*20
            end: int = 20 + i*20
            print(self.world_map[start: end])
        print("////////////////")




