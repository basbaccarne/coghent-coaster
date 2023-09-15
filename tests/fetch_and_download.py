# this test tests the data_fetcher & object fetcher
from src.fetcher import *

# Get random image information
new_object = data_fetcher()

# If we get a result, download that image as data/image1.jpg
if new_object is not None:
    img_fetcher(new_object, counter=1, action='download')