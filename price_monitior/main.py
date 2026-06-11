# main.py
import time
import logging
from config import TARGET_PRODUCTS, HEADERS
from database import init_db, log_price_data
from scraper import scrape_product

def run_pipeline():
    logging.info("Starting Competitor Price Monitoring Pipeline...")
    
    # Ensure database tables exist
    init_db()
    
    for product in TARGET_PRODUCTS:
        logging.info(f"Processing target: {product['name']}")
        
        # Execute scraping task
        data = scrape_product(product, HEADERS)
        
        if data:
            # Persist data to SQLite
            log_price_data(
                name=data["name"],
                url=data["url"],
                price=data["price"],
                is_in_stock=data["is_in_stock"]
            )
            logging.info(f"Successfully logged {data['name']}: £{data['price']} (In Stock: {data['is_in_stock']})")
        
        # Polite crawling rule: pause between requests to avoid getting banned
        time.sleep(2)
        
    logging.info("Pipeline execution complete.")

if __name__ == "__main__":
    run_pipeline()