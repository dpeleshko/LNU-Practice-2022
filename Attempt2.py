from cgitb import text
import requests
import urllib3
from bs4 import BeautifulSoup
import stringformat
import re
import unidecode


# html_text = requests.get('https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q=Xiaomi').text
# print(html_text)

def getHTMLtext(url):
    http = urllib3.PoolManager()
    resp = http.request('GET', url)
    html_text = resp.data.decode('utf-8')
    soup = BeautifulSoup(html_text, 'lxml')
    return soup

def textFormat(txt):# Just for text formating
    return re.sub(' +', ' ',txt.replace('\n', '').replace('\t','').lstrip())

def getFormatedItems(html_txt):
    items = html_txt.find_all('div', class_='list-item list-item--row')#not formated
    items_formated = list()
    for item in items:
        item_formated= list()
        item_link= "https://hotline.ua" + item.find_all('a')[1].get('href')#magic number
        item_title = textFormat(item.find('a', class_='list-item__title text-md').text)
        item_price = unidecode.unidecode(textFormat(item.find('span', class_='price__value').text))
        item_specification = textFormat(item.find('div', class_='list-item__specifications-text').text)
        #Add to small list
        item_formated.append(item_title)
        item_formated.append(item_link)
        item_formated.append(item_price)
        
        items_formated.append(item_formated)#add to return list
    return items_formated

def printItem(item):
    print(f"Title: {item[0]}")
    print(f"Link: {item[1]}")
    print(f"Price: {item[2]}")
def printItems(items):
    for item in items:
        printItem(item)
        print('')
search = str(input("Enter what are you looking for: "))
# search = "xiaomi"
items = getFormatedItems(getHTMLtext('https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q='+search))
# items = getFormatedItems(getHTMLtext("https://hotline.ua/ua/sr/?q=Wi%20fi"))
printItems(items)
# search ="TP link"
# url = 'https://hotline.ua/ua/sr/?q=Wi-fi'
# myobj = {'somekey': 'somevalue'}
# json_ = """{"jsonrpc":"2.0","method":"search.search","params":{"q":"""+search+""","lang":"uk","section_id":null,"entity":"full"},"id":1}"""
# x = requests.post(url, json = json_)
# #print(x.text)
# http = urllib3.PoolManager()
# resp = http.request('POST', url,json= json_)
# html_text = resp.data.decode('utf-8')
# soup = BeautifulSoup(html_text, 'lxml')
# printItems(getFormatedItems(soup))
# http = urllib3.PoolManager()
# r = http.request(
#     'POST',
#     'http://httpbin.org/post',
#     fields={'hello': 'world'}

# )