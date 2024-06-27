from Book_Scraper  import WebScrapper
import shelve

db_name="kitaplar.db"
ws= WebScrapper(db_name)


link= "http://books.toscrape.com/index.html"
gs=ws.get_soup(link)
print(gs)
gc=ws.get_categories()
print(gc)
gps=ws.get_prices_stars(ws.get_soup("https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"),link)
print(gps)
ws.create_db("kitaplar.db")
ws.parse()
with shelve.open(db_name, 'r') as db:
    for keys, values in db.items():
        print(keys, ':', values)
