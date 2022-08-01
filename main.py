from player import Player
import pygame
import sys


# This class will contain the sprite sheets and the utility that governs them.
class Game:
    def __init__(self):
        player_sprite = Player((screen_width / 2, screen_height), screen_width, screen_height, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

    def run(self):
        self.player.update()
        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)


if __name__ == "__main__":
    # Initializes PyGame's engine
    pygame.init()

    # Game Variables
    screen_width = 600
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

                sys.exit()

        screen.fill((30, 30, 30))

        game.run()

        pygame.display.flip()
        clock.tick(60)
