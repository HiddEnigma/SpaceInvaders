import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height):
        super().__init__()

        self.image = pygame.Surface((4, 20))

        self.image.fill("white")

        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.y_constraint = screen_height

    def update(self):
        self.rect.y += self.speed

        self.has_collided()

    def has_collided(self):
        if self.rect.top >= self.y_constraint or self.rect.bottom <= 0:
            self.kill()
            print("Bullet has been destroyed.")
        #
        # if self.rect.y <= -50 or self.rect.y >= self.y_constraint + 50:
        #     self.kill()
        #     print("Bullet has been destroyed.")