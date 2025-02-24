import pygame, random
from Generic_classes import Settings, SFX
from Main_classes import Enemy, Player, Item

class EnemySpawner:
    def __init__(self):
        self.settings = Settings()
        self.benchmark_time = 0     # For comparison

    def spawn_enemies(self, number_of_enemies, rescale_dims=None):
        new_enemies = []        #Note, this can't be an instance property, as it'll grow on every call. Needs to be reset on every method call as so
        for enemy_creation_index in range(number_of_enemies):
            enemy = Enemy('greyball.png',
                          ((self.settings.screen_width) / 2,
                           (self.settings.screen_height) / 2),
                          speed=[random.randint(-3, 3), random.randint(-3, 3)],
                          rescale_dims=rescale_dims)
            new_enemies += [enemy]
        return new_enemies

    def spawn_reinforcement_enemies(self, refresh_time_millis, number_of_current_enemies, number_of_new_enemies, max_enemies, rescale_dims=None):
        current_time = pygame.time.get_ticks()
        if (current_time - self.benchmark_time) > refresh_time_millis and number_of_current_enemies < (max_enemies - number_of_new_enemies):
            self.benchmark_time = current_time
            return self.spawn_enemies(number_of_new_enemies, rescale_dims)
        else:
            return []

class ItemSpawner:
    def __init__(self):
        self.settings = Settings()

    def spawn_items(self, number_of_items):
        items = []
        for item_creation_index in range(number_of_items):
            item = Item('Beach Ball',
                         'Intro_ball.gif',
                        ((self.settings.screen_width / number_of_items) * random.randint(0, number_of_items-1),
                         (self.settings.screen_height / number_of_items) * random.randint(0, number_of_items-1)),
                         100,
                         10)
            items += [item]
        return items