import random
import pygame
import os

class Food:
    def __init__(self, game_width, game_height, block_size):
        self.block_size = block_size
        self.visual_size = int(block_size * 1.5)  # Еда будет больше блоков
        self.game_width = game_width
        self.game_height = game_height
        self.position = [0, 0]
        self.load_texture()
        self.randomize_position()  # Теперь метод существует
    
    def load_texture(self):
        """Загрузка текстуры еды"""
        try:
            if not os.path.exists('assets'):
                os.makedirs('assets')
            
            self.texture = pygame.image.load('assets/food.png').convert_alpha()
            self.texture = pygame.transform.scale(
                self.texture,
                (self.visual_size, self.visual_size)
            )
        except Exception as e:
            print(f"Не удалось загрузить текстуру еды: {e}. Будет использована цветная отрисовка.")
            self.texture = None
    
    def randomize_position(self):
        """Генерация случайной позиции для еды"""
        margin = self.visual_size
        self.position = [
            round(random.randrange(margin, self.game_width - margin) / 10.0) * 10.0,
            round(random.randrange(margin, self.game_height - margin) / 10.0) * 10.0
        ]
        return self.position
    def draw(self, surface, color):
        """Отрисовка еды"""
        if self.texture:
            # Центрируем увеличенную текстуру
            surface.blit(
                self.texture,
                (self.position[0] - (self.visual_size - self.block_size) // 2,
                 self.position[1] - (self.visual_size - self.block_size) // 2)
            )
        else:
            # Рисуем увеличенный круг
            pygame.draw.circle(
                surface,
                color,
                (
                    int(self.position[0] + self.block_size // 2),
                    int(self.position[1] + self.block_size // 2)
                ),
                self.visual_size // 2
            )