# jav-scraper
This script scrap the data from JAV website, download the poster and rename the folder to movie title

### Prep
- python3
- Windows/Linux/Mac OS
- Folder name: SISS-123, JUL-303 etc..

### How to use
Because JavLibrary use CloudFlare anti-bot protection, we need to use cookies to by pass it
1. Access JavaLibrary from Chrome, go to console developer -> network tab -> doc -> set_cookies, extract string value of cf_clearance and User-Agent fields
2. Copy above value to cookies.json

```
pip3 install -r requirments.txt
python3 main.py <path_to_folder>
```

### Notes
Cookies has expired, need to update new cookies to cookies.json when expired