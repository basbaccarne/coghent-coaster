# This script accesses the CoGhent API to fetch and show a random image
# (API documentation: https://coghent.github.io/)

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

##################
# QUERY SETTINGS #
##################

# Set SPARQL datasource url
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

#########################
# FETCH RANDOM MANIFEST #
#########################

print(f"Getting a random manifest ....")

# Get the data and convert the results to a JSON format
sparql.setReturnFormat(JSON)
response = sparql.query().convert()

# If the response has content, store the URI of the manifest
if 'results' in response and 'bindings' in response['results']:
    bindings = response['results']['bindings']

    if len(bindings) > 0:
        first_result = bindings[0]
        uri = first_result['o']['value']
        print(f"the random URI is: {uri}")
    else:
        print("No results found.")
else:
    print("Invalid or empty response.")

##############################
# GET DATA FROM THE MANIFEST #
##############################

print(f"Fetching data from the manifest ....")

# Fetch the data
uri_response = requests.get(uri)

# Process the incoming signal
if uri_response.status_code == 200:
    data = uri_response.json()
else:
    print(f"Failed to fetch data. Status code: {uri_response.status_code}")
if uri_response.status_code == 403:
    data = 403
    print(f"We ran into auth issues")

#############################
# PROCESS THE INCOMING DATA #
#############################

# If there is data, get the values from the jason data"
if data != 403:
    name = data['label'] ['@value']
    print(f"the name of the oject is: {name}")

    attribution = data['sequences'] [0] ['canvases'] [0] ['images'] [0] ['attribution']
    print(f"the attribution is: {attribution}")

    img_url = data['sequences'] [0] ['canvases'] [0] ['images'] [0] ['resource'] ['@id']
    print(f"the image url is is: {img_url}")

#############################
# DOWNLOAD & SHOW THE IMAGE #
#############################

# Send a GET request to the IIIF URL
if data != 403:
    img_response = requests.get(img_url)

    # Check if the request was successful (status code 200)
    if img_response.status_code == 200:
        # Open the image from the response content
        image = Image.open(BytesIO(img_response.content))

        # Display the image
        image.show()
    else:
        print(f"Request failed with status code: {response.status_code}")
