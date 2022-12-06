import time
from modules import scraper
from  modules import get_data
from rich.console import Console

console = Console()

console.print(""" 
\nTrendyol Ürün Fiyat Takip Uygulamasına Hoş Geldiniz
\n
\nYazar: Emirhan KARADENİZ
\nVersion: 2022.2
\nGithub: https://github.com/karadenizemirr
\n
\n[red]Uyarı: Lütfen [yellow]data[/yellow] klasörü içerisinde bulunan [yellow]category.txt[/yellow] dosyasını silmeyin.[/red]

""", style="bold purple", justify="center")

def main():
    # Open Category Data
    categories = []

    with open('data/category.txt', 'r', encoding='utf-8') as file:
        for f in file.readlines():
            categories.append(f.strip())
    
    get_data.GetData(categories=categories).run()

if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)