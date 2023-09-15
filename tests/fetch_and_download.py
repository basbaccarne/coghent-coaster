# this test tests the data_fetcher & object fetcher

# libraries
import sys
sys.path.append('../src')
from fetcher import *

# Get image and save as data/image1.jpg
new_object = data_fetcher()
if new_object is not None:
    img_fetcher(new_object, counter=1, action='download')
