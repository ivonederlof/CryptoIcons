from bs4 import BeautifulSoup
import requests, urllib2, cookielib
from time import sleep
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options

class Coin(object):

    def __init__(self, name, image):
        self.name = name 
        self.image = image
 
class CoinRank(object):

    url = "https://coinranking.com/"
    coins = [] 
    page = 1
    total_pages = 1

    def __init__(self):
        self._get_total_pages()
        print "start"

    def getAllImages(self):

        while self.page <= self.total_pages: 
            print self.page
            self._getCoins(self.page)
            self.page += 1 

    def _get_total_pages(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.content,'lxml')
        pages = soup.find('span',{'class':'pagination__info'})
        self.total_pages = int(pages.find_all('b')[1].get_text(strip=True))
        print '> total pages:', self.total_pages
        

    def _getCoins(self, page):
        print "> getting page", page
        scrape_url = self.url + '?page=' + str(page)
        req = requests.get(scrape_url)
        print scrape_url
        soup = BeautifulSoup(req.content,'lxml')
        a = soup.find_all('a',{'class','coin-list__body__row'})
        for item in a:
            icon = item.find('span',{'class':'coin-list__body__row__cryptocurrency__prepend__icon'})
            name = item.find('span',{'class':'coin-name'}).get_text(strip=True).replace(' ','-')
            if icon:
                img = icon.img   
                if img:
                    coin = Coin(name, img['src'])
                    self.coins.append(coin)
                    print coin.name

        sleep(2)

    def saveAllImages(self):
        print "> saving images"
 
        for coin in self.coins:
            if coin.image and coin.name:
                print '> request:', coin.image

                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                req = requests.get(coin.image, headers=headers)
                content = req.headers['content-type']
             
                if req.status_code == 200:
                    if content:
                        if content == 'image/svg+xml':
                            with open('./../images/cryptocoins/'+coin.name.lower()+'.svg', 'wb') as f:
                                f.write(req.content)

                        elif content == 'image/jpg':
                            with open('./../images/cryptocoins/'+coin.name.lower()+'.jpg', 'wb') as f:
                                f.write(req.content)

                        elif content == 'image/png':
                            with open('./../images/cryptocoins/'+coin.name.lower()+'.png', 'wb') as f:
                                f.write(req.content)
                                
                sleep(10)

coinRank = CoinRank()
coinRank.getAllImages()
coinRank.saveAllImages()
