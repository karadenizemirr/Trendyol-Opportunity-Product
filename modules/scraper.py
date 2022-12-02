import requests
import re
import os
from rich.console import Console
from bs4 import BeautifulSoup
from modules.user_agent import user_agent
from modules.bypass import cloudflare_bypass
from modules.telegram import telegram
from modules.logger import logger

class Scraper:
    def __init__(self):
        self.console = Console()
        self.session = requests.Session()
        self.bypass = cloudflare_bypass.Bypass()
        self.telegram = telegram.Telegram(token="5750542194:AAHUctF5ImPnjjOmobKfh7pUBsd_5ZHobG8", user_id="744777387")
        self.telegram_my = telegram.Telegram(token="5901890521:AAG_9fjlySpTIQmJD-pb5wjYXC8hU-jjVvA", user_id="5669620760")
        self.base_url = "https://www.trendyol.com/"
        # &pi=4

    def get_page_number(self, link=None):
        counter = 1
        
        while True:
            _link = f"{link}&pi={counter}"
            req = self.bypass.get(URL=_link, allow_redirect=True)
            html = BeautifulSoup(req, 'lxml').findAll('div', {'class': 'prdct-cntnr-wrppr'})

            if len(html) < 1:
                if counter >= 150:
                    break
                break
            counter += 1
        
        return counter - 1
        
    def get_product_link(self,links=[]):
        for link in links:
            req = self.bypass.get(URL=link)
            html = BeautifulSoup(req, 'lxml')

            links = []

            link_html = html.findAll('div', {'class' : 'p-card-chldrn-cntnr card-border'})
            
            for l in link_html:
                links.append(f"{self.base_url}{str(l.findNext('a')['href']).strip()}")
            
            # Save Links File

            with open('data/links.txt', 'w', encoding='utf-8') as file:
                for _ in links:
                    file.write('\r')
                    file.write(_.strip())
            
            return links
    
    def get_product_detail(self):
        links = []

        try:
            os.remove('data/links.txt')
        except:
            pass
        with open('data/links.txt', 'r', encoding='utf-8') as file:
            for f in file.readlines():
                links.append(f.strip())
        links.pop(0)
        for link in links:
            req = self.bypass.get(URL=link)
            html = BeautifulSoup(req, 'lxml')
            
            title = self.get_title(html)
            seller = self.get_seller(html)
            price = self.get_price(html)
            
            try:
                other_seller = html.findAll('div', {'class': 'pr-mc-w gnr-cnt-br'})[0]
                other_seller_name = self.get_other_seller_name(other_seller)
                other_seller_price = self.get_other_seller_price(other_seller)
                percent = ((price - other_seller_price) / price) * 100
            except:
                percent = "none"
                continue

            
            if percent >= 25:
                message = f""" 
                \n<b>TRENDYOL FIRSAT ÜRÜNÜ</b>\n\n\n<a href="{link}">{title}</a>\n\n<b>Satıcı:</b>{seller}\n<b>Fiyatı:</b>{price} TL\n<b>Fırsat Satıcı:</b>{other_seller_name}\n<b>Fırsat Fiyat:</b>{other_seller_price} TL\n<b>Yüzdelik Fark:</b>{"%.2f" % percent}\n\n
                """
                self.telegram.sendMessage(message=message)
                self.telegram_my.sendMessage(message=message)
            
            logger.create_log(link, 'linkControlLog')   
    
    def get_title(self, soup):
        try:
            title = soup.findAll('h1', {'class': 'pr-new-br'})[0].text
        except:
            title = "null"
        
        return title
    
    def get_seller(self, soup):
        try:
            seller = soup.find('a', {'class': 'merchant-text'}).text
        except:
            seller = "null"
        
        return seller
    
    def get_price(self, soup):
        try:
            price = float(re.sub(r',(.*)','',soup.find('span', {'class': 'prc-dsc'}).text))
        except:
            price = "null"
        
        return price
    
    def get_other_seller_name(self, soup):
        try:
            other_seller_name = soup.find('div', {'class': 'seller-container'}).a.text
        except:
            other_seller_name = "null"
        
        return other_seller_name
    
    def get_other_seller_price(self, soup):
        try:
            other_seller_price = float(soup.find('span', {'class': 'prc-dsc'}).text.replace(' TL', ''))
        except:
            other_seller_price = "null"
        
        return other_seller_price
    
    def get_product_img(self, soup):
        try:
            product_img = soup.findAll('div', {'class': 'gallery-container'})[0].img['src']
        except:
            product_img = "null"
        
        return product_img