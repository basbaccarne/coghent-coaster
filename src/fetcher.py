"""
This module accesses the CoGhent API to fetch and download (or show) a random image
(API documentation: https://coghent.github.io/)

It defines two functions:

* data_fetcher():
    returns a random collection object as a dictionary with the following variables:
        - 'name': the title of the object
        - 'attribution': the institute it belongs to
        - 'img_url': the IIIF url (full quality) of the object
        - If the fetch failed, the function returns [None]

* img_fetcher(my_object, counter, action):
    needs the following arguments
        - 'my_object': the [dictionary] response of data_fetcher (needs 'name' and 'img_url')
        - 'counter': adds a [integer] to the filename of the downloaded image
        - 'action': character variable that can be 'show' (display result directly) or 'download' (store file)
    returns nothing but:
        - if the action is 'show': [displays] the image
        - if the action is 'download': [download] the file in the data folder as image{counter}.jpg
"""
############
# PACKAGES #
############

# To use SPARQL we need the SPARQLWrapper package
from SPARQLWrapper import SPARQLWrapper, JSON
# To get JSON data from a URL we need the requests package
import requests
# To work with IIIF images we need the Pillow package and the io package
from PIL import Image
from io import BytesIO
import json
import keyboard

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

session = requests.Session()
headers = {'User-Agent': 'CoGhent Coaster App/1.0', 'Accept-Encoding': 'gzip, deflate'}

###########################
# DEFINE THE DATA FETCHER #
###########################


def data_fetcher():
    # print(f"Getting a random manifest ....")

    # Get the data and convert the results to a JSON format
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    uri = None
    my_object = None

    # If the response has content, store the URI of the manifest
    if 'results' in response and 'bindings' in response['results']:
        bindings = response['results']['bindings']

        if len(bindings) > 0:
            first_result = bindings[0]
            uri = first_result['o']['value']
            # print(f"--> the random URI is: {uri}")
        else:
            print("No results found.")
            my_object = None
    else:
        print("Invalid or empty response.")
        my_object = None

    # print(f"--> Fetching data from the manifest ....")

    # Fetch the data
    try:
        uri_response = session.get(uri, headers=headers, timeout=(1, 3))
        # Process the incoming signal
        data = None
        if uri_response.status_code == 200:
            data = uri_response.json()
        else:
            # print(f"--> Failed to fetch data. Status code: {uri_response.status_code}")
            my_object = None
        if uri_response.status_code == 403:
            # print(f"--> We ran into auth issues")
            my_object = None

        # If there is data, get the values from the jason data
        if uri_response.status_code == 200:
            name = data['label']['@value']
            # print(f"-----> the name of the object is: {name}")

            attribution = data['sequences'][0]['canvases'][0]['images'][0]['attribution']
            # print(f"-----> the attribution is: {attribution}")

            img_url = data['sequences'][0]['canvases'][0]['images'][0]['resource']['@id']
            # print(f"-----> the image url is is: {img_url}")

            # store the result in a dictionary
            my_object = {'name': name, 'attribution': attribution, 'img_url': img_url}

    except requests.exceptions.Timeout:
        my_object = None

    return my_object

#########################################
# DEFINE THE DOWNLOAD AND SHOW FUNCTION #
#########################################


def img_fetcher(my_object, counter, action='show'):

    # print(f"--> Getting the image: {my_object['name']}")

    # rescale
    base_url, shape, resolution, rotation, filetype = (my_object['img_url'].rsplit("/", 4))
    new_shape = 'square'
    new_resolution = '!500,500'
    new_rotation = 0
    rescaled_url = f"{base_url}/{new_shape}/{new_resolution}/{new_rotation}/{filetype}"
    # print(f"-----> the rescaled url is: {rescaled_url}")

    # Send a GET request to the IIIF URL
    try:
        img_response = session.get(rescaled_url, headers=headers, timeout=(1, 3))

        # Check if the request was successful (status code 200)
        if img_response.status_code == 200:

            if action == 'show':
                # Open the image from the response content
                image = Image.open(BytesIO(img_response.content))
                # Display the image
                image.show()

            if action == 'download':
                try:
                    filename = f"data/image{counter}.jpg"
                    with open(filename, "wb") as file:
                        file.write(img_response.content)
                        # ("----->  Image downloaded successfully.")
                        pass
                except PermissionError:
                    print('file is open in viewer')
        else:
            print(f"----->  Request failed with status code: {img_response.status_code}")

    except requests.exceptions.Timeout:
        print("uh ow, timeout while downloading")

###################################################################
#  FUNCTION THAT GETS TRIGGERED WHEN NEW IMAGES HAVE TO BE LOADED #
###################################################################


def load_new_imgs(start_index):

    # define array to loop through and an index to start from
    img_array = [1, 2, 3, 4, 5]
    my_index = start_index

    # print(f'Loading {len(img_array)-3} images, starting with image {start_index+1}')
    # get 2 new random images, starting from the start_index
    for item in range(len(img_array)-3):
        # update the counter
        my_index = (my_index + 1) % len(img_array)

        image_id = img_array[my_index]

        # get the metadata of a random image
        print(f'Loading image {image_id}.', end='')
        image = None
        while image is None:
            image = data_fetcher()
            print('.', end='')

        # download the image
        img_fetcher(image, image_id, action='download')
        print('.', end='')

        # store the metadata
        json_string = json.dumps(image)
        data_path = f'data/image{image_id}.json'
        with open(data_path, 'w') as file:
            file.write(json_string)

        print()

    print("New load complete!")


# load images on boot
starting_index = 0
print('Erfgoed bij de koffie, geniet van deze ervaring!')
load_new_imgs(2)

key_pressed = False


# now wait for the spacebar to do new things
def spacebar_action():
    # When the spacebar is pressed, load the next images
    # print("Spacebar pressed!")
    global key_pressed
    global starting_index
    if not key_pressed:
        key_pressed = True
        print(f'Loading two new images. The current index is {starting_index}')
        starting_index = (starting_index + 1) % 5  # proceed step by step (0 - 1 -2 -3 - 4)
        load_new_imgs(starting_index + 1)  # load 3 images ahead
    else:
        key_pressed = False
    key_pressed = False
    print("Space bar loads two new images.")


# Register the spacebar key press event
keyboard.on_press_key("space", lambda e: spacebar_action())

# Listen for events until 'q' is pressed
keyboard.wait("esc")

# Unregister the event handler
keyboard.unhook_all()
