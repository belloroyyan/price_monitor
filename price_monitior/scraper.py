# scraper.py
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_product(product_dict, headers):
    try:
        response = requests.get(product_dict["url"], headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Find the HTML elements using the clean CSS selectors
        price_element = soup.select_one(product_dict["selector_price"])
        stock_element = soup.select_one(product_dict["selector_stock"])
        
        # 2. Add an explicit defensive check to make sure the elements actually exist
        if not price_element or not stock_element:
            logging.error(f"Selectors not found on page for {product_dict['name']}")
            return None
            
        # 3. Extract the inner text safely using .get_text()
        raw_price = price_element.get_text()
        raw_stock = stock_element.get_text()
        
        # Clean Data
        cleaned_price = float(''.join(c for c in raw_price if c.isdigit() or c == '.'))
        is_in_stock = "In stock" in raw_stock
        
        return {
            "name": product_dict["name"],
            "url": product_dict["url"],
            "price": cleaned_price,
            "is_in_stock": is_in_stock
        }
        
    except Exception as e:
        logging.error(f"Failed to scrape {product_dict['name']}: {str(e)}")
        return None
