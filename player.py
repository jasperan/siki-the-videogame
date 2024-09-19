import pygame

class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 5
        original_image = pygame.image.load("assets/player.png").convert_alpha()
        new_size = (int(original_image.get_width() * 0.1), int(original_image.get_height() * 0.1))
        self.image = pygame.transform.scale(original_image, new_size)
        self.size = new_size[0]
        self.stars = 0
        self.star_image = pygame.image.load("assets/star.png").convert_alpha()
        self.star_image = pygame.transform.scale(self.star_image, (20, 20))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def grow(self):
        self.size += 1
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, screen, center_x, center_y):
        screen.blit(self.image, (center_x - self.size // 2, center_y - self.size // 2))
        for i in range(self.stars):
            screen.blit(self.star_image, (center_x - self.size // 2 + i * 25, center_y - self.size // 2 - 30))