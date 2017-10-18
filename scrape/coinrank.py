from bs4 import BeautifulSoup
import requests, urllib
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

    def getAllImages(self):
        # self._pageControl()
        # self._getUrls()

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
        
    def _pageControl(self):
        print '> start preparing pages'
        driver = webdriver.Chrome()
        driver.get(self.url)
        button = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div/button')
        while True: 
            if button: 
                print 'There is a button'
                button.click()
                print 'nextPage'
                sleep(1)
        print "> waiting for a minute, so it can load ..."
        sleep(60)


    def _getCoins(self, page):
        print "> getting page", page
        scrape_url = self.url + '?page=' + str(page)
        req = requests.get(scrape_url)
        print scrape_url
        soup = BeautifulSoup(req.content,'lxml')
        a = soup.find_all('a',{'class','coin-list__body__row'})
        for item in a:
            icon = item.find('span',{'class':'coin-list__body__row__cryptocurrency__prepend__icon'})
            name = item.find('span',{'class':'coin-name'}).get_text(strip=True).replace(' ','_')
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
                urllib.urlretrieve(coin.image,'./../images/cryptocoins/'+coin.name.lower()+'.svg')  
                sleep(0.5)

coinRank = CoinRank()
coinRank.getAllImages()
coinRank.saveAllImages()
