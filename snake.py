import pygame  # Добавьте импорт pygame

class Snake:
    def __init__(self, game_width, game_height):
        self.position = [game_width//2, game_height//2]
        self.body = [[game_width//2, game_height//2]]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.block_size = 10
        
    def change_direction(self, new_direction):
        if new_direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if new_direction == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if new_direction == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if new_direction == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"
    
    def move(self, food_pos):
        if self.direction == "RIGHT":
            self.position[0] += self.block_size
        if self.direction == "LEFT":
            self.position[0] -= self.block_size
        if self.direction == "UP":
            self.position[1] -= self.block_size
        if self.direction == "DOWN":
            self.position[1] += self.block_size
            
        self.body.insert(0, list(self.position))
        if self.position == food_pos:
            return True
        else:
            self.body.pop()
            return False
    
    def check_collision(self, game_width, game_height):
        if (self.position[0] >= game_width or self.position[0] < 0 or
            self.position[1] >= game_height or self.position[1] < 0):
            return True
        for block in self.body[1:]:
            if self.position == block:
                return True
        return False
    
    def draw(self, surface, color):
        for block in self.body:
            pygame.draw.rect(surface, color, 
                           [block[0], block[1], 
                            self.block_size, self.block_size])
