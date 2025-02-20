#import and initialise pygame modules
import sys, pygame
pygame.init()

size = width, height = 640, 480     #size of screen
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)

ball = pygame.image.load("intro_ball.gif")
ball_rect = ball.get_rect()


# Set up the clock for frame rate control
clock = pygame.time.Clock()


while True:
    #EXIT CONDITION CHECK
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #GAME LOGIC - move ball. Reverse direction if edge of screen passed
    ball_rect = ball_rect.move(speed)
    if ball_rect.left < 0 or ball_rect.right > width:       #if ball has hit left/right side of screen
        speed[0] = -speed[0]
    if ball_rect.top < 0 or ball_rect.bottom > height:          #if ball has hit top/bottom of screen. Remember, (0,0) is the top left
        speed[1] = -speed[1]

    #DRAW SCREEN
    screen.fill(black)          #clear screen
    screen.blit(ball, ball_rect)        #draw the ball image at the location of ball_rect, which I applied the movement logic to
    pygame.display.flip()               #display screen. .flip() exists to stop the user seeing all the items above being drawn sequentially


    # Limit the frame rate to 60 FPS
    clock.tick(60)