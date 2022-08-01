from game import Game
import pygame
import sys


if __name__ == "__main__":
    # Initializes PyGame's engine
    pygame.init()

    # Game Variables
    screen_width = 800
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