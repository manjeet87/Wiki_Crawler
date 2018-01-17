import requests
from bs4 import BeautifulSoup as bs
import time
import pprint

max_steps = 35
target_url = "https://en.wikipedia.org/wiki/Philosophy"
start_url = "https://en.wikipedia.org/wiki/Rama"

def check_crawler(links_list, new_link, target_url):
    global max_steps
    if len(links_list) == 1 :
        return True
    elif new_link in links_list[:-1]:
        print ("Link directed to earlier link in the search history. Aborting")
        return False
    elif len(links_list)>max_steps:
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

def generate_firstLink(link_url):
    response = requests.get(link_url)
    soup = bs(response.content, 'lxml')
    lst = soup.find_all('p')
    try:
        childList = lst[0].findChildren()
        # for child in childList:
        #     print (child)
        # it has to ensured that only the direct link in the text of body is extracted. Not of others for translations etc
        first_link = "https://en.wikipedia.org" + soup.select_one('div > p > a')['href']
        print(link_url)
    except:
        first_link = None
    return first_link

link_url = start_url
articleLink_lst = []
articleLink_lst.append(start_url)
itr = 0

while(check_crawler(articleLink_lst,link_url,target_url)):
    next_url = generate_firstLink(link_url)
    articleLink_lst.append(link_url)
    link_url = next_url
    itr +=1
    #time.sleep(0.5)

pprint.pprint(articleLink_lst)


