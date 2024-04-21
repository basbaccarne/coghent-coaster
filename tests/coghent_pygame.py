"""
iterative build of the pygame
"""
import pygame                     # we use pygame to make the GUI
import evdev

# screen settings
WIN = pygame.display.set_mode((480, 480))  # a 480 x 480 window
# WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # for a full screen window
pygame.display.set_caption("CoGhent Coaster")   # define the caption of the window
FPS = 60  # set frames per second

# load initial assets
main_image = pygame.image.load('../data/init.jpg')


# function to handle the actual drawing (define manipulations)
def draw_window(rotation, pulse):
    WIN.fill((10, 10, 10))    # background color
    rotated_img = pygame.transform.rotate(main_image, rotation)  # define image
    WIN.blit(rotated_img, (0, 0))   # draw image
    pygame.draw.circle(WIN, (184, 85, 153), [250, 250], pulse + 150, pulse)  # draw circle
    pygame.display.update()  # update the display


# define what happens when the coaster is booting (define manipulations)
def boot_function(pulse):
    new_pulse = pulse + 1
    if new_pulse > 250:
        new_pulse = 1
    return new_pulse


# define what happens when spacebar is pressed (define manipulations)
def update_content(rotation, booting, loading):
    if booting:
        return rotation + 90
    elif loading:
        return rotation + 120
    else:
        return rotation + 180


# main game loop (define interactions)
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
                elif event.key == pygame.K_SPACE or event.key == 330:
                    booting = False
                    pulse = 1
                    rotation = update_content(rotation, booting, loading)

        # draw new graphics
        draw_window(rotation, pulse)

    # close when the while loop is escaped
    pygame.quit()


# run the game
main()
