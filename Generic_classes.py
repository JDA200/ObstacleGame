import pygame
import time

pygame.font.init()


class Settings:
    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 1000
        self.fps = 60
        self.background_colour = (100, 100, 120)
        self.background_music = "514508__gis_sweden__background-techno-loop131bpm.wav"
        self.inventory_text = {"header_font": pygame.font.SysFont("Verdana", 40),
                               "body_font": pygame.font.SysFont("Verdana", 20),
                               "colour": (255, 255, 255)}
        self.lives_text = {"header_font": pygame.font.SysFont("Verdana", 40),
                           "body_font": pygame.font.SysFont("Verdana", 20),
                           "colour": (255, 255, 255)}
        self.game_over_text = {"header_text" : "Game Over!",
                               "header_font": pygame.font.SysFont("palatino", 100),
                               "header_text_colour": (200, 50, 50),
                               "body_text": "Better Luck Next Time!",
                               "body_font": pygame.font.SysFont("Verdana", 40),
                               "body_text_colour": (200, 50, 50)}


class UIManager:
    "Responsible for creating and displaying lives, inventory etc. text." \
    "This removes UI clutter from the game loop"

    def __init__(self):
        self.settings = Settings()

    def display_inventory(self, inventory, screen):
        "method to display inventory to screen" \
        "inventory arg should be passed from Player class. See Player for datatype" \
        "screen arg should be main game screen"
        inventory_header_text = self.settings.inventory_text['header_font'].render(f"Inventory",   #surface (text) to blit
                                                                            True,   # anti-aliasing
                                                                            (255, 255, 255))    # surface (text) colouring
        screen.blit(inventory_header_text, (0, 0))
        for index, item in enumerate(inventory.items()):  # print player inventory to screen
            screen.blit(
                self.settings.inventory_text['body_font'].render(f"{item[0]}: {item[1]['count']}",  # surface (text) to blit
                                                            True,  # Anti-aliasing
                                                            self.settings.inventory_text['colour']), # surface (text) colouring
                                                            (0, (inventory_header_text.get_height() + index * 20)))  # position to blit to

    def display_lives(self, lives, screen):
        "method to display lives to screen" \
        "lives arg should be passed from Player class. See Player for datatype" \
        "screen arg should be main game screen"
        lives_header_text = self.settings.lives_text['header_font'].render(f"Lives: {lives}",
                                                                    True,
                                                                    (255, 255, 255))
        text_width = lives_header_text.get_width()
        text_position = ((0.9 * self.settings.screen_width - text_width), 0)
        screen.blit(lives_header_text, text_position)   #print Lives to RHS of screen

    def game_over(self, screen):
        game_over_text = self.settings.game_over_text["header_font"].render(self.settings.game_over_text["header_text"],
                                                                            True,
                                                                            self.settings.game_over_text["header_text_colour"])
        game_over_text_width = game_over_text.get_width()
        game_over_text_height = game_over_text.get_height()
        game_over_text_position = ((self.settings.screen_width - game_over_text_width) / 2, (self.settings.screen_height - game_over_text_height) / 2)
        screen.blit(game_over_text, game_over_text_position)
        pygame.display.update()
        pygame.time.wait(3000)


class SFX:
    def __init__(self):
        self.is_playing = False
        self.sound_cooldown = 0.1  # cooldown to ensure sounds don't play every frame on collision
        self.last_play_time = 0  # init last_play_time for use in sound cooldown
        self.settings = Settings()
        pygame.mixer.init()

    def play_sound(self, sound_file):
        """Play sound"""
        current_time = time.time()
        if current_time - self.last_play_time > self.sound_cooldown:
            sound = pygame.mixer.Sound(sound_file)
            self.last_play_time = current_time
            return sound.play()

    def play_background_music(self):
        """Check if the music is finished and restart if necessary."""
        if not self.is_playing:
            self.is_playing = True
            pygame.mixer.music.load(self.settings.background_music)
            pygame.mixer.music.play(-1)  # -1 arg means play indefinitely

    def stop_background_music(self):
        """Stop the background music."""
        pygame.mixer.music.stop()
        self.is_playing = False
