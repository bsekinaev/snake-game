import pygame
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Инициализация звуковой системы
        
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
        self.block_size = 10
        self.snake_speed = 15
        
        # Шрифты
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
        
        # Игровые объекты
        self.snake = Snake(self.dis_width, self.dis_height)
        self.food = Food(self.dis_width, self.dis_height, self.block_size)
        
        # Воспроизведение фоновой музыки
        if self.sound_enabled:
            self.background_music.play(-1)

    def play_eat_sound(self):
        if self.sound_enabled:
            self.eat_sound.play()

    def play_crash_sound(self):
        if self.sound_enabled:
            self.crash_sound.play()

    def show_score(self, score):
        value = self.score_font.render(f"Ваш счет: {score}", True, self.white)
        self.dis.blit(value, [0, 0])

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width/6, self.dis_height/3])

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
                    if self.sound_enabled:
                        pygame.mixer.pause()
                        self.sound_enabled = False
                    else:
                        pygame.mixer.unpause()
                        self.sound_enabled = True
        return True

    def game_loop(self):
        game_over = False
        game_close = False
        
        while not game_over:
            while game_close:
                self.dis.fill(self.blue)
                self.message("Проиграли! Q-выход C-заново", self.red)
                self.show_score(len(self.snake.body) - 1)
                pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            if self.sound_enabled:
                                self.background_music.stop()
                                self.background_music.play(-1)
                            self.snake = Snake(self.dis_width, self.dis_height)
                            self.food = Food(self.dis_width, self.dis_height, self.block_size)
                            game_close = False
            
            if not self.handle_events():
                break
                
            if self.snake.move(self.food.position):
                self.food.randomize_position(self.dis_width, self.dis_height)
                self.play_eat_sound()
            
            self.dis.fill(self.black)
            self.food.draw(self.dis, self.red)
            self.snake.draw(self.dis, self.green)
            self.show_score(len(self.snake.body) - 1)
            
            pygame.display.update()
            
            if self.snake.check_collision(self.dis_width, self.dis_height):
                self.play_crash_sound()
                game_close = True
            
            self.clock.tick(self.snake_speed)
        
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
