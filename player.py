import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.image = pygame.image.load("../sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=position)