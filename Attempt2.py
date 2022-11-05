from cgitb import text
from xml.etree.ElementTree import iterparse
import requests
import urllib3 #internet requests
from bs4 import BeautifulSoup #HTML text formattig and managing
import stringformat
import re#for text formatig
import unidecode
import os
import urllib.request #for image downloading
# html_text = requests.get('https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q=Xiaomi').text
# print(html_text)

class Review:
    def __init__(self,comment,stars, user):
        self.comment = comment
        self.stars = unidecode.unidecode(textFormat(stars))
        self.username = user
    def print(self):
        print(f"User: {self.username}")
        print(f"Review text: {self.comment}")
        print(f"Stars: {self.stars}")
class Item:
    #items_list = []#for all Item members
    def isImageExist(self):
        return os.path.exists("Images/"+self.title+".jpg")
    def __init__(self,title, link, price, short_specefication):
        self.title  = title
        self.link = link
        self.price = price
        self.specefication = short_specefication
        self.description = str() #TODO
        self.reviews = [] #will add later TODO
        self.image_path = None
        if(self.isImageExist()):
            self.image_path = f"Images/{self.title}.jpg"
        
        # html = getHTMLtext(link)
        # self.average_rating = html.find("div",class_="informer-review__rating-value").text
    
    def getReviews(self):
        html = getHTMLtext(self.link+"?tab=reviews&filter=reviews")
        self.av_stars = float(html.find("div",class_="informer-review__rating-value").text)
        reviews_html = html.find_all("div", class_ ="review__col-content")
        for review in reviews_html:
            try:
                review_text = review.find("div", class_ = "review__comment").text
                review_stars = review.find("div", class_="review__rating-value").text
                reviewer_name = review.find("a", class_="review__user-name").text
            except:
                continue
            self.reviews.append(Review(review_text, review_stars,reviewer_name))
        #print(self.av_stars)
    def print(self):
        print(f"Title: {self.title}")
        print(f"Price: {self.price}")
        print(f"Link: {self.link}")
        #print(f"Specefication: {self.specefication}")
        try:
            print(f"Average rating: {self.av_stars}")
        except:
            pass
    # def saveImage(url, name):
        
    #def getReviews():
        
    #def getDescription():#from item page
        

        
def getHTMLtext(url):#text version of HTML page
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    html_text = resp.data.decode('utf-8')
    soup = BeautifulSoup(html_text, 'lxml')
    return soup

def textFormat(txt):# Just for text formating(delete the spaces between words)
    return re.sub(' +', ' ',txt.replace('\n', '').replace('\t','').lstrip())

def addFormatedItems(html_txt, items_class):#from Hotline page
    items = html_txt.find_all('div', class_='list-item list-item--row')#not formated
    items_formated = list()
    for item in items:
        item_formated= list()
        item_link= "https://hotline.ua" + item.find_all('a')[1].get('href')#magic number
        item_title = textFormat(item.find('a', class_='list-item__title text-md').text)
        item_price = unidecode.unidecode(textFormat(item.find('span', class_='price__value').text))
        item_specification = textFormat(item.find('div', class_='list-item__specifications-text').text)
        
        try:
            item_img_url = "https://hotline.ua"+item.find('img').get('src')
            urllib.request.urlretrieve(item_img_url, f"Images\{item_title}.jpg")
        except Exception as e:
            pass
            # print(f"Title: {item_title}\nURL: {item_img_url}\nError: {e}")

        items_class.append(Item(item_title,item_link,item_price,item_specification))

def printItem(item):
    print(f"Title: {item[0]}")
    print(f"Link: {item[1]}")
    print(f"Price: {item[2]}")
def printItems(items):
    for item in items:
        printItem(item)
        print('')
def formatingSearch(search):#For ability to search with spaces between words
    return search.replace(" ","%20") 

def createFolder(name):
    try:
        os.mkdir(name)
    except:
        pass
    
# search = str(input("Enter what are you looking for: "))
def deleteImages():
    for file in os.listdir("Images"):
        os.remove(f"Images/{file}")

createFolder("Images")
search = "xiaomi"
# search = formatingSearch(search)
items_class = []
addFormatedItems(getHTMLtext('https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q='+search),items_class)
# items = getFormatedItems(getHTMLtext("https://hotline.ua/ua/sr/?q=Wi%20fi"))
#printItems(items)
#item = Item("Xiaomi Mi WiFi Router 4A Global (DVB4230GL)","https://hotline.ua/ua/computer-besprovodnoe-oborudovanie/xiaomi-mi-wifi-router-4a-global-dvb4230gl/", "1022", "Бездротовий маршрутизатор (роутер) • 802.11ac • інтерфейс підключення: 2x10 / 100 Ethernet • швидкість з'єднання: 300 + 867 Мбіт / с • 12.2019")
# for item in items:
#     items_class.append(Item(*item))
#item.print()

# items_class[0].getReviews()
# items_class[0].print()
# items_class[0].reviews[0].print()

# items_class[1].getReviews()
# items_class[1].print()
# items_class[1].reviews[0].print()
for item in items_class:
    if not item.isImageExist():
        item.print()
deleteImages()
input("\n\nEnter to exit....")