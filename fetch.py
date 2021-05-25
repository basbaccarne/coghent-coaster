# Run a script that downloads a random Unsplash image

# Arguments:
# key = Unsplash key (cfr. https://unsplash.com/developers)
# name = image filename (default = "image.jpg")

# Result: Random image is downloaded in program dir

import urllib.request
import json

my_key = "###"


def get_unsplash(key, name="image.jpg"):
    # Part 1: construct URL (feed your key)

    base_url = "https://api.unsplash.com"
    endpoint = "/photos/random"  # endpoint for a random image entry
    get_url = base_url + endpoint + "?client_id=" + key

    # Part 2: get a random download link

    print("Randomly picking a nice picture ...")
    print("(Remember I can only do this 50 times per hour due to free API limitations)")
    data = urllib.request.urlopen(get_url).read()  # get json (max 50 per seconde)
    response = json.loads(data)  # parse json als python dictionary
    img_url = response['urls']['small']  # geef url door

    # Part 3: download the image from the URL and store it in 'dir' with name 'name'

    print("Downloading that nice picture to your disk ...")
    urllib.request.urlretrieve(img_url, name)
    print("Yes, the picture is there! Called" + name)


get_unsplash(my_key)
