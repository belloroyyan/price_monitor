TARGET_PRODUCTS = [
    {
        "name" : "A Light In The Attic",
        "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "selector_price": "p.price_color",
        "selector_stock": "p.instock.availability",
        "threshold" : 52.00
    },
    {
        "name": "Tipping the Velvet",
        "url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
        "selector_price": "p.price_color",
        "selector_stock": "p.instock.availability",
        "threshold" : 54.00
    },
    {
        "name": "Soumission",
        "url": "https://books.toscrape.com/catalogue/soumission_998/index.html",
        "selector_price": "p.price_color",
        "selector_stock": "p.instock.availability",
        "threshold" : 50.00
    }
]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}