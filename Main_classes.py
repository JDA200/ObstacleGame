import pygame
from Generic_classes import Settings

class Enemy:
    def __init__(self, image, pos, speed):
        self.image = pygame.image.load(image)
        self.pos = self.image.get_rect().move(pos)
        self.speed = speed  #list - vector to define 2D movement
        self.settings = Settings()  #to scale movement to screen size


    def move(self): #basic linear movement
        self.pos = self.pos.move(self.speed)
        if self.pos.bottom > self.settings.screen_height or self.pos.top < 0:
            self.speed[1] = -self.speed[1]
        if self.pos.right > self.settings.screen_width or self.pos.left < 0:
            self.speed[0] = -self.speed[0]



class Player:
    def __init__(self, image, pos, speed):
        self.image = pygame.image.load(image)
        self.pos = self.image.get_rect().move(pos)
        self.speed = speed  #list - vector to define 2D movement
        self.inventory = {}
        self.lives = 3
        self.settings = Settings()

    def move(self, keys):
        # Handle key events to move the player
        if keys[pygame.K_LEFT] and self.pos.left > 0:
            self.pos.x -= self.speed[0]  # Move left
        if keys[pygame.K_RIGHT] and self.pos.right < self.settings.screen_width:
            self.pos.x += self.speed[0]  # Move right
        if keys[pygame.K_UP] and self.pos.top > 0:
            self.pos.y -= self.speed[1]  # Move up
        if keys[pygame.K_DOWN] and self.pos.bottom < self.settings.screen_height:
            self.pos.y += self.speed[1]  # Move down

    def add_to_inventory(self, item):
        if item.name in self.inventory:
            self.inventory[item.name]["count"] += 1  # Stack identical items
        else:
            self.inventory[item.name] = {"item": item, "count": 1}  # Store instance & count


class Item:
    def __init__(self, name, image, pos, value, weight):
        self.name = name
        self.image = pygame.image.load(image)
        self.value = value
        self.weight = weight
        self.pos = self.image.get_rect().move(pos)
        self.active = True
        self.settings = Settings()

    def picked_up(self):
        return self





