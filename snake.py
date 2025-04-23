import pygame
import os

class Snake:
    def __init__(self, game_width, game_height, block_size):
        self.block_size = block_size
        self.game_width = game_width
        self.game_height = game_height
        self.position = [game_width // 2, game_height // 2]
        self.body = [[game_width // 2, game_height // 2]]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.head_visual_size = int(block_size * 1.2)
        self.load_textures()

    def load_textures(self):
        """Загрузка текстур для змейки"""
        try:
            if not os.path.exists('assets'):
                os.makedirs('assets')
                
            self.head_texture = pygame.image.load('assets/snake_head.png').convert_alpha()
            self.head_texture = pygame.transform.scale(
                self.head_texture, 
                (self.head_visual_size, self.head_visual_size)
            )
            
            self.body_texture = pygame.image.load('assets/snake_body.png').convert_alpha()
            self.body_texture = pygame.transform.scale(
                self.body_texture, 
                (self.block_size, self.block_size)
            )
        except Exception as e:
            print(f"Текстуры змейки не загружены: {e}. Используется цветная отрисовка.")
            self.head_texture = None
            self.body_texture = None

    def move(self, food_pos):
        """Движение змейки"""
        # Изменение позиции головы
        if self.direction == "RIGHT":
            self.position[0] += self.block_size
        elif self.direction == "LEFT":
            self.position[0] -= self.block_size
        elif self.direction == "UP":
            self.position[1] -= self.block_size
        elif self.direction == "DOWN":
            self.position[1] += self.block_size
        
        # Добавление новой позиции в начало тела
        self.body.insert(0, list(self.position))
        
        # Проверка, съела ли змейка еду
         # Проверяем столкновение с едой (точное сравнение координат)
        if (abs(self.position[0] - food_pos[0]) < self.block_size and 
            abs(self.position[1] - food_pos[1]) < self.block_size):
            return True  # Еда съедена
        else:
            self.body.pop()  # Удаляем хвост, если не ели
            return False

    def change_direction(self, new_direction):
        """Изменение направления движения"""
        if (new_direction == "RIGHT" and not self.direction == "LEFT" or
            new_direction == "LEFT" and not self.direction == "RIGHT" or
            new_direction == "UP" and not self.direction == "DOWN" or
            new_direction == "DOWN" and not self.direction == "UP"):
            self.direction = new_direction

    def check_collision(self):
        """Проверка столкновений"""
        # С границами экрана
        if (self.position[0] >= self.game_width or self.position[0] < 0 or
            self.position[1] >= self.game_height or self.position[1] < 0):
            return True
        
        # С собственным телом (кроме головы)
        for block in self.body[1:]:
            if self.position == block:
                return True
                
        return False

    def draw(self, surface, color):
        """Отрисовка змейки"""
        for i, block in enumerate(self.body):
            if i == 0:  # Голова
                if self.head_texture:
                    rotated_head = self.rotate_head()
                    surface.blit(
                        rotated_head,
                        (block[0] - (self.head_visual_size - self.block_size) // 2,
                         block[1] - (self.head_visual_size - self.block_size) // 2)
                    )
                else:
                    pygame.draw.rect(
                        surface, color,
                        [block[0], block[1], self.block_size, self.block_size],
                        border_radius=3
                    )
            else:  # Тело
                if self.body_texture:
                    surface.blit(self.body_texture, (block[0], block[1]))
                else:
                    pygame.draw.rect(
                        surface, color,
                        [block[0], block[1], self.block_size, self.block_size],
                        border_radius=2
                    )

    def rotate_head(self):
        """Поворот текстуры головы согласно направлению"""
        angle = {
            "RIGHT": 0,
            "UP": 90,
            "LEFT": 180,
            "DOWN": 270
        }.get(self.direction, 0)
        return pygame.transform.rotate(self.head_texture, angle)