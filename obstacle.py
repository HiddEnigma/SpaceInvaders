import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, size, colour,x, y):
        super(Obstacle, self).__init__()

        self.image = pygame.Surface((size, size))

        self.image.fill(colour)

        self.rect = self.image.get_rect(topleft=(x, y))


obstacle_shape = [
    "  xxxxxxx",
    " xxxxxxxxx",
    "xxxxxxxxxxx",
    "xxxxxxxxxxx",
    "xxxxxxxxxxx",
    "xxx     xxx",
    "xx       xx"
]
