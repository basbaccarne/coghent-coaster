"""
iterative build of the pygame
"""
import pygame  # we use pygame to make the GUI

# game screen settings
WIN = pygame.display.set_mode((500, 500))  # a 500 x 500 window
# WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # for a full screen window
pygame.display.set_caption("CoGhent Coaster")   # define the caption of the window
FPS = 60  # set frames per second

# load initial assets
main_image = pygame.image.load('data/init.jpg')


# function to handle the actual drawing (define manipulations)
def draw_window(border, size, image=main_image):
    WIN.fill((10, 10, 10))    # set the background color
    WIN.blit(image, (0, 0))   # draw the image
    pygame.draw.circle(WIN, (184, 85, 153), [250, 250], size, border)  # draw a circle (animated size & border)
    pygame.display.update()  # update the display


# define what happens when the coaster is booting (define pulse manipulations)
def boot_function(pulse):
    new_pulse = pulse + 1
    if new_pulse > 250:
        new_pulse = 1
    return new_pulse


# define starting index for the images
show_index = 0


# define what happens when spacebar is pressed (define manipulations)
def update_content():
    global show_index
    show_index = (show_index + 1) % 3   # increase the show index
    return pygame.image.load(f'data/image{show_index+1}.jpg') # give back the path of the image


# main game loop (define interactions)
def main(image):
    clock = pygame.time.Clock()     # clock to maintain the FPS
    run = True

    # other settings
    border = 1
    booting = True

    while run:
        clock.tick(FPS)

        # animation while booting
        if booting:
            border = boot_function(border)
            size = border+150

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
                    border = 0
                    size = 0
                    image = update_content()

        # draw new graphics
        draw_window(border, size, image)

    # close when the while loop is escaped
    pygame.quit()


# run the game
main(main_image)
