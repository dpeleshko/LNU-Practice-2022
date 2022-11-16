from cgitb import text
from xml.etree.ElementTree import iterparse
import requests
import urllib3 #internet requests
from bs4 import BeautifulSoup #HTML text formattig and managing
import stringformat
import re #for text formatig
import unidecode
import os
from math import floor
import urllib.request #for image downloading
# html_text = requests.get('https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q=Xiaomi').text
# print(html_text)

def deleteCharsFromText(text, chars):
    for char in chars:
        text=text.replace(char,"")
    return text
class Review:#Need getReviews method for working
    def __init__(self,comment,stars, user):
        self.comment = comment
        self.stars = unidecode.unidecode(textFormat(stars))
        self.username = user
    def print(self):
        print(f"User: {self.username}")
        print(f"Review text: {self.comment}")
        print(f"Stars: {self.stars}")
    def keyWordsSearch(self, key_words):
        key_words = deleteCharsFromText(key_words,",.!()?{[}]\|").lower().split()
        comment_text = self.comment.lower()
        for word in key_words:
            if word not in comment_text:
                return False
        return True
    def countWords(self):#roughly
        return self.comment.count(" ")+1
    def isInStars(self, stars):
        return stars==None or (stars == floor(float(self.stars)))
    def isInCritarias(self, key_words, stars, isLong):
        min_words = 0
        if isLong:
            min_words = 15
        return self.keyWordsSearch(key_words) and self.isInStars(stars) and self.countWords()>=min_words
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
        #self.av_stars = 0
        if(self.isImageExist()):
            self.image_path = f"Images/{self.title}.jpg"
        
        # html = getHTMLtext(link)
        # self.average_rating = html.find("div",class_="informer-review__rating-value").text
    
    def downloadReviews(self):
        html = getHTMLtext(self.link+"?tab=reviews&filter=reviews")
        try:
            self.av_stars = float(html.find("div",class_="informer-review__rating-value").text)
        except:
            self.av_stars = 0
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
    def getInfo(self):
        info = []
        info.append(self.title)
        info.append(self.price)
        info.append(self.link)
        return info
    def getReviewFromCriterias(self, key_words, stars, isLong):#return first appearence
        good_reviews = []
        for review in self.reviews:
            if review.isInCritarias(key_words, stars, isLong):
                good_reviews.append(review)
        return good_reviews
        

        
def getHTMLtext(URL):#search_text):#text version of HTML page
    #url = 'https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q='+formatingSearch(search_text)
    http = urllib3.PoolManager()
    resp = http.request('GET', URL)
    html_text = resp.data.decode('utf-8')
    soup = BeautifulSoup(html_text, 'lxml')
    return soup

def textFormat(txt):# Just for text formating(delete the spaces between words)
    return re.sub(' +', ' ',txt.replace('\n', '').replace('\t','').lstrip().rstrip())

# def getFileExtension(url):
#     return url.split('.')[-1]

def addFormatedItems(html_txt, items_class):#from Hotline page
    items = html_txt.find_all('div', class_='list-item list-item--row')#not formated
    #items_formated = list()
    for item in items:
        #item_formated= list()
        item_link= "https://hotline.ua" + item.find_all('a')[1].get('href')#magic number
        item_title = textFormat(item.find('a', class_='list-item__title text-md').text)
        item_price = unidecode.unidecode(textFormat(item.find('span', class_='price__value').text))
        item_specification = textFormat(item.find('div', class_='list-item__specifications-text').text)
        
        try:
            item_img_url = "https://hotline.ua"+item.find('img').get('src')
            urllib.request.urlretrieve(item_img_url, f"Images/{item_title}.jpg")
            #print(f"Title: {item_title}\nURL: {item_img_url}\n")
        except Exception as e:
            continue
            #print(f"Title: {item_title}\nURL: {item_img_url}\nError: {e}\n")
            pass
            

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
    

def deleteImages():
    for file in os.listdir("Images"):
        os.remove(f"Images/{file}")

# createFolder("Images")

# search = "Xiaomi Mi WiFi Router 4A Gigabit Edition"
# # search = str(input("Enter what are you looking for: "))
# items_class = []
# addFormatedItems(getHTMLtext("https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q="+formatingSearch(search)),items_class)


# items_class[0].downloadReviews()
# key_words = "працює"
# review = items_class[0].getReviewFromCriterias(key_words, None, False)
# if review:
#     review.print()

#deleteImages()
#input("\n\nEnter to exit....")