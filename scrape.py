from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient


url= 'https://www.pricecheck.co.za/categories/166/Wines%20&%20Spirits?category=7428'

page = requests.get(url).text
soup = BeautifulSoup(page,'lxml')
items=[]
Client = MongoClient();
db=Client["Beverages"]
collection=db["Alcoholic"]


for div in soup.find_all('div',{'class':'rowgrid'}):

    try:
        title = div.h5.a.text
        description = div.find('p',{'class':'card-text'}).text
        price= div.find('a',{'class':'text-red'}).text
        store = div.find('span',{'class':'d-block'}).b
        imgDiv = div.find('div',{'class':'background-image'}).attrs['style'][21:]
        img_url=imgDiv.split(')')

        
        item={"img":img_url[0],"title":title,"descr":description,"price":price,"store":store}
        obj ={}
        obj["Image"] = img_url
        obj["Title"] = title
        obj["Descr"]=description
        obj["Price"]=price
        
        collection.insert_one(obj)
        items.append(item)



    except Exception as identifier:
        pass
        

def show_items():
    for d in items:
        print(d['title'])
        print(d['price'])
        print(d['store'])
        print('.........')

show_items()
