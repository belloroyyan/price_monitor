# main.py
import time
import logging
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import TARGET_PRODUCTS, HEADERS, SMTP_PORT, SMTP_SERVER
from database import init_db, log_price_data
from scraper import scrape_product

def send_email_alert(product, current, target):
    sender_pass = os.environ.get("EMAIL_PASS")
    sender_email = os.environ.get("EMAIL_USER")
    receiver_email = os.environ.get("EMAIL_RECEIVER")

    if not sender_email or not sender_pass or not receiver_email:
        print("Email params not complete. Skipping alerts.")
        return
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f"Price Drop Alert: {product}"

    body = f"""
        The price monitoring tool has detected an active shift in prices!

        Product: {product}
        Current Price: £{current}
        Your Target Alert Threshold: £{target}
        
        Please log in to your dashboard to review historical analysis.
"""
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_pass)
        server.send_message(msg)
        server.quit()
        logging.info(f"📩 Price alert successfully dispatched to {receiver_email}!")
    except Exception as e:
        logging.error(f"Failed to transmit automated alert notification: {str(e)}")


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
            if data["price"] < product["threshold"]:
                logging.info(f"🔥 Price drop detected for {data['name']}! Initiating alert...")
                send_email_alert(data["name"], data["price"], product["threshold"])
        # Polite crawling rule: pause between requests to avoid getting banned
        time.sleep(2)
        
    logging.info("Pipeline execution complete.")

if __name__ == "__main__":
    run_pipeline()