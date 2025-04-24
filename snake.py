import pygame

class Snake:
    def __init__(self, dis_width, dis_height, block_size, head_texture=None, body_texture=None):
        self.block_size = block_size
        self.dis_width = dis_width
        self.dis_height = dis_height
        self.head_texture = head_texture
        self.body_texture = body_texture
        self.reset()
    
    def reset(self):
        x = round(self.dis_width / 2 / self.block_size) * self.block_size
        y = round(self.dis_height / 2 / self.block_size) * self.block_size
        self.body = [(x, y)]
        self.direction = "RIGHT"
        self.last_direction = "RIGHT"
    
    def change_direction(self, new_direction):
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if new_direction != opposite_directions.get(self.last_direction):
            self.direction = new_direction
    
    def move(self, food_pos):
        x, y = self.body[0]
        
        if self.direction == "UP":
            y -= self.block_size
        elif self.direction == "DOWN":
            y += self.block_size
        elif self.direction == "LEFT":
            x -= self.block_size
        elif self.direction == "RIGHT":
            x += self.block_size
        
        self.last_direction = self.direction
        
        if (x, y) == food_pos:
            self.body.insert(0, (x, y))
            return True
        else:
            self.body.insert(0, (x, y))
            self.body.pop()
            return False
    
    def check_collision(self):
        head = self.body[0]
        if (head[0] >= self.dis_width or head[0] < 0 or
            head[1] >= self.dis_height or head[1] < 0):
            return True
        if head in self.body[1:]:
            return True
        return False
    
    def draw(self, surface, color):
        for i, segment in enumerate(self.body):
            if i == 0:  # Голова
                if self.head_texture:
                    angle = 0
                    if self.direction == "UP":
                        angle = 90
                    elif self.direction == "DOWN":
                        angle = 270
                    elif self.direction == "LEFT":
                        angle = 180
                    rotated_head = pygame.transform.rotate(self.head_texture, angle)
                    surface.blit(rotated_head, segment)
                else:
                    pygame.draw.rect(surface, color, [segment[0], segment[1], self.block_size, self.block_size])
            else:  # Тело
                if self.body_texture:
                    surface.blit(self.body_texture, segment)
                else:
                    pygame.draw.rect(surface, color, [segment[0], segment[1], self.block_size, self.block_size])