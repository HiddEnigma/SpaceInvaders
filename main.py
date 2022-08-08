from player import Player
from enemy import Enemy, Mother
from bullet import Bullet
from random import choice, randint

import obstacle
import pygame
import sys

# Constants
ENEMY_COLOURS = ["red", "yellow", "green"]
ENEMY_TIMER = pygame.USEREVENT + 1

MOTHER_SPAWNING_ORIGIN = ["left", "right"]


# This class will contain the sprite sheets and the utility that governs them.
def quit_game():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self):
        # Initializes the player object and player sprite
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Initializes the player lives mechanic, as well as the score.
        self.player_health = 3
        self.player_health_surface = pygame.image.load("sprites/player.png").convert_alpha()
        self.health_x_starting_position = screen_width - (self.player_health_surface.get_size()[0] * 2 + 20)

        self.score = 0
        self.score_font = pygame.font.Font("font/Pixeled.ttf", 20)

        # Initializes the obstacle objects and their sprites
        self.obstacles = pygame.sprite.Group()

        self.shape = obstacle.obstacle_shape
        self.obstacle_size = 6
        self.amount_of_obstacles = 4
        self.x_position_of_obstacles = [number * (screen_width / self.amount_of_obstacles)
                                        for number in range(self.amount_of_obstacles)]

        self.create_obstacles(*self.x_position_of_obstacles, starting_x=screen_width / 14, starting_y=480)

        # Initializes the Enemy objects, their sprites and their mechanics.
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.enemy_wave = 0
        self.enemy_vector = 1
        self.enemy_offset_y = 6

        # Initializes the Mother objects and their sprites
        self.mother = pygame.sprite.GroupSingle()
        self.mother_spawning_time = randint(400, 800)

        # Initializes the audio for the game
        self.game_music = pygame.mixer.Sound("audio/music.wav")
        self.explosion_sound = pygame.mixer.Sound("audio/explosion.wav")
        self.bullet_sound = pygame.mixer.Sound("audio/bullet.wav")

        self.game_music.set_volume(0.1)
        self.explosion_sound.set_volume(0.1)
        self.bullet_sound.set_volume(0.055)

        self.game_music.play(loops=-1)

    def create_obstacles(self, *offset, starting_x, starting_y):
        for x_offset in offset:
            for row_index, row in enumerate(self.shape):
                for column_index, column in enumerate(row):
                    if column == "x":
                        x = starting_x + column_index * self.obstacle_size + x_offset
                        y = starting_y + row_index * self.obstacle_size
                        block = obstacle.Obstacle(self.obstacle_size, (241, 79, 80), x, y)

                        self.obstacles.add(block)

    def enemy_factory(self, rows, columns, distance_x=60, distance_y=48, offset_x=65, offset_y=60):
        for row_index, row in enumerate(range(rows)):
            for column_index, column in enumerate(range(columns)):
                x = column_index * distance_x + offset_x
                y = row_index * distance_y + offset_y
                enemy_sprite = Enemy(ENEMY_COLOURS[row_index % 3], x, y)
                self.enemies.add(enemy_sprite)

    def enemy_wave_engine(self):
        if not self.enemies:
            self.enemy_factory(rows=6, columns=8, offset_y=60 + (self.enemy_wave * 5))

            self.enemy_wave += 1

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
            self.bullet_sound.play()

    def mother_timer(self):
        self.mother_spawning_time -= 1

        if self.mother_spawning_time <= 0:
            print("Mother should be spawning.")
            self.mother_spawning_time = randint(400, 800)

            self.mother.add(Mother(spawning_corner=choice(MOTHER_SPAWNING_ORIGIN), screen_width=screen_width))

    def check_collision(self):
        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:
                if pygame.sprite.spritecollide(bullet, self.obstacles, True):
                    bullet.kill()

                enemies_hit = pygame.sprite.spritecollide(bullet, self.enemies, True)
                if enemies_hit:
                    for enemy in enemies_hit:
                        bullet.kill()
                        self.explosion_sound.play()
                        self.score += enemy.value

                mother_hit = pygame.sprite.spritecollide(bullet, self.mother, True)
                if mother_hit:
                    for mother in mother_hit:
                        bullet.kill()
                        self.explosion_sound.play()
                        self.score += mother.value

        if self.enemy_bullets:
            for bullet in self.enemy_bullets:
                if pygame.sprite.spritecollide(bullet, self.obstacles, True):
                    bullet.kill()

                elif pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    self.player_health -= 1

        if self.enemies:
            for enemy in self.enemies:
                if pygame.sprite.spritecollide(enemy, self.obstacles, True):
                    enemy.kill()
                    self.explosion_sound.play()

                if pygame.sprite.spritecollide(enemy, self.player, True):
                    enemy.kill()
                    self.explosion_sound.play()
                    quit_game()

    def display_health(self):
        for heart in range(self.player_health - 1):
            x = self.health_x_starting_position + (heart * (self.player_health_surface.get_size()[0] + 10))

            screen.blit(self.player_health_surface, (x, 8))


    def display_score(self):
        score = self.score_font.render(str(self.score), False, (235, 235, 235))

        screen.blit(score, (10, -5))

    def display_defeat(self):
        defeat_surface = self.score_font.render("You fought valiantly. Better luck next time...", False, "white")
        defeat_rectangle = defeat_surface.get_rect(center=(screen_width / 2, screen_height / 2))

        screen.blit(defeat_surface, defeat_rectangle)

    def run(self):
        if self.player_health > 0:
            self.player.update()
            self.enemies.update(self.enemy_vector)
            self.enemy_bullets.update()
            self.mother.update()

            self.enemy_wave_engine()
            self.enemy_movement_engine()
            self.mother_timer()

            self.check_collision()
            self.display_health()
            self.display_score()

            self.player.sprite.bullets.draw(screen)

            self.player.draw(screen)
            self.obstacles.draw(screen)
            self.enemies.draw(screen)
            self.enemy_bullets.draw(screen)
            self.mother.draw(screen)
        else:
            self.display_defeat()


class CRT:
    def __init__(self):
        self.tv_styling = pygame.image.load("sprites/tv.png").convert_alpha()
        self.tv_styling = pygame.transform.scale(self.tv_styling, (screen_width, screen_height))

    def draw_crt_style(self):
        self.tv_styling.set_alpha(randint(60, 90))
        self.create_crt_style_lines()
        screen.blit(self.tv_styling, (0, 0))

    def create_crt_style_lines(self):
        line_height = 3
        number_of_lines = int(screen_height / line_height)

        for line in range(number_of_lines):
            y = line * line_height

            pygame.draw.line(self.tv_styling, "black", (0, y), (screen_width, y), 1)


def play():
    is_running = True

    game = Game()
    crt = CRT()

    # A simple timing mechanic for the enemy shooting.
    pygame.time.set_timer(ENEMY_TIMER, 500)

    while is_running:
        screen.fill((30, 30, 30))

        game.run()
        crt.draw_crt_style()
        pygame.display.flip()
        clock.tick(60)

        if game.player_health > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                if event.type == ENEMY_TIMER:
                    game.enemy_attack_engine()

        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.game_music.stop()
                        play()

                    if event.key == pygame.K_ESCAPE:
                        quit_game()


if __name__ == "__main__":
    # Initializes PyGame's engine
    pygame.init()

    # Game Variables
    screen_width = 600
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    play()
