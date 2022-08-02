import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        super(Enemy, self).__init__()

        self.file_path = "sprites/" + colour + ".png"
        self.image = pygame.image.load(self.file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, vector):
        self.rect.x += vector