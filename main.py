#imports
import pygame
import sys
from Main_classes import Enemy, Player, Item
from Generic_classes import Settings
pygame.font.init()




#General parameters and init
settings = Settings()
screen_size = (settings.screen_width, settings.screen_height)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)         # Initialize font for rendering text (life counter)


#Obstacle and player params and init
player = Player('player_char.png',
                (0, 0),
                [3, 3])

e1 = Enemy('greyball.png',
           ((settings.screen_width) / 2,
            (settings.screen_height) / 2),
           [3, 2])

item1 = Item('example_item',
             'Intro_ball.gif',
             (settings.screen_width / 4,
             settings.screen_height / 4),
             100,
             10)

#gameplay loop
while True:
    #Handle events
    for event in pygame.event.get():        #if user quits, exit
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    keys = pygame.key.get_pressed() #read user key press


    #Update Game
    e1.move()
    player.move(keys)
    if player.pos.colliderect(e1.pos):
        player.lives -= 1
    elif player.pos.colliderect(item1.pos) and item1.active:
        player.add_to_inventory(item1.picked_up())
        item1.active = False



    #Render screen (background surface, sprite blits, text etc.)
    inventory_header_text = font.render(f"Inventory", True, (255, 255, 255))

    screen.fill((50, 50, 50))    #background
    screen.blit(e1.image, e1.pos)   #blit enemy
    if item1.active:    #check item is actually in the world before drawing
        screen.blit(item1.image, item1.pos)
    screen.blit(player.image, player.pos)   #blit player

    screen.blit(inventory_header_text, (0, 0))
    for index, item in enumerate(player.inventory.items()):    #print player inventory to screen
        screen.blit(font.render(f"{item[0]}: {item[1]['count']}", True, (255, 255, 255)), (0, (index+1)*20))

    #show screen to user
    pygame.display.update()

    #clock tick
    clock.tick(settings.fps)
