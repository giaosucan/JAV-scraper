# import cloudscraper
import json
import os
import logging
import urllib.request
from javlibrary import JAVLibrary

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_list_folder(directory_path):
    return [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

def get_movie_info(code, userAgent, javlibraryCFClearance):
    jav = JAVLibrary(userAgent, javlibraryCFClearance)
    return jav.get_metadata(code)

def download_poster(urls,path,poster):
    # Send a GET request to the URL
    for url in urls:
        try:
            urllib.request.urlretrieve(url, path + poster + ".jpg")        
            logging.debug('Image successfully downloaded and saved!')
        except Exception as e:
            logging.error(f'Failed to retrieve image. {e}')

BASE_PATH = "/mnt/d/Download/"

def main():
    # Your main code logic here
    print("Start scrapping data")    
    # Load JSON data from a file
    with open('cookies.json', 'r') as file:
        data = json.load(file)
    # Accessing values
    userAgent = data["userAgent"]
    javlibraryCFClearance = data["javlibraryCFClearance"]
    list_code = get_list_folder(BASE_PATH)
    logging.debug(f"list folders name {list_code}")    
    for code in list_code:
        movie_info = get_movie_info(code,userAgent=userAgent,javlibraryCFClearance=javlibraryCFClearance)       
        download_poster(movie_info['art'], BASE_PATH+ code + "/", movie_info['title'])
        os.rename(BASE_PATH+ code, BASE_PATH + movie_info['title'])
if __name__ == "__main__":
    main()

