import pygame
import random

class Target:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.growth_rate = 0.05
        self.image = pygame.image.load("assets/cigarrette.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def grow(self):
        self.size += self.growth_rate
        self.image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))

    def draw(self, screen, offset_x, offset_y):
        screen_x = self.x + offset_x
        screen_y = self.y + offset_y
        screen.blit(self.image, (screen_x - self.size // 2, screen_y - self.size // 2))