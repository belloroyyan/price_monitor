TARGET_PRODUCTS = [
    {
        "name" : "A Light In The Attic",
        "url": "https://books.toscrape.com",
        "selector_price": "p.price_color",
        "selector_stock": "p.instock.availability"
    },
    {
        "name": "Tipping the Velvet",
        "url": "https://books.toscrape.com",
        "selector_price": "p.price_color",
        "selector_stock": "p.instock.availability"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}