from dataclasses import dataclass, field
from typing import List
from random import randrange
import pygame


@dataclass
class Snake:
    length: int
    color: tuple
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
    num_of_obstacles: int
    world_map: List[int] = field(default_factory=list)
    SIZE = 20
    background = 'XD'


    def __post_init__(self):
        for i in range(0, self.SIZE * self.SIZE):
            self.world_map.append(0)
        self.place_obstacles()

    def place_obstacles(self):
        obstacles_placements = list()
        while len(obstacles_placements) < self.num_of_obstacles:
            num = randrange(self.SIZE * self.SIZE)
            if num not in obstacles_placements:
                obstacles_placements.append(num)
                self.world_map.pop(num)
                self.world_map.insert(num, 1)

    def place_fruit(self):
        if 2 in self.world_map:
            index = self.world_map.index(2)
            self.world_map.pop(index)
            self.world_map.insert(index, 0)
        run = True
        while run:
            num = randrange(self.SIZE * self.SIZE)
            if self.world_map[num] != 1:
                run = False
                self.world_map.pop(num)
                self.world_map.insert(num, 2)

    def print_world(self):
        print(len(self.world_map))
        for i in range(0, self.SIZE):
            start: int = 0 + i*20
            end: int = 20 + i*20
            print(self.world_map[start: end])



w = World(num_of_obstacles=30)
w.print_world()
w.place_fruit()
w.print_world()
w.place_fruit()
w.print_world()