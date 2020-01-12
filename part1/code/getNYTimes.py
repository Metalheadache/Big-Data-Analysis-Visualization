from nytimesarticle import articleAPI
from bs4 import BeautifulSoup
import requests

api = articleAPI("flnF28k2xaKDGKKzb4GYTzI64koVm6fT")
f=open('nytarticles_maintopic.txt','w',encoding='utf-8')
links=[]

try:
    for a in range(0,20):
        articles = api.search(q="health",begin_date=20190101,page=a)
        for i in range(0,len(articles['response']['docs'])):
            url = articles['response']['docs'][i]['web_url']
            #html = urlopen(url)
            data = requests.get(url)
            soup = BeautifulSoup(data.content, 'html.parser')
            soup.prettify()
            
            for j in range((len(soup.find_all('p')))-3):
                f.write(soup.find_all('p')[j].get_text())
            #print(url)
            links.append(url)
    f.close()
except:
    print(len(links),"articles are acquired.")