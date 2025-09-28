# coding=utf-8
from difflib import SequenceMatcher
import re
from bs4 import BeautifulSoup
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class JAVLibrary():
    def __init__(self, userAgent, javlibraryCFClearance):
        self.userAgent = userAgent
        self.javlibraryCFClearance = javlibraryCFClearance
    
    def get_agent_id(self, keyword):
        keyword = keyword.upper()
        url = "https://www.javlibrary.com/en/vl_searchbyid.php"
        params = {
            "keyword": keyword
        }
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        html = resp.content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        if soup.find("div", "videos"):
            if soup.find("div", "video"):
                for video in soup.find_all("div", "video"):
                    agent_id = video.find("a")["href"][5:]
        else:
            try:
                agent_id = soup.find("h3", "post-title").find("a")["href"][7:]
            except AttributeError:
                logging.error("an exception occurred: " + url)
                return            
        return agent_id 
    
    def get_metadata(self, keyword):
        agent_id = self.get_agent_id(keyword)
        logging.debug(f"get_metadata agent_id : {agent_id}")
        data = self.crawl(agent_id)
        title = self.get_original_title(data)
        if not title:
            raise Exception(
                "Got an unexpected response for {0}".format(keyword))
        return {
            "movie_id": re.split(r"\s", title)[0],
            "agent_id": agent_id,
            "title": title,           
            "roles": self.get_roles(data),            
            "posters": self.get_posters(data),
            "art": self.get_thumbs(data)
        }


    def get_original_title(self, data):
        return data.find("div", {"id": "video_title"}).find("a").text.strip()

    def get_roles(self, data):
        try:
            ele = self.find_ele(data, "Cast:")
            if ele:
                return [               
                    {"name": list(filter(None, item.text.strip().split(" ")))[1] + " " + list(filter(None, item.text.strip().split(" ")))[0]}
                    for item in ele.findAll("a")
                ]
        except Exception as e:
            logging.error(f"Error {e}")
        finally:
            return []   

    def get_posters(self, data):
        javlibrary_thumb = data.find("img", {"id": "video_jacket_img"})
        if javlibrary_thumb and javlibrary_thumb["src"]:
            src = javlibrary_thumb["src"]
            if not src.startswith("http"):
                src = "https:" + src
            return [src.replace("pl.", "ps.")]

    def get_thumbs(self, data):
        javlibrary_thumb = data.find("img", {"id": "video_jacket_img"})
        if javlibrary_thumb and javlibrary_thumb["src"]:
            src = javlibrary_thumb["src"]
            if not src.startswith("http"):
                src = "https:" + src
            return [src]
        
    

    def crawl(self, agent_id):
        url = "https://www.javlibrary.com/en/"
        resp = self.session.get(url, params={
            "v": agent_id
        })
        resp.raise_for_status()
        html = resp.content.decode("utf-8")
        return BeautifulSoup(html, "html.parser")

    def find_ele(self, data, title):
        ele = data.find("table", {"id": "video_jacket_info"})
        single_infos = ele.findAll("tr")
        for single_info in single_infos:
            if single_info.find("td", "header").text.strip() == title:
                return single_info.find("td", "header").findNext("td")

    s_requests = None
    s_cloudscraper = None

    @property
    def session(self):               
        if not self.s_requests:
            self.s_requests = requests.session()
        if self.userAgent:
            self.s_requests.headers["User-Agent"] = self.userAgent
        if self.javlibraryCFClearance:
            self.s_requests.cookies.set(
                "cf_clearance",  self.javlibraryCFClearance, domain=".javlibrary.com")
        return self.s_requests