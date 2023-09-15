# This script accesses the CoGhent API to fetch and show a random image
# (API documentation: https://coghent.github.io/)

############
# PACKAGES #
############

import os
# To use SPARQL we need the SPARQLWrapper package
from SPARQLWrapper import SPARQLWrapper, JSON
# To get JSON data from a URL we need the requests package
import requests
# To work with IIIF images we need the Pillow package and the io package
from PIL import Image
from io import BytesIO
# To make full screen interactive experiences, PyGame is a nice package
import pygame
# To run things on the background of the PyGame we use the threading package
import threading

#############
#  SETTINGS #
#############

# SPARQL datasource url
sparql = SPARQLWrapper("https://stad.gent/sparql")

# Set the SPARQL query to fetch one random IIIF manifest from the CoGhent event streams
# (Test SPARQL queries at http://query.linkeddatafragments.org/)
sparql.setQuery("""
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    SELECT ?o WHERE {
        ?s cidoc:P129i_is_subject_of ?o .
        BIND(RAND() AS ?random) .
    } ORDER BY ?random
    LIMIT 1
""")

###########################
# DEFINE THE DATA FETCHER #
###########################
def dataFetcher():
    print(f"Getting a random manifest ....")

    # Get the data and convert the results to a JSON format
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    uri = None
    object = None

    # If the response has content, store the URI of the manifest
    if 'results' in response and 'bindings' in response['results']:
        bindings = response['results']['bindings']

        if len(bindings) > 0:
            first_result = bindings[0]
            uri = first_result['o']['value']
            print(f"--> the random URI is: {uri}")
        else:
            print("No results found.")
            object = None
    else:
        print("Invalid or empty response.")
        object = None

    print(f"--> Fetching data from the manifest ....")

    # Fetch the data
    uri_response = requests.get(uri)

    # Process the incoming signal
    data = None
    if uri_response.status_code == 200:
        data = uri_response.json()
    else:
        print(f"--> Failed to fetch data. Status code: {uri_response.status_code}")
        object = None
    if uri_response.status_code == 403:
        print(f"--> We ran into auth issues")
        object = None

    # If there is data, get the values from the jason data
    if uri_response.status_code == 200:
        name = data['label'] ['@value']
        print(f"-----> the name of the object is: {name}")

        attribution = data['sequences'] [0] ['canvases'] [0] ['images'] [0] ['attribution']
        print(f"-----> the attribution is: {attribution}")

        img_url = data['sequences'] [0] ['canvases'] [0] ['images'] [0] ['resource'] ['@id']
        print(f"-----> the image url is is: {img_url}")

        # store the result in a dictionary
        object = {'name': name, 'attribution': attribution, 'img_url': img_url}

    return object

#########################################
# DEFINE THE DOWNLOAD AND SHOW FUNCTION #
#########################################
def imgFetcher(object, toggle, action='show'):

    print(f"--> Getting the image: {object['name']}")

    # rescale
    base_url, shape, resolution, rotation, format =  (object['img_url'].rsplit("/", 4))
    new_shape = 'square'
    new_resolution = '!500,500'
    new_rotation = 0
    rescaled_url = f"{base_url}/{new_shape}/{new_resolution}/{new_rotation}/{format}"
    print(f"-----> the rescaled url is: {rescaled_url}")

    # Send a GET request to the IIIF URL
    img_response = requests.get(rescaled_url)

    # Check if the request was successful (status code 200)
    if img_response.status_code == 200:

        if action=='show':
            # Open the image from the response content
            image = Image.open(BytesIO(img_response.content))
            # Display the image
            image.show()

        if action=='download':
            filename = f"downloaded_image{toggle}.jpg"
            with open(f"data/{filename}", "wb") as file:
                file.write(img_response.content)
                print("----->  Image downloaded successfully.")
    else:
        print(f"----->  Request failed with status code: {img_response.status_code}")

###################
# TESTING 1, 2, 3 #
###################
# Get first image
object1 = dataFetcher()
if object1 != None:
    imgFetcher(object1, toggle = 1, action = 'download')
# Get second image
object2 = dataFetcher()
if object2 != None:
    if os.path.exists("data/downloaded_image1.jpg"): toggle = 2
    else: toggle = 1
    imgFetcher(object2, toggle, action = 'download')

#################
# SET-UP PYGAME #
#################
# check animations (cloud transitions): https://github.com/hoffstadt/DearPyGui/wiki/Dear-PyGui-Showcase

# Initialize pygame
pygame.init()

# Define screen dimensions (full-screen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Initialize pygame fonts (for text rendering)
pygame.font.init()

# Load the initial image and text
image1 = pygame.image.load("data/downloaded_image1.jpg")
image2 = pygame.image.load("data/downloaded_image2.jpg")
current_image = image1

font = pygame.font.Font(None, 36)
text1 = font.render("Text 1", True, (255, 255, 255))  # White text
text2 = font.render("Text 2", True, (255, 255, 255))  # White text
current_text = text1

# Get the image and text dimensions
image_rect = current_image.get_rect()
text_rect = current_text.get_rect()

# Center the text on the screen
text_rect.center = screen.get_rect().center

# Function to download an image in the background
def download_image():
    object = dataFetcher()
    imgFetcher(object, toggle = 1, action = 'download')
    return pygame.image.load("downloaded_image1.jpg")

# Function to switch to the second image and text
def switch_to_second_image():
    global current_image, current_text
    current_image = image2
    current_text = text2

# Main game loop
running = True
show_second_image = False

# Start a thread for downloading the second image
download_thread = threading.Thread(target=switch_to_second_image)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Toggle between the first and second image and text
                if not show_second_image:
                    show_second_image = True
                    if not download_thread.is_alive():
                        download_thread.start()

    # Clear the screen
    screen.fill((0, 0, 0))  # Fill with black

    # Draw the current image
    screen.blit(current_image, image_rect)

    # Draw the current text
    screen.blit(current_text, text_rect)

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
