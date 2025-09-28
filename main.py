import json
import re
import os
import time
import logging
import urllib.request
import argparse
from javlibrary import JAVLibrary

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_movie(directory_path, userAgent, javlibraryCFClearance):
    """
    Process each movie directory in the given path.

    Args:
        directory_path (str): The path to the directory containing movie directories.
        userAgent (str): The user agent string to use for web requests.
        javlibraryCFClearance (str): The CF clearance token to use for JAVLibrary requests.
    """
    
    movie_dirs = get_list_folder(directory_path)
    for movie_dir in movie_dirs:    
        logging.debug(f"Processing movie directory: {movie_dir}") 
        movie_info = get_movie_info(movie_dir, userAgent, javlibraryCFClearance)
        print(movie_info)
        if movie_info:
            poster_urls = movie_info.get('art', [])           
            if poster_urls:
                download_poster(poster_urls, os.path.join(directory_path, movie_dir), movie_dir)
                 # Remove both double quotes and single quotes
                cleaned_title = re.sub(r'[\\/:*?"<>|\'"]', '', movie_info["title"])
                 # Strip leading/trailing spaces and dots
                cleaned_title = cleaned_title.strip(" .")
                movie_info["title"] = cleaned_title[:255]
                os.rename(directory_path + movie_dir, directory_path + movie_info['title'])
            else:
                logging.warning(f"No poster URLs found for movie code: {movie_dir}")
        
        time.sleep(3) ## Avoid to many request exception

def get_list_folder(directory_path):
    """
    Get a list of all directories in the given path.
    Args:
        directory_path (str): The path to the directory.
    Returns:
        list: A list of directory names.
    """
    return [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

def get_movie_info(code, userAgent, javlibraryCFClearance):
    """
    Get the metadata for a movie using the JAVLibrary API.
    Args:
        code (str): The movie code.
        userAgent (str): The user agent string to use for web requests.
        javlibraryCFClearance (str): The Cloud Flare clearance cookies to use for JAVLibrary requests.
    Returns:
        dict: A dictionary containing the movie metadata, or None if the metadata could not be retrieved.
    """
    try:
        jav = JAVLibrary(userAgent, javlibraryCFClearance)
        return jav.get_metadata(code)
    except Exception as e:
        logging.error(f"Error getting movie info for code {code}: {e}")
        return None

def download_poster(urls, path, poster):
        """
        Download a movie poster from the given URLs and save it to the specified path.
        Args:
            urls (list): A list of URLs where the poster image can be downloaded.
            path (str): The path to the directory where the poster should be saved.
            poster (str): The filename for the poster image.
        """
        for url in urls:
            try:
                urllib.request.urlretrieve(url, os.path.join(path, f"{poster}.jpg"))
                logging.debug(f'Image successfully downloaded and saved to {os.path.join(path, f"{poster}.jpg")}')
            except Exception as e:
                logging.error(f'Failed to retrieve image from {url}. Error: {e}')

def main():
    parser = argparse.ArgumentParser(description="JAV scrapper",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('directory_path', type=str, help='Path of the folder to scrap')
    args = parser.parse_args()
    config = vars(args)    
 
    logging.info(f"Start scrapping data from folder {config['directory_path']}...")       
    
    # Load JSON data from a file
    with open('cookies.json', 'r') as file:
        data = json.load(file)
    # Accessing values
    userAgent = data["userAgent"]
    javlibraryCFClearance = data["javlibraryCFClearance"]       
    process_movie(config['directory_path'], userAgent, javlibraryCFClearance)  

if __name__ == "__main__":
    main()

