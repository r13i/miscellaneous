
### Load JSON from API
import urllib.request           # Fetch from the API
import json                     # Parse json
from pprint import pprint       # Pretty print (makes printing dictionaries more beautiful)

API_URL = "https://www.sats.se/webapi/filteredcenters/sv/0/0"

with urllib.request.urlopen(API_URL) as url:
    # Load JSON formatted as 'bytes'
    byteJson = url.read()

    # Convert bytes to string
    stringJson = byteJson.decode()

    # Convert string json to a python dictionary
    data = json.loads(stringJson)

    # Or do the operation in a single line:
    # data = json.loads(url.read().decode())

    # Pretty print
    pprint(data)



### Walking through the data

for region in data["Regions"]:

    # for center in region["Centers"]:
    #     print(center["Name"])

    # Or use 'enumerate' to get both element and his index in the array
    for idx, center in enumerate(region["Centers"]):
        print("{index} => {name}".format(index = idx, name = center["Name"]))

    print('=' * 30)     # Horizontal separator (just to separate and make lists more visible)