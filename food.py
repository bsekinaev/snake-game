import random
import pygame  

class Food:
    def __init__(self, game_width, game_height, block_size):
        self.block_size = block_size
        self.position = [0, 0]
        self.randomize_position(game_width, game_height)
        
    def randomize_position(self, game_width, game_height):
        self.position = [
            round(random.randrange(0, game_width - self.block_size) / 10.0) * 10.0,
            round(random.randrange(0, game_height - self.block_size) / 10.0) * 10.0
        ]
    
    def draw(self, surface, color):
        pygame.draw.rect(surface, color, 
                        [self.position[0], self.position[1], 
                         self.block_size, self.block_size])
