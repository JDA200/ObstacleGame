# imports
import pygame
import sys
import random
from Main_classes import Enemy, Player, Item
from Generic_classes import Settings, SFX, UIManager
from Spawner_classes import EnemySpawner, ItemSpawner
class Game:
    def __init__(self):
        self.running = True

    def run_game(self):
        # General parameters and init
        settings = Settings()
        sfx = SFX()
        UI = UIManager()
        screen_size = (settings.screen_width, settings.screen_height)
        screen = pygame.display.set_mode(screen_size)
        clock = pygame.time.Clock()

        # Player params and init
        player = Player(image='player_char.png',
                        pos=(0, 0),
                        speed=[5, 5])

        # Enemy and Item spawns
        enemy_spawner = EnemySpawner()
        enemies = enemy_spawner.spawn_enemies(10, rescale_dims=(40, 40))
        item_spawner = ItemSpawner()
        items = item_spawner.spawn_items(25)
        # gameplay loop
        while self.running == True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if user quits, exit
                    self.running = False
                    sys.exit()

            if player.lives <= 0:  # if player loses all lives
                UI.game_over(screen)
                self.running=False

            sfx.play_background_music()  # Play background music. Class ensures it will repeat if it ends

            keys = pygame.key.get_pressed()  # read user key press

            # Update Game
            player.move(keys)

            for enemy in enemies:
                enemy.move()
                if player.pos.colliderect(enemy.pos):
                    player.get_hit()
                    enemy.remove_on_death(enemies)
            # Reinforcement enemies
            enemies += enemy_spawner.spawn_reinforcement_enemies(refresh_time_millis=5000,
                                                                 # Returns none if time passed < refresh time
                                                                 number_of_current_enemies=len(enemies),
                                                                 number_of_new_enemies=4,
                                                                 max_enemies=30,
                                                                 rescale_dims=(20, 20))

            for item in items:
                if player.pos.colliderect(item.pos) and item.active:
                    player.add_to_inventory(item.picked_up())
                    item.active = False

            # Render screen (background surface, sprite blits, text etc.)
            screen.fill(settings.background_colour)  # background
            for item in items:
                if item.active:  # check item is active before drawing
                    screen.blit(item.image, item.pos)  # blit items
            for enemy in enemies:
                screen.blit(enemy.image, enemy.pos)  # blit enemies
            screen.blit(player.image, player.pos)  # blit player

            UI.display_inventory(player.inventory, screen)
            UI.display_lives(player.lives, screen)

            # show screen to user
            pygame.display.update()

            # clock tick
            clock.tick(settings.fps)

        sfx.stop_background_music()
        pygame.display.quit()

    def restart_game(self):
        # Reset any variables or states for a new game if necessary
        self.running = True  # Set running to True to restart the game
        self.run_game()  # Restart the game loop
