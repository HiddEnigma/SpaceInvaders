from player import Player
import obstacle
import pygame
import sys


# This class will contain the sprite sheets and the utility that governs them.
class Game:
    def __init__(self):
        # Initializes the player object and the player sprite
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Initializes the obstacle objects and their sprites
        self.shape = obstacle.obstacle_shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.amount_of_obstacles = 4
        self.x_position_of_obstacles = [number * (screen_width / self.amount_of_obstacles)
                                        for number in range(self.amount_of_obstacles)]

        self.create_obstacles(*self.x_position_of_obstacles, starting_x=screen_width / 14, starting_y=480)

    def create_obstacle(self, starting_x, starting_y, x_offset):
        for row_index, row in enumerate(self.shape):
            for column_index, column in enumerate(row):
                if column == "x":
                    x = starting_x + column_index * self.block_size + x_offset
                    y = starting_y + row_index * self.block_size
                    block = obstacle.Obstacle(self.block_size, (241, 79, 80), x, y)

                    self.blocks.add(block)

    def create_obstacles(self, *offset, starting_x, starting_y):
        for x_offset in offset:
            self.create_obstacle(starting_x, starting_y, x_offset)

    def run(self):
        self.player.update()
        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)

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
