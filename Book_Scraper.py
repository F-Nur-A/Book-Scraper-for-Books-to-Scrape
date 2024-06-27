from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib.parse import urljoin
import re
import shelve

class WebScrapper():

    def __init__(self,db_ismi):
        self.db_ismi=db_ismi 
        self.categories={}

    def get_soup(self,webpage="http://books.toscrape.com/index.html"):
        self.main_url= webpage
        open = urllib2.urlopen(self.main_url)
        contents = open.read()
        self.soup = BeautifulSoup(contents)
        self.veriler=self.soup.prettify()
        return self.soup

    def get_categories(self):
        self.get_soup()
        navlistler = self.soup.find_all(class_='nav nav-list')
        a_listesi = navlistler[0].findChildren("a" , recursive=True)

        for indeks in range(1,len(a_listesi)):
            categories_link = a_listesi[indeks].get('href')
            link_join = urljoin(self.main_url, categories_link)

            kategori=a_listesi[indeks].string.strip()
            self.categories[kategori]=link_join
        return self.categories
    
    def get_prices_stars(self,soup,link):
        self.soup2=soup
        self.link=link
        self.get_prices_stars_liste=[]
        kitap_verileri = self.soup2.find_all(class_='product_pod')
        
        for indeks in range(len(kitap_verileri)):
            h3= kitap_verileri[indeks].find_all("h3")
            h3_a=h3[0].findChildren("a" , recursive=True)
            #kitap ismi alma
            title = h3_a[0].get('title')
            #kitap linki alma
            href = h3_a[0].get('href')
            sil=href.lstrip("../../..")
            yeni= "catalogue/"+sil
            href_birlesmis = urljoin(self.link, yeni)
            #fiyat bilgisi alma
            price_color=kitap_verileri[indeks].findChildren(class_='price_color' , recursive=True)
            fiyat=price_color[0].string.strip()
            sil_fiyat=fiyat.lstrip("£")
            #rating bilgisi alma
            rating=self.soup2.find_all(class_ = re.compile("star-rating"))
            yildiz=rating[indeks].get('class')
            yeni_cumle= " ".join(yildiz)
            if yeni_cumle== "star-rating One":
                rating_yildiz="1"
            if yeni_cumle== "star-rating Two":
                rating_yildiz="2"
            if yeni_cumle== "star-rating Three":
                rating_yildiz="3"
            if yeni_cumle== "star-rating Four":
                rating_yildiz="4"
            if yeni_cumle== "star-rating Five":
                rating_yildiz="5"

            self.degerler = {
                "Name: " : str(title),
                "Rating: ": int(rating_yildiz),
                "Price: ": float(sil_fiyat),
                "URL: ":str(href_birlesmis)}
            self.get_prices_stars_liste.append(self.degerler)
        return self.get_prices_stars_liste
    
    def create_db(self,db_ismi):
        self.db_ismi=db_ismi
        self.db_dosya=shelve.open(self.db_ismi,writeback=True, flag='c')

    def close_db(self):
        self.db_dosya.close()

    def parse(self):
        self.get_categories()
        self.create_db(self.db_ismi)
        for key in self.categories.keys():
            linkler_son=self.categories[key]
            kategori_linkleri=self.get_soup(linkler_son)
            self.get_prices_stars(kategori_linkleri,"http://books.toscrape.com/index.html")
            self.db_dosya[key]= self.get_prices_stars_liste
        self.close_db()
