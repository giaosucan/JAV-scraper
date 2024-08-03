# import cloudscraper
import json
from javlibrary import JAVLibrary


# Load JSON data from a file
with open('cookies.json', 'r') as file:
    data = json.load(file)

# Accessing values
userAgent = data["userAgent"]
javlibraryCFClearance = data["javlibraryCFClearance"]

jav = JAVLibrary(userAgent, javlibraryCFClearance)
movieInfo = jav.get_metadata("ADN-333")
print(movieInfo)


