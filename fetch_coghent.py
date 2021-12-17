# These are some tests to use the CoGhent SPARQL in Python #
############################################################

# Somehow I needed to solve https issues (I kept getting [SSL: CERTIFICATE_VERIFY_FAILED] errors)
# The following hack solved the issue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Include the SPARQLWrapper library
from SPARQLWrapper import SPARQLWrapper, JSON

# Set SPARQL source url (no idea what this is ;))
sparql = SPARQLWrapper("https://stad.gent/sparql")

# Define the query (you can test this, using the source url on http://query.linkeddatafragments.org/)
sparql.setQuery("""
        PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
        SELECT DISTINCT ?title
        WHERE { 
          ?object cidoc:P102_has_title ?title.
        } LIMIT 10
""")

# Get the data and convert the results to a JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

# Print all the data fields that are in the first entry (called a binding)
# print(result['results']['bindings'][0])

# Show all the titles in the retrieved JSON object
print("These are 10 sample titles:")
for each in result['results']['bindings']:
    print(each['title']['value'])

# How many entries are there with a title?
sparql.setQuery("""
        PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
        SELECT (COUNT(*) AS ?count) 
        WHERE { 
          ?object cidoc:P102_has_title ?title.
        } 
""")
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

print("\n" , result['results']['bindings'][0]['count']['value'], "= total n° of objects counted with a title")
