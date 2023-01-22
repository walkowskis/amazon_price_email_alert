import smtplib
import time
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    URL = ""  # product page link on amazon.pl
    threshold_price = 999.0  # maximum price of the observed product

    page = requests.get(URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                      'Safari/537.36',
        'Accept-Language': 'gzip, deflate'})

    for i in range(3):
        try:
            soup = BeautifulSoup(page.content, "html.parser")
            product_title = soup.select_one("#productTitle").get_text(strip=True)
            price_whole = soup.select_one('.a-price-whole').get_text(strip=True)
            price_fraction = soup.select_one('.a-price-fraction').get_text(strip=True)
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'get_text'":
                product_title = "Unable to download the product name."
                price_whole = "0"
                price_fraction = "0"
            else:
                raise e
        time.sleep(15)

    price = price_whole + price_fraction

    if page.status_code == 200:
        if float(price.replace(',', '.')) < threshold_price:
            sender_email = ""
            receiver_email = [""]
            password = ""
            message = f'The price of the monitored product {product_title} has decreased below {threshold_price} PLN, and is now {price} PLN.'
            print(message)
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = f'Amazon Price Alert: {product_title}'
            msg['From'] = sender_email
            msg['To'] = receiver_email
            port = 587  # SMTP Server port
            SMTP_server = ""

            with smtplib.SMTP(SMTP_server, port) as server:
                server.login(sender_email, password)
                server.send_message(msg)
            print("The email has been sent.")
        else:
            print("The price is too high.")
