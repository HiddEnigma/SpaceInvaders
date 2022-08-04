import pygame
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, position, screen_width, player_speed):
        super().__init__()

        self.image = pygame.image.load("sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=position)

        self.speed = player_speed
        self.health = 3
        self.x_constraint = screen_width

        self.ready_to_shoot = True
        self.time_to_shoot = 0
        self.shooting_cooldown = 600

        self.bullets = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            # Checks if the player's X position is colliding against the right edge of the screen. If it is,
            # return.
            if self.rect.right >= self.x_constraint:
                return
            else:
                self.rect.x += self.speed

        elif keys[pygame.K_LEFT]:
            # Checks if the player's X position is colliding against the left edge of the screen. If it is,
            # return.
            if self.rect.left <= 0:
                return
            else:
                self.rect.x -= self.speed
        elif keys[pygame.K_SPACE] and self.ready_to_shoot:
            self.shoot()

    def shoot(self):
        self.ready_to_shoot = False
        self.time_to_shoot = pygame.time.get_ticks()

        self.bullets.add(Bullet(self.rect.center, -8, self.rect.bottom))

    def reload(self):
        if not self.ready_to_shoot:
            current_time = pygame.time.get_ticks()

            if (current_time - self.time_to_shoot) >= self.shooting_cooldown:
                self.ready_to_shoot = True

    def is_damaged(self):
        self.health -= 1

    def update(self):
        self.get_input()
        self.reload()
        self.bullets.update()