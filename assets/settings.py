import pygame
import json
import os

class Settings:
    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    BLUE = (50, 153, 213)
    GOLD = (255, 215, 0)
    
    # Размеры
    DIS_WIDTH = 800
    DIS_HEIGHT = 600
    BLOCK_SIZE = 20
    
    # Шрифты
    FONT_STYLE = "bahnschrift"
    SCORE_FONT = "comicsansms"
    
    # Уровни сложности
    LEVELS = {
        1: {"speed": 10, "name": "Лёгкий", "goal": 5},
        2: {"speed": 15, "name": "Средний", "goal": 10},
        3: {"speed": 20, "name": "Тяжёлый", "goal": 15}
    }
    
    # Звуковые файлы
    SOUND_FILES = {
        'background': 'assets/sounds/background.wav',
        'eat': 'assets/sounds/eat.wav',
        'crash': 'assets/sounds/crash.wav'
    }
    
    @staticmethod
    def ensure_directories_exist():
        """Создает необходимые директории, если они не существуют"""
        if not os.path.exists('assets/sounds'):
            os.makedirs('assets/sounds')
