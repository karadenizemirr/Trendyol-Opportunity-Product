import requests
import re
import os
import random
from rich.console import Console
from rich.progress import Progress
from bs4 import BeautifulSoup
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
        self.base_url = "https://www.trendyol.com"
        # &pi=4

    def get_page_number(self, link=None):
        counter = 1
        
        with self.console.status("[cyan]Sayfa numaraları tespit ediliyor..[/cyan]") as status:
            while True:
                _link = f"{link}&pi={counter}"
                req = self.bypass.get(URL=_link, allow_redirect=True)
                html = BeautifulSoup(req, 'lxml').findAll('div', {'class': 'prdct-cntnr-wrppr'})

                if len(html) < 1:
                    if counter >= 150:
                        break
                    break
                counter += 1
            self.console.log('Sayfa numarası tespit edildi.', style="bold yellow")
            return int(counter - 1)
        
    def get_product_link(self,links=[]):
        _links = []
        for link in links:
            for p in range(0, self.get_page_number(link)):
                req = self.bypass.get(URL=f"{link}&pi={p}")
                html = BeautifulSoup(req, 'lxml')

                link_html = html.findAll('div', {'class' : 'p-card-chldrn-cntnr card-border'})
                
                for l in link_html:
                    _links.append(f"{self.base_url}{str(l.findNext('a')['href']).strip()}")
        try:
            os.remove('data/links.txt')
        except:
            pass
        
        with open('data/links.txt', 'w', encoding='utf-8') as file:
            for _ in _links:
                file.write('\n')
                file.write(_.strip())
        return _links
    
    def get_product_detail(self):
        links = []
        with open('data/links.txt', 'r', encoding='utf-8') as file:
            for f in file.readlines():
                links.append(f.strip())
        links.pop(0)

        with self.console.status('Ürün detayları alınıyor') as progress:
            for link in range(0, len(links)):
                __link = links[random.randint(0, len(links) - 1)]
                req = self.bypass.get(URL=__link)
                html = BeautifulSoup(req, 'lxml')
                
                title = self.get_title(html)
                seller = self.get_seller(html)
                price = self.get_price(html)
                
                try:
                    other_seller = html.findAll('div', {'class': 'pr-mc-w gnr-cnt-br'})[0]
                    other_seller_name = self.get_other_seller_name(other_seller)
                    other_seller_price = self.get_other_seller_price(other_seller)
                    thirt_price = self.get_other_seller_price(html.findAll('div', {'class': 'pr-mc-w gnr-cnt-br'})[1])
                    A = int(re.sub(r',(.*)','',price))
                    B = int(other_seller_price.replace(' TL', ''))

                    percent = ((B - A) / B) * 100
                except:
                    percent = "none"
                    continue

                
                if percent >= 25:
                    message = f""" 
                    \n<b>TRENDYOL FIRSAT ÜRÜNÜ</b>\n\n\n<a href="{__link}">{title}</a>\n\n<b>İlk Satıcı:</b>{seller}\n<b>İlk Satıcı Fiyatı:</b>{price}\n<b>İkinci Satıcı:</b>{other_seller_name}\n<b>İkinci Satıcı Fiyat:</b>{other_seller_price}\n<b>Üçüncü Satıcı Fiyat:</b>{thirt_price}\n<b>Yüzdelik Fark:</b>{"%.2f" % abs(percent)}\n\n
                    """
                    logControl = logger.log_control(query=title, filename='productLog')

                    if logControl == False:
                        self.telegram.sendMessage(message=message)
                        self.telegram_my.sendMessage(message=message)
                logger.create_log(link, 'productLog')   
            self.console.log('Ürün detayları alındı.')
    
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
            #price = float(re.sub(r',(.*)','',soup.find('span', {'class': 'prc-dsc'}).text))
            price = soup.find('span', {'class': 'prc-dsc'}).text
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
            #other_seller_price = float(soup.find('span', {'class': 'prc-dsc'}).text.replace(' TL', ''))
            other_seller_price = soup.find('span', {'class': 'prc-dsc'}).text
        except:
            other_seller_price = "null"
        
        return other_seller_price