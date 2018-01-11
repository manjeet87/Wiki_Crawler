import requests
from bs4 import BeautifulSoup as bs
import time


def check_crawler(links_list, new_link, target_url):
    if new_link in links_list[:-1]:
        print ("Link directed to earlier link in the search history. Aborting")
        return False
    elif len(links_list)>25:
        print ("No. of search trials exceeded limit. Aborting search")
        return  False
    elif new_link == target_url:
        print ("Target link found. Terminating process")
        return False
    elif new_link is None:
        print ("No. link found. Aboritng")
        return False
    else:
        return True


target_url = "https://en.wikipedia.org/wiki/Philosophy"
start_url = "https://en.wikipedia.org/wiki/Animal"


