import pygame
from Generic_classes import Settings, SFX


class Sprite:
    def __init__(self, image, pos, speed, rescale_dims=(50, 50)):
        "rescale_dims should be a tuple of (width, height), otherwise None"
        self.settings = Settings()
        self.image = pygame.image.load(image)
        self.pos = self.image.get_rect().move(pos)
        if speed[0] >= 0:
            self.orientation = 'R'
        else:
            self.orientation = 'L'
            self.flip_x()
        self.rescale_dims = rescale_dims  # Set it up here
        if self.rescale_dims:  # If it's not None, call rescale
            self.rescale(self.rescale_dims)

    def flip_x(self):
        self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def rescale(self, dims):
        self.image = pygame.transform.scale(self.image, dims)
        self.pos = self.image.get_rect().move(self.pos[0], self.pos[1])  # Set position based on image


class Enemy(Sprite):
    def __init__(self, image, pos, speed, rescale_dims=None):
        if rescale_dims is None:
            rescale_dims = (50, 50)  # Default if not passed
        super().__init__(image, pos, speed, rescale_dims)
        self.speed = speed  #list - vector to define 2D movement

    def move(self): # Basic linear movement
        self.pos = self.pos.move(self.speed)
        if self.pos.bottom > self.settings.screen_height or self.pos.top < 0:
            self.speed[1] = -self.speed[1]
        if self.pos.right > self.settings.screen_width or self.pos.left < 0:
            self.speed[0] = -self.speed[0]
            self.flip_x()

    def remove_on_death(self, enemy_group):
        enemy_group.remove(self)

    def flip_x(self):
        self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)


class Player(Sprite):
    def __init__(self, image, pos, speed):
        super().__init__(image, pos, speed, rescale_dims=None)
        self.rescale_dims = (self.settings.screen_width / 24, self.settings.screen_height / 10)
        self.rescale(self.rescale_dims)
        self.speed = speed  #list - vector to define 2D movement
        self.inventory = {}
        self.lives = 3
        self.sfx = SFX()

    def move(self, keys):
        # Handle key events to move the player
        if keys[pygame.K_LEFT] and self.pos.left > 0:
            self.pos.x -= self.speed[0]  # Move left
            if self.orientation == 'R':
                self.flip_x()
            self.orientation = 'L'
        if keys[pygame.K_RIGHT] and self.pos.right < self.settings.screen_width:
            self.pos.x += self.speed[0]  # Move right
            if self.orientation == 'L':
                self.flip_x()
            self.orientation = 'R'
        if keys[pygame.K_UP] and self.pos.top > 0:
            self.pos.y -= self.speed[1]  # Move up
        if keys[pygame.K_DOWN] and self.pos.bottom < self.settings.screen_height:
            self.pos.y += self.speed[1]  # Move down

    def add_to_inventory(self, item):
        if item.name in self.inventory:
            self.inventory[item.name]["count"] += 1  # Stack identical items
        else:
            self.inventory[item.name] = {"item": item, "count": 1}  # Store instance & count

    def get_hit(self):
        if self.lives > 0:
            self.lives -= 1
            self.sfx.play_sound("582265__rocketpancake__justa-slap-smack.wav")


class Item:
    def __init__(self, name, image, pos, value, weight):
        self.name = name
        self.image = pygame.image.load(image)
        self.value = value
        self.weight = weight
        self.pos = self.image.get_rect().move(pos)
        self.active = True
        self.settings = Settings()
        self.sfx = SFX()

    def picked_up(self):
        self.sfx.play_sound("733018__geoff-bremner-audio__whip-3.wav")
        return self





