import pygame
import random

class Obstacle:
    def __init__(self, x, y, size, speed=0):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.image = pygame.Surface((size, size))
        self.is_dangerous = False
        self.creation_time = pygame.time.get_ticks()
        self.update_color()

    def move(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

    def update_color(self):
        if not self.is_dangerous:
            self.image.fill((0, 255, 0))  # Green color for safe obstacles
        else:
            self.image.fill((255, 0, 0))  # Red color for dangerous obstacles

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.is_dangerous and current_time - self.creation_time >= 1000:  # 1000 ms = 1 second
            self.is_dangerous = True
            self.update_color()

    def draw(self, screen, offset_x, offset_y):
        screen_x = self.x + offset_x
        screen_y = self.y + offset_y
        screen.blit(self.image, (screen_x - self.size // 2, screen_y - self.size // 2))