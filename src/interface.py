"""
iterative build of the pygame
"""
import pygame  # we use pygame to make the GUI
import json    # to read the metadata

pygame.init()
# game screen settings
WIN = pygame.display.set_mode((500, 500))  # a 500 x 500 window
# WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # for a full screen window
screen_rect = WIN.get_rect()
pygame.display.set_caption("CoGhent Coaster")   # define the caption of the window

FPS = 60  # set frames per second
font = pygame.font.Font('src/basetica-medium.otf', 20)

# load initial img assets
image = 'data/init.jpg'

# load text assets
description = ''
desc_text = font.render(description, True, (0, 0, 0))
desc_rect = desc_text.get_rect(left=screen_rect.right)


# function to handle the actual drawing (define manipulations)
def draw_window(border, size, new_desc_rect, new_image=image, new_text='', ):
    # set the background color
    WIN.fill((10, 10, 10))

    # update the image
    new_image = pygame.image.load(new_image)
    WIN.blit(new_image, (0, 0))

    # update the text
    if new_text != '':
        pygame.draw.rect(WIN, (220, 220, 220), pygame.Rect(0, 6, 500, 49))
        pygame.draw.rect(WIN, (192, 192, 192), pygame.Rect(0, 6, 500, 46))
        pygame.draw.rect(WIN, (169, 169, 169), pygame.Rect(0, 6, 500, 43))
        pygame.draw.rect(WIN, (253, 194, 11), pygame.Rect(0, 6, 500, 40))
    text = font.render(new_text, True, (0, 0, 0))
    WIN.blit(text, new_desc_rect)

    # loading animation for the booting process
    pygame.draw.circle(WIN, (184, 85, 153), [250, 250], size, border)

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
    # increase the show index
    global show_index
    show_index = (show_index + 1) % 5

    # get the metadata
    with open(f'data/image{show_index+1}.json', 'r') as json_file:
        meta_data = json.load(json_file)

    # store image url, name and source in a dictionary
    new_data = {'img': f'data/image{show_index+1}.jpg',
                'name': meta_data['name'],
                'source': meta_data['attribution']}
    return new_data


# main game loop (define interactions)
def main(boot_image):
    clock = pygame.time.Clock()     # clock to maintain the FPS
    run = True

    # other settings
    border = 1
    size = border + 150
    booting = True
    text = ''
    updated_image = boot_image

    while run:
        clock.tick(FPS)

        # animation while booting
        if booting:
            border = boot_function(border)
            size = border+150

        # vertical text scrolling
        desc_rect.y = 16
        desc_rect.x -= 1
        if desc_rect.right <= 0-500:  # if leave on left side
            desc_rect.x = screen_rect.right  # then move to right side

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
                    update = update_content()
                    updated_image = update['img']
                    text = f"{update['name']} ({update['source']})"
                    desc_rect.x = screen_rect.right
        # draw new graphics
        draw_window(border, size, new_desc_rect=desc_rect, new_image=updated_image, new_text=text)

    # close when the while loop is escaped
    pygame.quit()


# run the game
main(image)
