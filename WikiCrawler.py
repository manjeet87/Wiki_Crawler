import requests
from bs4 import BeautifulSoup as bs
import time
import pprint


def check_crawler(links_list, new_link, target_url):
    if new_link in links_list[:-1]:
        print ("Link directed to earlier link in the search history. Aborting")
        return False
    elif len(links_list)>35:
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
link_url = start_url
link_lst = []
link_lst.append(start_url)
itr = 0

while(check_crawler(link_lst,link_url,target_url)):
    response = requests.get(link_url)
    soup = bs(response.content, 'lxml')
    lst = soup.find_all('p')
    try:
        childList = lst[0].findChildren()

        # for child in childList:
        #     print (child)
        link_url = "https://en.wikipedia.org" + lst[0].find('a')['href']
        print (link_url)
    except:
        link_url = None
    link_lst.append(link_url)
    itr +=1
    print (itr)
    #time.sleep(0.5)

pprint.pprint(link_lst)


