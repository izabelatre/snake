import pygame
from Snake_Game.snake import *
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

pygame.display.set_caption('Snake Game')
screen = pygame.display.set_mode((screen_width, screen_height))

apple_img = pygame.image.load('apple.png')
grass_img = pygame.image.load('grass.JPG')
end_img = pygame.image.load('end.JPG')

class World():
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    self.load_image(image=end_img, col=col_count, row=row_count)
                if tile == 0:
                    self.load_image(image=grass_img, col=col_count, row=row_count)
                col_count += 1
            row_count += 1

    def load_image(self, image: pygame.image, col: int, row: int):
        img = pygame.transform.scale(image, (cell_size, cell_size))
        img_rect = img.get_rect()
        img_rect.x = col * cell_size
        img_rect.y = row * cell_size
        tile = (img, img_rect)
        self.tile_list.append(tile)

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# class Snake_head():
#     def __init__(self,x,y):
#         self.image = pygame.transform.scale(head_img, (30, 30))
#         self.rect = self.image.get_rect()
#         self.rect.x =x
#         self.rect.y =y
#
#     def update(self):
#         screen.blit(self.image,self.rect)


snake_pos =[[int(screen_width/2), int(screen_height/2)]]
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size])
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size*2])
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size*3] )


bg = (200, 200, 150)


run = True;
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run == False

    pygame.display.update()

pygame.quit



