from player import Player
from enemy import Enemy
from bullet import Bullet
from random import choice

import obstacle
import pygame
import sys

# Constants
ENEMY_COLOURS = ["red", "yellow", "green"]
ENEMY_TIMER = pygame.USEREVENT + 1

# This class will contain the sprite sheets and the utility that governs them.
class Game:
    def __init__(self):
        # Initializes the player object and the player sprite
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Initializes the obstacle objects and their sprites
        self.obstacles = pygame.sprite.Group()

        self.shape = obstacle.obstacle_shape
        self.obstacle_size = 6
        self.amount_of_obstacles = 4
        self.x_position_of_obstacles = [number * (screen_width / self.amount_of_obstacles)
                                        for number in range(self.amount_of_obstacles)]

        self.create_obstacles(*self.x_position_of_obstacles, starting_x=screen_width / 14, starting_y=480)

        # Initializes the Enemy objects and their sprites
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.enemy_factory(rows=6, columns=8)
        self.enemy_vector = 1
        self.enemy_offset_y = 6

    def create_obstacles(self, *offset, starting_x, starting_y):
        for x_offset in offset:
            for row_index, row in enumerate(self.shape):
                for column_index, column in enumerate(row):
                    if column == "x":
                        x = starting_x + column_index * self.obstacle_size + x_offset
                        y = starting_y + row_index * self.obstacle_size
                        block = obstacle.Obstacle(self.obstacle_size, (241, 79, 80), x, y)

                        self.obstacles.add(block)

    def enemy_factory(self, rows, columns, distance_x=60, distance_y=48, offset_x=65, offset_y=10):
        for row_index, row in enumerate(range(rows)):
            for column_index, column in enumerate(range(columns)):
                x = column_index * distance_x + offset_x
                y = row_index * distance_y + offset_y
                enemy_sprite = Enemy(ENEMY_COLOURS[row_index % 3], x, y)
                self.enemies.add(enemy_sprite)

    def enemy_movement_engine(self):
        if self.enemies:
            for enemy in self.enemies.sprites():
                if enemy.rect.right >= screen_width or enemy.rect.left <= 0:
                    self.enemy_vector *= -1

                    self.enemy_move_further()

                    return

    def enemy_move_further(self):
        if self.enemies:
            for enemy in self.enemies.sprites():
                enemy.rect.y += self.enemy_offset_y

    def enemy_attack_engine(self):
        if self.enemies:
            enemy = choice(self.enemies.sprites())
            enemy_bullet = Bullet(enemy.rect.center, 6, screen_height)
            self.enemy_bullets.add(enemy_bullet)



    def run(self):
        self.player.update()
        self.enemies.update(self.enemy_vector)
        self.enemy_movement_engine()
        self.enemy_bullets.update()

        self.player.sprite.bullets.draw(screen)
        self.enemies.sprites

        self.player.draw(screen)
        self.obstacles.draw(screen)
        self.enemies.draw(screen)
        self.enemy_bullets.draw(screen)


if __name__ == "__main__":
    # Initializes PyGame's engine
    pygame.init()

    # Game Variables
    screen_width = 600
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    # A simple timing mechanic for the enemy shooting.
    pygame.time.set_timer(ENEMY_TIMER, 500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

                sys.exit()
            if event.type == ENEMY_TIMER:
                game.enemy_attack_engine()

        screen.fill((30, 30, 30))

        game.run()

        pygame.display.flip()
        clock.tick(60)
