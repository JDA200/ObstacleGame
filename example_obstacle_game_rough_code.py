
import sys
import pygame
pygame.font.init()

#Create some objects to move in our game
class GameObject:
    def __init__(self, image, height, speed):
        self.image = image
        self.speed = speed
        self.pos = self.image.get_rect().move(0, height)  # Just use the image size directly

    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right > 1280:
            self.pos.left = 0

#create movabke player
class PlayerObject:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.pos = self.image.get_rect()
        self.pos.x = x  # Starting X position
        self.pos.y = y  # Starting Y position
        self.speed = speed  # Speed of movement (how many pixels per frame)
        self.score = 0


    def move(self, keys):
        # Handle key events to move the player
        if keys[pygame.K_LEFT]:
            self.pos.x -= self.speed  # Move left
        if keys[pygame.K_RIGHT]:
            self.pos.x += self.speed  # Move right
        if keys[pygame.K_UP]:
            self.pos.y -= self.speed  # Move up
        if keys[pygame.K_DOWN]:
            self.pos.y += self.speed  # Move down

        #check for hitting bottom of screen
        if p.pos.bottom > 960:
            self.score += 1
        if self.pos.right > 1280:
            self.pos.left = 0
        if self.pos.left < 0:
            self.pos.right = 1280
        if self.pos.bottom > 960:
            self.pos.top = 0

    def reset_pos(self):
        self.pos = self.image.get_rect()
        self.pos.x = 640
        self.pos.y = 0


screen = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock()
player = pygame.image.load('player_char.png')
player = pygame.transform.scale(player, (30, 60))  # Resize player to 100x100 pixels
obstacle = pygame.image.load('greyball.png')
font = pygame.font.SysFont("Arial", 30)         # Initialize font for rendering text (life counter)
objects = []
lives = 5
time_of_last_collision = 0

start_line = pygame.Rect(0, 69, 1280, 10)  # A horizontal line at the top with a width of 1280px and height of 10px


#create player
p = PlayerObject(player, 640, 0, 3)

#create obstacles
for x in range(11):
    o = GameObject(obstacle, (x+1)*80, x+1)
    objects.append(o)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if lives <= 0:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    screen.fill(settings.background_colour)  # Fill the screen with block color, i.e. background

    keys = pygame.key.get_pressed()     #get state of all keys pressed

    #move player
    p.move(keys)
    ###pygame.draw.rect(screen, (255, 0, 0), p.pos, 2)  # Draw a red outline of the rect
    screen.blit(p.image, p.pos)

    #move objects
    for o in objects:
        o.move()
        # Draw the rect (red outline) for debugging
        ###pygame.draw.rect(screen, (255, 0, 0), o.pos, 2)  # Draw a red outline of the rect

        #check for collision
        if p.pos.colliderect(o.pos):
            if pygame.time.get_ticks() - time_of_last_collision > 500:
                lives -= 1
                p.reset_pos()
            time_of_last_collision = pygame.time.get_ticks()

        screen.blit(o.image, o.pos)

    #draw start line
    pygame.draw.rect(screen, (180, 40, 40), start_line)  # Draw the start line (e.g., white color)

    # Render lives, score
    life_text = font.render(f"Lives: {lives}", True, (255, 255, 255))  # White text
    score_text = font.render(f"Score: {p.score}", True, (255, 255, 255))  # White text
    screen.blit(life_text, (10, 10))  # Change the position as needed
    screen.blit(score_text, (10, 50))  # Change the position as needed


    pygame.display.update()
    clock.tick(60)


