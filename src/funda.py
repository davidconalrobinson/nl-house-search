import json
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
from tqdm import tqdm
from src.base_requests import BaseRequests


HOST = "https://www.funda.nl"


class Funda(BaseRequests):

    def __init__(self):
        super(Funda, self).__init__(HOST)
        self.host = HOST


    def get_listings(self, endpoint="/en/huur/haarlem,utrecht/beschikbaar/1200-1500/1+kamers/", page=1):
        url = HOST + endpoint
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
            "Origin": HOST,
            "Referer": url + ("" if page == 0 else "p" + str(page) + '/')
        }
        r = self.post(endpoint, headers=header)
        soup = BeautifulSoup(r.text, features="html.parser")
        listings = [listing['url'] for listing in json.loads(soup.find("script", {
            "type": "application/ld+json",
            "data-tracking-properties": None, "data-advertisement-targeting": None
            }).get_text())['itemListElement']]
        return listings


    def get_all_listings(self):
        all_listings = []
        page = 1
        scraping = True
        while scraping:
            try:
                print(f"Scraping page {page}")
                all_listings += self.get_listings(page=page)
                page += 1
            except Exception as e:
                scraping = False
                print(e)
        return all_listings


    def get_listing_availability(self, endpoint):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        r = self.get(endpoint, headers=headers)
        soup = BeautifulSoup(r.text, features="html.parser")
        try:
            acceptance = [x.get_text() for x in soup.find_all("span", {"class": ""}) if x.get_text().startswith("Available ")][0]
            available_on = dt.datetime.strptime(acceptance.split(" ")[2], "%m/%d/%Y").date()
        except:
            available_on = None
        try:
            available = [x.get_text() for x in soup.find_all("span", {"class": ""}) if x.get_text() == "Available"][0]
        except:
            available = "Available"
        return available, available_on


    def get_all(self):
        all_listings = self.get_all_listings()
        available_arr = []
        available_on_arr = []
        for listing in tqdm(all_listings):
            endpoint = listing.replace(HOST, "")
            available, available_on = self.get_listing_availability(endpoint)
            available_arr += [available]
            available_on_arr += [available_on]
        all_listings_df = pd.DataFrame({
            "listing": all_listings,
            "available": available_arr,
            "available_on": available_on_arr   
        })
        all_listings_df["discovered_on"] = dt.date.today() #all_listings_df["available_on"] #
        return all_listings_df
