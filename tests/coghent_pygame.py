"""
iterative build of the pygame
"""
import pygame                     # we use pygame to make the GUI
# import threading                # we use threading to run things on the background
# from src.fetcher import *       # we use our own script to fetch new images

# screen settings
WIN = pygame.display.set_mode((500, 500))  # a 500 x 500 window
# WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # for a full screen window
pygame.display.set_caption("CoGhent Coaster")   # define the caption of the window
FPS = 60  # set frames per second

# load initial assets
main_image = pygame.image.load('../data/init.jpg')


# function to handle the actual drawing
def draw_window(rotation, pulse):
    WIN.fill((10, 10, 10))    # background color
    rotated_img = pygame.transform.rotate(main_image, rotation)  # define image
    WIN.blit(rotated_img, (0, 0))   # draw image
    pygame.draw.circle(WIN, (184, 85, 153), [250, 250], pulse + 150, pulse)  # draw circle
    pygame.display.update()  # update the display


# define what happens when the coaster is booting
def boot_function(pulse):
    new_pulse = pulse + 1
    if new_pulse > 250:
        new_pulse = 1
    return new_pulse


# define what happens when spacebar is pressed
def update_content(rotation, booting, loading):
    if booting:
        return rotation + 90
    elif loading:
        return rotation + 120
    else:
        return rotation + 180


# main game loop
def main():
    clock = pygame.time.Clock()     # clock to maintain the FPS
    run = True

    # other settings
    rotation = 0
    pulse = 1
    booting = True
    loading = False

    while run:
        clock.tick(FPS)
        if booting:
            pulse = boot_function(pulse)
        # get a list of al the incoming events
        for event in pygame.event.get():
            # escape the loop and quit the game when window x is pressed
            if event.type == pygame.QUIT:
                run = False
            # when a button is pressed
            if event.type == pygame.KEYDOWN:
                # escape the loop and quit the game when it is the escape key
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_SPACE:
                    booting = False
                    pulse = 1
                    rotation = update_content(rotation, booting, loading)

        # draw new graphics
        draw_window(rotation, pulse)

    # close when the while loop is escaped
    pygame.quit()


# run the game
main()
