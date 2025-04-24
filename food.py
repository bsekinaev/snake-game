import pygame
import random

class Food:
    def __init__(self, dis_width, dis_height, block_size, food_texture=None):
        self.block_size = block_size
        self.dis_width = dis_width
        self.dis_height = dis_height
        self.food_texture = food_texture
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        x = round(random.randrange(0, self.dis_width - self.block_size) / self.block_size) * self.block_size
        y = round(random.randrange(0, self.dis_height - self.block_size) / self.block_size) * self.block_size
        self.position = (x, y)
    
    def draw(self, surface, color):
        if self.food_texture:
            surface.blit(self.food_texture, self.position)
        else:
            pygame.draw.rect(surface, color, [self.position[0], self.position[1], self.block_size, self.block_size])