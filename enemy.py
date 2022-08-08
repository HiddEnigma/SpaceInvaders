import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        super(Enemy, self).__init__()

        self.file_path = "sprites/" + colour + ".png"
        self.image = pygame.image.load(self.file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if colour == "red":
            self.value = 10
        elif colour == "green":
            self.value = 20
        elif colour == "yellow":
            self.value = 30

    def update(self, vector):
        self.rect.x += vector


class Mother(pygame.sprite.Sprite):
    def __init__(self, spawning_corner, screen_width):
        super(Mother, self).__init__()

        self.image = pygame.image.load("sprites/mother.png").convert_alpha()

        if spawning_corner == "right":
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.value = 100

        self.rect = self.image.get_rect(topleft=(x, 40))

    def update(self):
        self.rect.x += self.speed
