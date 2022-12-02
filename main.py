import time
import tkinter as tk
from tkinter import filedialog
from modules import scraper
from rich.console import Console

console = Console()
root = tk.Tk()
root.withdraw()
sc = scraper.Scraper()

console.print(""" 
    \n[purple]Trendyol Fırsat Ürün Bulucu[/purple]
    \n\n
    \nYazar: Emirhan KARADENİZ
    \nVersion: 2022.1
    \nGithub: https://github.com/karadenizemirr
    \n\n
    [yellow]Uyarı: Yazılımı kullanabilmek için kategori linklerinin olması gerekir.[yellow]
""", style="bold cyan", justify="center")

def main():
    console.print("\nLütfen kategori .txt dosyasını seçiniz.", style="bold red")
    time.sleep(2)
    filepath = filedialog.askopenfilename(title="Kategori Dosyası Seçiniz.")
    category_link = []

    with open(filepath, 'r', encoding="utf-8") as file:
        for f in file.readlines():
            category_link.append(f.strip())
    
    # Create Product Link
    sc.get_product_link(links=category_link)
    # Get Operations
    sc.get_product_detail()
    

if __name__=='__main__':
    while True:
        main()
        time.sleep(60 * 5)