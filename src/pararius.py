import json
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from tqdm import tqdm
from src.base_requests import BaseRequests


HOST = "https://www.pararius.com"


class Pararius(BaseRequests):

    def __init__(self):
        super(Pararius, self).__init__(HOST)
        self.host = HOST


    def get_listings(self, endpoint="/apartments/amsterdam/1500-2200/", page=1):
        endpoint = endpoint + "page-" + str(page)
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
        }
        r = self.get(endpoint, headers=header)
        soup = BeautifulSoup(r.text, features="html.parser")
        listings = [x.find("a")["href"] for x in soup.find_all("h2", {
            "class": "listing-search-item__title"
            })]
        return listings

    
if __name__ == "__main__":
    pararius = Pararius()
    r = pararius.get_listings(page=1)
    print(r)
