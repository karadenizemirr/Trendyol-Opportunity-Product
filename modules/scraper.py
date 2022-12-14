import requests
import queue
import re
from rich.console import Console
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from modules import bypass
from decimal import Decimal
from modules.logger import logger
from modules import telegram

class TrendyolScraper:
    def __init__(self):
        self.console = Console()
        self.Q = queue.Queue()
        self.session = requests.Session()
        self.ua = UserAgent(browsers=['edge', 'chrome'])
        self.bypass = bypass.Bypass()
        self.headers = {
            "User-Agent": self.ua.random
        }
        self.base_url = "https://www.trendyol.com"
        self.telegram = telegram.Telegram(token="5750542194:AAHUctF5ImPnjjOmobKfh7pUBsd_5ZHobG8", user_id="744777387")
        self.telegram_my = telegram.Telegram(token="5901890521:AAG_9fjlySpTIQmJD-pb5wjYXC8hU-jjVvA", user_id="5669620760")

    def get_page_number(self, link=None):
        counter = 1
        category_pagination_link = []

        with self.console.status("[cyan]Sayfa numaralar─▒ ve kategoriler tespit ediliyor..[/cyan]") as status:
            while True:
                _link = f"{link}&pi={counter}"
                req = self.bypass.get(URL=_link, allow_redirect=True)
                html = BeautifulSoup(req, 'lxml').findAll(
                    'div', {'class': 'prdct-cntnr-wrppr'})

                if len(html) < 1:
                    if counter >= 150:
                        break
                    break
                counter += 1
                category_pagination_link.append(_link)

            self.Q.put(category_pagination_link)

    def create_product_link(self, category_link=None):
        product_link = []

        req = self.session.get(category_link, headers=self.headers)
        html = BeautifulSoup(req.text, 'html.parser')
        all_a = html.findAll(
            'div', {'class': 'p-card-chldrn-cntnr card-border'})

        for a in all_a:
            product_link.append(f"{self.base_url}{a.a['href']}")

        self.Q.put(product_link)

    def get_product(self, product_link=None):
        req = self.bypass.get(URL=product_link)
        html = BeautifulSoup(req, 'html.parser')

        title = self.get_title(html)
        first_seller, first_seller_price = self.get_first_seller(html)
        second_seller, second_seller_price = self.get_other_seller(html, 0)
        thirt_seller, thiry_seller_price = self.get_other_seller(html, 1)
        percent_difference = self.percent_diffrence(A=first_seller_price, B=second_seller_price)

        self.Q.put({
            "├ťr├╝n Ad─▒": title,
            "─░lk Sat─▒c─▒": first_seller,
            "─░lk Sat─▒c─▒ Fiyat─▒": first_seller_price,
            "─░kinci Sat─▒c─▒": second_seller,
            "─░kinci Sat─▒c─▒ Fiyat─▒": second_seller_price,
            "├ť├ž├╝nc├╝ Sat─▒c─▒ Fiyat─▒": thiry_seller_price,
            "Y├╝zdelik Fark": "%.2f" % (percent_difference),
            "├ťr├╝n Linki": product_link
        })
        
        if (percent_difference >= 25) & (logger.log_control(query=product_link, filename='productLog') == False):
            # Create Message
            message = f"""\n\n<b>Trendyol F─▒rsat ├ťr├╝n├╝</b>\n\
                \n<a href="{product_link}">{title}</a>\n\n<b>─░lk Sat─▒c─▒:</b>{first_seller}\n<b>─░lk Sat─▒c─▒ Fiyat─▒:</b>{first_seller_price}\n<b>─░kinci Sat─▒c─▒:</b>{second_seller}\n<b>─░kinci Sat─▒c─▒ Fiyat─▒:</b>{second_seller_price}\n<b>├ť├ž├╝nc├╝ Sat─▒c─▒ Fiyat─▒:</b>{thiry_seller_price}\n<b>Y├╝zdelik Fark:</b>{"%.2f" % (percent_difference)}
                """
            
            self.telegram.sendMessage(message=message)
            self.telegram_my.sendMessage(message=message)
        else:
            pass

        logger.create_log(data=product_link, filename='productLog')

    def get_title(self, html):
        try:
            title = html.find('h1', {'class': 'pr-new-br'}).text
        except:
            title = "null"

        return title

    def get_first_seller(self, html):
        try:
            first_seller = html.find('a', {'class': 'merchant-text'}).text
            first_seller_price = float(int(re.sub(r',[0-9]* TL', "", html.find('span', {'class': 'prc-dsc'}).text)))
        except:
            first_seller = 'null'
            first_seller_price = 'null'

        return first_seller, first_seller_price

    def get_other_seller(self, html, seller_number):
        if seller_number > 4:
            return "null", "null"

        try:
            container = html.findAll(
                'div', {'class': 'pr-mc-w gnr-cnt-br'})[seller_number]
            seller = container.find('div', {'class': 'seller-container'}).text
            price = float(int(re.sub(r',[0-9]* TL', "", container.find('span', {'class': 'prc-dsc'}).text).replace(".", "")))
        except:
            seller = "null"
            price = "null"

        return seller, price
    
    def get_rate(self, html):
        try:
            rate = html.find('div', {'class': 'pr-rnr-sm-p'}).text
        except:
            rate = "null"

        return rate

    def flatten(self, nasted_list):
        """
        input: nasted_list - this contain any number of nested lists.
        ------------------------
        output: list_of_lists - one list contain all the items.
        """

        list_of_lists = []
        for item in nasted_list:
            list_of_lists.extend(item)
        return list_of_lists

    def percent_diffrence(self,A,B):
        try:
            return abs((A - B) / B) * 100
        except:
            return 0.00