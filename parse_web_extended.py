import requests
from bs4 import BeautifulSoup
from PIL import Image

# Parses the humanphenotypes.net website
# Downloads images of human phenotypes
# Separates the female and male images
# ==> See "images" folder

def create_link_list(webpages=148):
    link_list = []
    for i in range(1, webpages):
        url = "http://humanphenotypes.net/map/"+str(i)+".html"
        print(url)
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        table = soup.find("table")
        tds = table.find_all("td")
        for td in tds:
            try: 
                link = td.find("a")['href']
                link = link[2:]
                link_list.append(link)
            except TypeError: 
                continue
    print(set(link_list))
    return set(link_list) # /basic/Eskimid.html


def create_img_link_list(link_list):
    male_img_link_list = []
    female_img_link_list = []
    for link in link_list:

        link = "http://humanphenotypes.net"+link
        print(link)
        respond = requests.get(link)
        if respond.status_code != 200:
            continue
        soup = BeautifulSoup(respond.text, "html.parser")
        table = soup.find("table")
        tds = table.find_all("td")
        td_male = tds[2]
        td_female = tds[3]
        
        td_male_img_link = td_male.find("img")['src']
        male_img_link_list.append(td_male_img_link)
        td_female_img_link = td_female.find("img")['src']
        female_img_link_list.append(td_female_img_link)
    return male_img_link_list, female_img_link_list

def create_img(male_img_link_list, female_img_link_list):
    for i in range(0, len(male_img_link_list)):
        m_img_url = "http://humanphenotypes.net/basic/" + male_img_link_list[i]
        f_img_url = "http://humanphenotypes.net/basic/" + female_img_link_list[i]

        m_img = Image.open(requests.get(m_img_url, stream=True).raw)
        f_img = Image.open(requests.get(f_img_url, stream=True).raw)

        m_img.save("images/"+male_img_link_list[i])
        f_img.save("images/"+female_img_link_list[i])

links = create_link_list(139)
male_img_link_list, female_img_link_list = create_img_link_list(links)
create_img(male_img_link_list, female_img_link_list)
