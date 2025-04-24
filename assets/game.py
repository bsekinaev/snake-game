import pygame
import json
import os
from settings import Settings
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        # Инициализация pygame и микшера для звуков
        pygame.init()
        pygame.mixer.init()
        
        # Загрузка настроек из settings.py
        self.settings = Settings()
        Settings.ensure_directories_exist()  # Создание необходимых директорий
        
        # Флаг для отслеживания играющей музыки
        self.music_playing = False
        
        # Создание игрового окна
        self.dis = pygame.display.set_mode((self.settings.DIS_WIDTH, self.settings.DIS_HEIGHT))
        pygame.display.set_caption('Змейка')
        
        # Инициализация игровых компонентов
        self.clock = pygame.time.Clock()
        self.background = self._load_background()  # Загрузка фона
        self._init_sounds()  # Инициализация звуков
        self._load_progress()  # Загрузка прогресса игры
        self.records = self._load_records()  # Загрузка рекордов
        self.current_player = ""  # Текущий игрок
        self.current_level = 1  # Текущий уровень
        self.reset_game()  # Сброс игры в начальное состояние
    
    def _load_background(self):
        """Загружает фоновое изображение или создает синий фон по умолчанию"""
        try:
            bg_path = 'assets/background.jpg'
            if os.path.exists(bg_path):
                background = pygame.image.load(bg_path).convert()
                return pygame.transform.scale(background, (self.settings.DIS_WIDTH, self.settings.DIS_HEIGHT))
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")
        
        # Создание фона по умолчанию
        background = pygame.Surface((self.settings.DIS_WIDTH, self.settings.DIS_HEIGHT))
        background.fill(self.settings.BLUE)
        return background
    
    def _init_sounds(self):
        """Инициализирует звуковые эффекты игры"""
        self.sound_enabled = True
        self.sounds = {}  # Словарь для хранения звуков
        
        try:
            # Загрузка звуков из настроек
            for name, path in self.settings.SOUND_FILES.items():
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                else:
                    # Создание пустого звука, если файл не найден
                    self.sounds[name] = pygame.mixer.Sound(buffer=bytes(44))
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")
            self.sound_enabled = False
    
    def _load_progress(self):
        """Загружает прогресс игрока из файла"""
        try:
            if os.path.exists("progress.json"):
                with open("progress.json", "r") as f:
                    data = json.load(f)
                    self.max_unlocked_level = data.get("max_unlocked_level", 1)
            else:
                self.max_unlocked_level = 1
        except:
            self.max_unlocked_level = 1
    
    def _load_records(self):
        """Загружает таблицу рекордов из файла"""
        try:
            if os.path.exists("records.json"):
                with open("records.json", "r") as f:
                    return json.load(f)
        except:
            return {"levels": {}, "players": {}}
    
    def _save_progress(self):
        """Сохраняет прогресс игрока в файл"""
        with open("progress.json", "w") as f:
            json.dump({"max_unlocked_level": self.max_unlocked_level}, f)
    
    def _save_records(self):
        """Сохраняет таблицу рекордов в файл"""
        with open("records.json", "w") as f:
            json.dump(self.records, f)
    
    def reset_game(self):
        """Сбрасывает игру в начальное состояние"""
        try:
            # Загрузка текстур для змейки и еды
            food_texture = pygame.image.load('assets/food.png').convert_alpha()
            food_texture = pygame.transform.scale(food_texture, (self.settings.BLOCK_SIZE, self.settings.BLOCK_SIZE))
            head_texture = pygame.image.load('assets/snake_head.png').convert_alpha()
            head_texture = pygame.transform.scale(head_texture, (self.settings.BLOCK_SIZE, self.settings.BLOCK_SIZE))
            body_texture = pygame.image.load('assets/snake_body.png').convert_alpha()
            body_texture = pygame.transform.scale(body_texture, (self.settings.BLOCK_SIZE, self.settings.BLOCK_SIZE))
        except Exception as e:
            print(f"Ошибка загрузки текстур: {e}")
            food_texture = head_texture = body_texture = None
        
        # Создание змейки и еды
        self.snake = Snake(
            self.settings.DIS_WIDTH, 
            self.settings.DIS_HEIGHT, 
            self.settings.BLOCK_SIZE,
            head_texture=head_texture,
            body_texture=body_texture
        )
        self.food = Food(
            self.settings.DIS_WIDTH, 
            self.settings.DIS_HEIGHT, 
            self.settings.BLOCK_SIZE,
            food_texture=food_texture
        )
        
        # Воспроизведение фоновой музыки
        if self.sound_enabled and 'background' in self.sounds and not self.music_playing:
            self.sounds['background'].play(-1)  # -1 означает бесконечный цикл
            self.music_playing = True
    
    def _update_record(self, player_name=None):
        """Обновляет таблицу рекордов"""
        current_score = len(self.snake.body) - 1
        level_key = str(self.current_level)
        
        if player_name:
            # Обновление рекордов для конкретного игрока
            if "players" not in self.records:
                self.records["players"] = {}
            if level_key not in self.records["players"]:
                self.records["players"][level_key] = []
            
            self.records["players"][level_key].append({
                "name": player_name,
                "score": current_score
            })
            # Сортировка и сохранение только топ-10 результатов
            self.records["players"][level_key].sort(key=lambda x: x["score"], reverse=True)
            self.records["players"][level_key] = self.records["players"][level_key][:10]
        
        # Обновление общего рекорда для уровня
        if "levels" not in self.records:
            self.records["levels"] = {}
        
        if current_score > self.records["levels"].get(level_key, 0):
            self.records["levels"][level_key] = current_score
        
        self._save_records()
    
    def _get_player_name(self):
        """Отображает экран ввода имени игрока"""
        input_active = True
        player_name = ""
        font = pygame.font.SysFont(self.settings.FONT_STYLE, 40)
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
            
            # Отрисовка экрана ввода имени
            self.dis.fill(self.settings.BLACK)
            prompt = font.render("Введите ваше имя:", True, self.settings.WHITE)
            name_text = font.render(player_name, True, self.settings.WHITE)
            
            self.dis.blit(prompt, (self.settings.DIS_WIDTH//2 - prompt.get_width()//2, 
                         self.settings.DIS_HEIGHT//2 - 50))
            self.dis.blit(name_text, (self.settings.DIS_WIDTH//2 - name_text.get_width()//2, 
                          self.settings.DIS_HEIGHT//2))
            
            pygame.display.flip()
            self.clock.tick(30)
        
        return player_name if player_name else "Игрок"
    
    def _show_leaderboard(self, level=None):
        """Отображает таблицу рекордов для указанного уровня"""
        if level is None:
            level = self.current_level
        
        showing = True
        font_title = pygame.font.SysFont(self.settings.FONT_STYLE, 40)
        font_item = pygame.font.SysFont(self.settings.FONT_STYLE, 30)
        
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    showing = False
            
            self.dis.fill(self.settings.BLACK)
            
            title = font_title.render(f"Таблица рекордов (Уровень {level})", True, self.settings.WHITE)
            self.dis.blit(title, (self.settings.DIS_WIDTH//2 - title.get_width()//2, 30))
            
            y_offset = 100
            level_key = str(level)
            
            # Отрисовка рекордов
            if "players" in self.records and level_key in self.records["players"]:
                for i, record in enumerate(self.records["players"][level_key]):
                    if i >= 10: break
                    record_text = f"{i+1}. {record['name']}: {record['score']}"
                    text = font_item.render(record_text, True, self.settings.WHITE)
                    self.dis.blit(text, (self.settings.DIS_WIDTH//2 - text.get_width()//2, y_offset))
                    y_offset += 40
            else:
                no_records = font_item.render("Рекордов пока нет!", True, self.settings.WHITE)
                self.dis.blit(no_records, (self.settings.DIS_WIDTH//2 - no_records.get_width()//2, y_offset))
            
            hint = font_item.render("Нажмите любую клавишу для продолжения", True, self.settings.WHITE)
            self.dis.blit(hint, (self.settings.DIS_WIDTH//2 - hint.get_width()//2, 
                              self.settings.DIS_HEIGHT - 50))
            
            pygame.display.flip()
            self.clock.tick(30)
        
        return True
    
    def _play_sound(self, sound_name):
        """Воспроизводит звуковой эффект"""
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def _toggle_sound(self):
        """Включает/выключает звук"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            pygame.mixer.unpause()
            if not self.music_playing and 'background' in self.sounds:
                self.sounds['background'].play(-1)
                self.music_playing = True
        else:
            pygame.mixer.pause()
            self.music_playing = False
    
    def show_score(self):
        """Отображает текущий счет, рекорд и уровень"""
        score = len(self.snake.body) - 1
        level = self.current_level
        record = self.records["levels"].get(str(level), 0) if "levels" in self.records else 0
        
        font = pygame.font.SysFont(self.settings.SCORE_FONT, 35)
        score_text = f"Счёт: {score} | Рекорд: {record} | Уровень: {self.settings.LEVELS[level]['name']}"
        text = font.render(score_text, True, self.settings.WHITE)
        self.dis.blit(text, [10, 10])
    
    def show_message(self, text, color, y_offset=0, font_size=25):
        """Отображает сообщение на экране"""
        font = pygame.font.SysFont(self.settings.FONT_STYLE, font_size)
        message = font.render(text, True, color)
        x_pos = self.settings.DIS_WIDTH // 2 - message.get_width() // 2
        y_pos = self.settings.DIS_HEIGHT // 3 + y_offset
        self.dis.blit(message, [x_pos, y_pos])
    
    def level_selection_menu(self):
        """Отображает меню выбора уровня"""
        menu = True
        show_leaderboard = False
        
        while menu:
            self.dis.fill(self.settings.BLUE)
            
            if show_leaderboard:
                if not self._show_leaderboard(self.current_level):
                    return False
                show_leaderboard = False
                continue
            
            title_font = pygame.font.SysFont(self.settings.FONT_STYLE, 30)
            title_text = title_font.render("Выберите уровень сложности", True, self.settings.WHITE)
            self.dis.blit(title_text, [self.settings.DIS_WIDTH//2 - title_text.get_width()//2, 50])
            
            level_buttons = []
            font = pygame.font.SysFont(self.settings.FONT_STYLE, 25)
            
            # Создание кнопок для каждого уровня
            for i, level in self.settings.LEVELS.items():
                color = self.settings.GREEN if i <= self.max_unlocked_level else self.settings.RED
                level_text = f"{i}. {level['name']} (Скорость: {level['speed']}, Цель: {level['goal']})"
                text = font.render(level_text, True, color)
                
                button_x = self.settings.DIS_WIDTH//2 - text.get_width()//2 - 10
                button_y = 150 + i * 50 - 5
                
                pygame.draw.rect(self.dis, color, 
                               [button_x, button_y, 
                                text.get_width() + 20, text.get_height() + 10], 2)
                self.dis.blit(text, [button_x + 10, button_y + 5])
                
                level_buttons.append((i, pygame.Rect(button_x, button_y, 
                                               text.get_width() + 20, text.get_height() + 10)))
            
            # Кнопка таблицы рекордов
            records_font = pygame.font.SysFont(self.settings.FONT_STYLE, 25)
            records_text = records_font.render("Таблица рекордов (R)", True, self.settings.WHITE)
            records_rect = pygame.Rect(
                self.settings.DIS_WIDTH//2 - records_text.get_width()//2 - 10,
                self.settings.DIS_HEIGHT - 100,
                records_text.get_width() + 20,
                records_text.get_height() + 10
            )
            pygame.draw.rect(self.dis, self.settings.GOLD, records_rect, 2)
            self.dis.blit(records_text, [
                self.settings.DIS_WIDTH//2 - records_text.get_width()//2,
                self.settings.DIS_HEIGHT - 95
            ])
            
            pygame.display.update()
            
            # Обработка событий в меню
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_3:
                        level = event.key - pygame.K_0
                        if level <= self.max_unlocked_level:
                            self.current_level = level
                            self.snake_speed = self.settings.LEVELS[level]["speed"]
                            return True
                    elif event.key == pygame.K_r:
                        show_leaderboard = True
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for level, button in level_buttons:
                        if button.collidepoint(mouse_pos) and level <= self.max_unlocked_level:
                            self.current_level = level
                            self.snake_speed = self.settings.LEVELS[level]["speed"]
                            return True
                    
                    if records_rect.collidepoint(mouse_pos):
                        show_leaderboard = True
        
        return True
    
    def _select_level(self, level):
        """Выбирает уровень и сбрасывает игру"""
        self.current_level = level
        self.snake_speed = self.settings.LEVELS[level]["speed"]
        self.reset_game()
    
    def handle_events(self):
        """Обрабатывает события ввода"""
        KEY_ACTIONS = {
            pygame.K_LEFT: lambda: self.snake.change_direction("LEFT"),
            pygame.K_RIGHT: lambda: self.snake.change_direction("RIGHT"),
            pygame.K_UP: lambda: self.snake.change_direction("UP"),
            pygame.K_DOWN: lambda: self.snake.change_direction("DOWN"),
            pygame.K_m: self._toggle_sound
        }
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in KEY_ACTIONS:
                KEY_ACTIONS[event.key]()
        return True
    
    def _process_game_logic(self):
        """Обрабатывает игровую логику"""
        if not self.handle_events():
            return False
            
        if self.snake.move(self.food.position):
            self._play_sound('eat')
            self.food.randomize_position()
            
            current_score = len(self.snake.body) - 1
            level_goal = self.settings.LEVELS[self.current_level]["goal"]
            
            if current_score >= level_goal:
                self._handle_level_completion()
                return "win"
            
        return True
    
    def _handle_level_completion(self):
        """Обрабатывает завершение уровня"""
        if self.current_level < len(self.settings.LEVELS):
            self.max_unlocked_level = max(self.max_unlocked_level, self.current_level + 1)
            self._save_progress()
    
    def _handle_game_end(self, win=False):
        """Обрабатывает завершение игры (победу или поражение)"""
        if win:
            self._update_record()
        else:
            # Только при проигрыше проверяем рекорд и запрашиваем имя
            level_key = str(self.current_level)
            current_score = len(self.snake.body) - 1
            current_record = self.records["levels"].get(level_key, 0) if "levels" in self.records else 0
            
            if current_score > current_record:
                player_name = self._get_player_name()
                if player_name:
                    self._update_record(player_name)
                    self._show_leaderboard()
                else:
                    return "quit"
        
        # Отображение меню после завершения игры
        while True:
            self.dis.fill(self.settings.BLACK)
            
            if win:
                self.show_message(f"Уровень {self.current_level} пройден!", self.settings.GREEN)
                options = [
                    "N - следующий уровень",
                    "M - вернуться в меню",
                    "Q - выход"
                ]
            else:
                self.show_message("Вы проиграли!", self.settings.RED)
                options = [
                    "C - заново",
                    "M - вернуться в меню",
                    "Q - выход"
                ]
            
            for i, option in enumerate(options):
                self.show_message(option, self.settings.WHITE, 50 + i * 40)
            
            self.show_score()
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return "quit"
                    if event.key == pygame.K_c and not win:
                        return "retry"
                    if event.key == pygame.K_n and win:
                        if self.current_level < len(self.settings.LEVELS):
                            self.current_level += 1
                            self._select_level(self.current_level)
                            return "continue"
                        else:
                            return "menu"
                    if event.key == pygame.K_m:
                        return "menu"
    
    def _render_game(self):
        """Отрисовывает игровое поле"""
        self.dis.blit(self.background, (0, 0))
        self.food.draw(self.dis, self.settings.RED)
        self.snake.draw(self.dis, self.settings.GREEN)
        self.show_score()
        pygame.display.update()
    
    def game_loop(self):
        """Основной игровой цикл"""
        running = True
        while running:
            if not self.level_selection_menu():
                break
            
            game_active = True
            while game_active:
                if not self.handle_events():
                    running = False
                    break
                
                result = None
                if self.snake.move(self.food.position):
                    self._play_sound('eat')
                    self.food.randomize_position()
                    
                    current_score = len(self.snake.body) - 1
                    level_goal = self.settings.LEVELS[self.current_level]["goal"]
                    
                    if current_score >= level_goal:
                        self._handle_level_completion()
                        result = "win"
                
                if self.snake.check_collision():
                    self._play_sound('crash')
                    result = "lose"
                
                self._render_game()
                self.clock.tick(self.snake_speed)
                
                if result in ("win", "lose"):
                    action = self._handle_game_end(win=(result == "win"))
                    if action == "quit":
                        running = False
                        break
                    elif action == "menu":
                        break
                    elif action == "retry":
                        self.reset_game()
                    elif action == "continue":
                        continue

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()