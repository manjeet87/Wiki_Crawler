import requests
from bs4 import BeautifulSoup as bs
import time
import pprint

max_steps = 35
target_url = "https://en.wikipedia.org/wiki/Philosophy"
start_url = "https://en.wikipedia.org/wiki/People"

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
        link_tag = soup.select_one('div > p > a')
        first_link = "https://en.wikipedia.org" + link_tag['href']
        print("Link found before Check: ",first_link)

        link_tag = checkBracket(link_tag)
        first_link = "https://en.wikipedia.org" + link_tag['href']
        print("Link found After Check: ", first_link)

    except:
        first_link = None

    return first_link


def checkBracket(link_tag):
    pos = 0
    link_tagPos = 0
    Openbracket_pos = 0
    Closebracket_pos = 0
    p_tag = link_tag.find_parent('p')
    child_lst = list(p_tag.children)
    for child in child_lst:
        try:
            if link_tag.string == child.string:
                link_tagPos = pos
            if child.string.find('(') != -1:
                Openbracket_pos = pos
            if child.string.find(')') != -1:
                Closebracket_pos = pos
        except:
            continue

        pos +=1

    if (Openbracket_pos < link_tagPos) and (Closebracket_pos > link_tagPos):   ## This means that our original link-tag is inside bracket

        pos = Closebracket_pos
        ## Searching for just nest link_tag outside the brackets, starting from closebracket position
        while(pos != (len(child_lst)-1)):
            try:
                if child_lst[pos].name == 'a':
                    link_tag = child_lst[pos]
                    print (link_tag)
                    break          ## Breaking the loop as the next first link_tag is found
            except:
                continue
            pos +=1

    return link_tag




link_url = start_url
articleLink_lst = []
articleLink_lst.append(start_url)
itr = 0

while(check_crawler(articleLink_lst,link_url,target_url)):
    next_url = generate_firstLink(link_url)
    articleLink_lst.append(next_url)
    link_url = next_url
    itr +=1
    #time.sleep(0.5)



