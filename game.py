import pygame
import json
import os
import os.path
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # Цвета
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        
        # Настройки экрана
        self.dis_width = 800
        self.dis_height = 600
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Змейка')
        
        # Настройки игры
        self.clock = pygame.time.Clock()
        self.block_size = 20
        self.snake_speed = 15
        
        # Загрузка ресурсов
        self.background = self.load_background()
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        # Звуки
        try:
            self.background_music = pygame.mixer.Sound("background.wav")
            self.eat_sound = pygame.mixer.Sound("eat.wav")
            self.crash_sound = pygame.mixer.Sound("crash.wav")
            self.sound_enabled = True
        except:
            print("Звуковые файлы не найдены, игра будет без звука")
            self.sound_enabled = False
        
        # Уровни сложности
        self.levels = {
            1: {"speed": 10, "name": "Лёгкий", "goal": 5},
            2: {"speed": 15, "name": "Средний", "goal": 10},
            3: {"speed": 20, "name": "Тяжёлый", "goal": 15}
        }
        
        self.current_level = 1
        self.max_unlocked_level = 1
        self.load_progress()
        
        # Игровые объекты
        self.reset_game()
        
        if self.sound_enabled:
            self.background_music.play(-1)
    def load_background(self):
        """Загрузка фонового изображения"""
        try:
            # Создаем папку assets если ее нет
            if not os.path.exists('assets'):
                os.makedirs('assets')
            
            bg_path = 'assets/background.jpg'
            if os.path.exists(bg_path):
                background = pygame.image.load(bg_path).convert()
                return pygame.transform.scale(background, (self.dis_width, self.dis_height))
            else:
                print(f"Файл {bg_path} не найден")
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
        
        # Создаем простой фон если изображение не загрузилось
        background = pygame.Surface((self.dis_width, self.dis_height))
        background.fill(self.blue)
        return background
        
        # Создаем простой фон если изображение не загрузилось
        background = pygame.Surface((self.dis_width, self.dis_height))
        background.fill(self.blue)
        return background
    def load_progress(self):
        if os.path.exists("progress.json"):
            try:
                with open("progress.json", "r") as f:
                    data = json.load(f)
                    self.max_unlocked_level = data.get("max_unlocked_level", 1)
            except:
                self.max_unlocked_level = 1

    def save_progress(self):
        with open("progress.json", "w") as f:
            json.dump({"max_unlocked_level": self.max_unlocked_level}, f)

    def reset_game(self):
        self.snake = Snake(self.dis_width, self.dis_height,self.block_size)
        self.food = Food(self.dis_width, self.dis_height, self.block_size)
        if self.sound_enabled:
            self.background_music.stop()
            self.background_music.play(-1)

    def play_eat_sound(self):
        if self.sound_enabled:
            self.eat_sound.play()

    def play_crash_sound(self):
        if self.sound_enabled:
            self.crash_sound.play()

    def show_score(self, score):
        value = self.score_font.render(f"Счёт: {score} | Уровень: {self.current_level}", True, self.white)
        self.dis.blit(value, [0, 0])

    def message(self, msg, color, y_offset=0):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width/2 - mesg.get_width()/2, self.dis_height/3 + y_offset])

    def level_selection_menu(self):
        menu = True
        while menu:
            self.dis.fill(self.blue)
            
            title = self.font_style.render("Выберите уровень сложности", True, self.white)
            self.dis.blit(title, [self.dis_width//2 - title.get_width()//2, 50])
            
            level_buttons = []
            for i, level in self.levels.items():
                color = self.green if i <= self.max_unlocked_level else self.red
                level_text = f"{i}. {level['name']} (Скорость: {level['speed']}, Цель: {level['goal']})"
                text = self.font_style.render(level_text, True, color)
                
                button_x = self.dis_width//2 - text.get_width()//2
                button_y = 150 + i * 50
                
                pygame.draw.rect(self.dis, color, 
                               [button_x-10, button_y-5, text.get_width()+20, text.get_height()+10], 2)
                self.dis.blit(text, [button_x, button_y])
                
                level_buttons.append((i, pygame.Rect(button_x-10, button_y-5, 
                                                   text.get_width()+20, text.get_height()+10)))
            
            hint = self.font_style.render("Нажмите цифру уровня или кликните на него", True, self.white)
            self.dis.blit(hint, [self.dis_width//2 - hint.get_width()//2, self.dis_height-50])
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and 1 <= self.max_unlocked_level:
                        self.select_level(1)
                        menu = False
                    elif event.key == pygame.K_2 and 2 <= self.max_unlocked_level:
                        self.select_level(2)
                        menu = False
                    elif event.key == pygame.K_3 and 3 <= self.max_unlocked_level:
                        self.select_level(3)
                        menu = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for level, button in level_buttons:
                        if button.collidepoint(mouse_pos) and level <= self.max_unlocked_level:
                            self.select_level(level)
                            menu = False

    def select_level(self, level):
        self.current_level = level
        self.snake_speed = self.levels[level]["speed"]
        self.reset_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")
                elif event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_m:
                    self.sound_enabled = not self.sound_enabled
                    if self.sound_enabled:
                        pygame.mixer.unpause()
                    else:
                        pygame.mixer.pause()
        return True

    def game_loop(self):
        game_over = False
        game_close = False
        win = False
        
        while not game_over:
            while game_close or win: 
                if win:
                    self.message(f"Уровень {self.current_level} пройден!", self.green)
                    self.message("N - следующий уровень | Q - выход", self.white, 50)
                    
                    if self.current_level < len(self.levels):
                        self.max_unlocked_level = max(self.max_unlocked_level, self.current_level + 1)
                        self.save_progress()
                else:
                    self.message("Вы проиграли!", self.red)
                    self.message("C - заново | Q - выход", self.white, 50)
                
                self.show_score(len(self.snake.body) - 1)
                pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False
                        win = False
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                            win = False
                        if event.key == pygame.K_c and not win:
                            self.reset_game()
                            game_close = False
                        if event.key == pygame.K_n and win:
                            if self.current_level < len(self.levels):
                                self.current_level += 1
                                self.select_level(self.current_level)
                            else:
                                self.level_selection_menu()
                            win = False
            
            if not self.handle_events():
                break
                
            if self.snake.move(self.food.position):
                self.food.randomize_position()
                self.play_eat_sound()
                
                if len(self.snake.body) - 1 >= self.levels[self.current_level]["goal"]:
                    win = True
            self.dis.blit(self.background, (0, 0))
            self.dis.fill(self.black)
            self.food.draw(self.dis, self.red)
            self.snake.draw(self.dis, self.green)
            self.show_score(len(self.snake.body) - 1)
            
            pygame.display.update()
            
            if self.snake.check_collision():
                self.play_crash_sound()
                game_close = True
            
            self.clock.tick(self.snake_speed)

    def show_win_message(self):
        """Показать сообщение о победе"""
        font = pygame.font.SysFont(None, 55)
        text = font.render('YOU WIN!', True, (255, 215, 0))  # Золотой цвет
        self.dis.blit(text, [self.dis_width/2 - 100, self.dis_height/2])
        pygame.display.update()
        pygame.time.wait(2000)    
        
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game()
    game.level_selection_menu()
    game.game_loop()