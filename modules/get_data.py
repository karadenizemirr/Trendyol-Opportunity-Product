from modules import scraper
from threading import Thread
from rich.progress import Progress

class GetData(scraper.TrendyolScraper):
    def __init__(self,categories):
        super().__init__()
        self.categories = categories
        self.all_product_link_list = []
        self.all_category_link_list = []
        self.all_product_detail = []
    
    def get_all_category_link(self):
        processes = []

        for category in self.categories:
            processes.append(Thread(target=self.get_page_number, args=(category,)))
        
        for process in processes:
            process.start()
            self.all_category_link_list.append(self.Q.get())
        
        for process in processes:
            process.join()
    
    
    def get_all_product_link(self):
        category_link = self.flatten(self.all_category_link_list)
        processes = []

        with self.console.status('Ürün linkleri alınıyor..') as status:
            for category in category_link:
                processes.append(Thread(target=self.create_product_link, args=(category,)))

            for process in processes:
                process.start()
                self.all_product_link_list.append(self.Q.get())
                
            for process in processes:
                process.join()
    
    def get_data(self):
        product_link = self.flatten(self.all_product_link_list)
        processes = []

        print("\n")
        with Progress() as progress:
            pbar = progress.add_task('Modüller başlatılıyor..', total=len(product_link))

            for product in product_link:
                processes.append(Thread(target=self.create_product_link, args=(product,)))
                progress.update(pbar, advance=1)

        print("\n")
        with Progress() as progress:
            pbar = progress.add_task('Veri alınıyor..', total=len(processes))
            for process in processes:
                process.start()
                self.all_product_detail.append(self.Q.get())
                print(self.Q.get())
                progress.update(pbar, advance=1)
        print("\n")
        with Progress() as progress:
            pbar = progress.add_task('Veri kayıt ediliyor..', total=len(processes))
            for process in processes:
                process.join()
                progress.update(pbar, advance=1)
    
    def run(self):
        self.get_all_category_link()
        self.get_all_product_link()
        self.get_data()