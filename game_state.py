import pygame
import random
from player import Player
from target import Target
from obstacle import Obstacle

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()
        self.font = pygame.font.Font(None, 36)
        self.start_screen = True
        self.high_score_screen = False
        self.game_over = False
        self.high_scores = self.load_high_scores()
        self.difficulty = "Easy"
        self.world_offset_x = 0
        self.world_offset_y = 0
        self.obstacles = []
        self.volume = 0.1  # Default volume at 10%
        self.player_name = ""
        self.entering_name = False

    def reset(self):
        initial_player_size = 30
        self.player = Player(self.width // 2, self.height // 2, initial_player_size)
        self.targets = []
        self.obstacles = []
        self.score = 0
        self.target_spawn_timer = 0
        self.target_spawn_interval = 60
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_interval = 120
        self.start_screen = False
        self.game_over = False
        self.world_offset_x = 0
        self.world_offset_y = 0

    def start_game(self):
        self.start_screen = False
        self.reset()

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a] + keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_s] - keys[pygame.K_w] + keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.player.move(dx, dy)
        
        self.world_offset_x -= dx * self.player.speed
        self.world_offset_y -= dy * self.player.speed

        self.target_spawn_timer += 1
        if self.target_spawn_timer >= self.target_spawn_interval:
            self.spawn_target()
            self.target_spawn_timer = 0

        self.obstacle_spawn_timer += 1
        if self.obstacle_spawn_timer >= self.obstacle_spawn_interval:
            self.spawn_obstacle()
            self.obstacle_spawn_timer = 0

        for target in self.targets:
            target.grow()

        for obstacle in self.obstacles:
            obstacle.move()
            obstacle.update()  # Add this line to update obstacle status

        self.update_difficulty()
        self.update_player_stars()

    def spawn_target(self):
        margin = max(self.player.size * 2, 50)
        while True:
            x = random.randint(-self.world_offset_x, self.width - self.world_offset_x)
            y = random.randint(-self.world_offset_y, self.height - self.world_offset_y)
            dx = x - (self.width // 2)
            dy = y - (self.height // 2)
            distance = (dx**2 + dy**2)**0.5
            if distance > margin:
                size = self.player.size // 2
                if self.difficulty == "Medium":
                    size *= 1.2
                elif self.difficulty == "Hard":
                    size *= 1.5
                elif self.difficulty == "Extreme":
                    size *= 2
                self.targets.append(Target(x, y, size))
                break

    def spawn_obstacle(self):
        margin = max(self.player.size * 2, 50)
        while True:
            x = random.randint(-self.world_offset_x, self.width - self.world_offset_x)
            y = random.randint(-self.world_offset_y, self.height - self.world_offset_y)
            dx = x - (self.width // 2)
            dy = y - (self.height // 2)
            distance = (dx**2 + dy**2)**0.5
            if distance > margin:
                size = self.player.size * 0.75  # Decreased obstacle size
                speed = 0
                if self.difficulty == "Medium":
                    speed = 1
                elif self.difficulty == "Hard":
                    speed = 2
                elif self.difficulty == "Extreme":
                    speed = 3
                self.obstacles.append(Obstacle(x, y, size, speed))
                break

    def check_collect(self):
        player_center_x = self.width // 2
        player_center_y = self.height // 2
        for target in self.targets[:]:
            target_screen_x = target.x + self.world_offset_x
            target_screen_y = target.y + self.world_offset_y
            if (abs(player_center_x - target_screen_x) < (self.player.size + target.size) // 2 and
                abs(player_center_y - target_screen_y) < (self.player.size + target.size) // 2):
                if self.player.size > target.size:
                    self.targets.remove(target)
                    self.score += int(target.size)
                    self.player.grow()
                    return True
        return False

    def check_game_over(self):
        player_center_x = self.width // 2
        player_center_y = self.height // 2
        for target in self.targets:
            if target.size > self.player.size:
                self.game_over = True
                return True
        for obstacle in self.obstacles:
            obstacle_screen_x = obstacle.x + self.world_offset_x
            obstacle_screen_y = obstacle.y + self.world_offset_y
            if (abs(player_center_x - obstacle_screen_x) < (self.player.size + obstacle.size) // 2 and
                abs(player_center_y - obstacle_screen_y) < (self.player.size + obstacle.size) // 2):
                if obstacle.is_dangerous:  # Only end the game if the obstacle is dangerous (red)
                    self.game_over = True
                    return True
        return False

    def draw(self, screen):
        self.player.draw(screen, self.width // 2, self.height // 2)
        for target in self.targets:
            target.draw(screen, self.world_offset_x, self.world_offset_y)
        for obstacle in self.obstacles:
            obstacle.draw(screen, self.world_offset_x, self.world_offset_y)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        difficulty_text = self.font.render(f"Difficulty: {self.difficulty}", True, (255, 255, 255))
        screen.blit(difficulty_text, (10, 50))

    def update_difficulty(self):
        if self.score < 1000:
            self.difficulty = "Easy"
        elif self.score < 5000:
            self.difficulty = "Medium"
        elif self.score < 10000:
            self.difficulty = "Hard"
        else:
            self.difficulty = "Extreme"

    def update_player_stars(self):
        if self.score >= 10000 and self.player.stars < 3:
            self.player.stars = 3
        elif self.score >= 5000 and self.player.stars < 2:
            self.player.stars = 2
        elif self.score >= 1000 and self.player.stars < 1:
            self.player.stars = 1

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as f:
                scores = []
                for line in f.readlines():
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        name, score = parts
                        if score.isdigit():
                            scores.append((name, int(score)))
                        else:
                            scores.append((name, 0))
                    else:
                        scores.append(("Anonymous", 0))
                return scores
        except FileNotFoundError:
            return []

    def update_high_scores(self):
        if self.player_name:
            self.high_scores.append((self.player_name, self.score))
        else:
            self.high_scores.append(("Anonymous", self.score))
        
        # Sort high scores, handling cases where the score might be invalid
        self.high_scores.sort(key=lambda x: x[1] if isinstance(x[1], int) else 0, reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only top 5 scores
        
        with open("high_scores.txt", "w") as f:
            for name, score in self.high_scores:
                f.write(f"{name},{score}\n")

    def draw_start_screen(self, screen):
        title = self.font.render("Siki's Smoking Adventure", True, (255, 255, 255))
        start = self.font.render("Press ENTER to start", True, (255, 255, 255))
        high_scores = self.font.render("Press H for High Scores", True, (255, 255, 255))
        volume_text = self.font.render(f"Volume: {int(self.volume * 100)}%", True, (255, 255, 255))
        volume_up = self.font.render("Press UP to increase volume", True, (255, 255, 255))
        volume_down = self.font.render("Press DOWN to decrease volume", True, (255, 255, 255))

        screen.blit(title, (self.width // 2 - title.get_width() // 2, self.height // 2 - 100))
        screen.blit(start, (self.width // 2 - start.get_width() // 2, self.height // 2))
        screen.blit(high_scores, (self.width // 2 - high_scores.get_width() // 2, self.height // 2 + 50))
        screen.blit(volume_text, (self.width // 2 - volume_text.get_width() // 2, self.height // 2 + 100))
        screen.blit(volume_up, (self.width // 2 - volume_up.get_width() // 2, self.height // 2 + 150))
        screen.blit(volume_down, (self.width // 2 - volume_down.get_width() // 2, self.height // 2 + 200))

    def draw_high_score_screen(self, screen):
        title = self.font.render("High Scores", True, (255, 255, 255))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

        for i, (name, score) in enumerate(self.high_scores):
            score_text = self.font.render(f"{i+1}. {name}: {score}", True, (255, 255, 255))
            screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 100 + i * 50))

        back = self.font.render("Press B to go back", True, (255, 255, 255))
        screen.blit(back, (self.width // 2 - back.get_width() // 2, self.height - 100))

    def handle_volume(self, change):
        self.volume = max(0, min(1, self.volume + change))
        pygame.mixer.music.set_volume(self.volume)

    def draw_game_over(self, screen):
        game_over = self.font.render("Game Over!", True, (255, 255, 255))
        score = self.font.render(f"Your score: {self.score}", True, (255, 255, 255))
        enter_name = self.font.render("Enter your name (optional):", True, (255, 255, 255))
        name = self.font.render(self.player_name, True, (255, 255, 255))
        restart = self.font.render("Press ENTER to save and restart", True, (255, 255, 255))
        
        screen.blit(game_over, (self.width // 2 - game_over.get_width() // 2, self.height // 2 - 100))
        screen.blit(score, (self.width // 2 - score.get_width() // 2, self.height // 2 - 50))
        screen.blit(enter_name, (self.width // 2 - enter_name.get_width() // 2, self.height // 2))
        screen.blit(name, (self.width // 2 - name.get_width() // 2, self.height // 2 + 50))
        screen.blit(restart, (self.width // 2 - restart.get_width() // 2, self.height // 2 + 100))