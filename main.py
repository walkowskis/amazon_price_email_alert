import json
import smtplib
from email.message import EmailMessage
import time
import random
import captcha_solver
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    with open('data.json') as file:
        data = json.load(file)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                      'Safari/537.36', 'Accept-Language': 'gzip, deflate'}

    for url, threshold_price in data.items():
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        if soup.select_one("#productTitle") is not None:
            for i in range(3):
                try:
                    product_title = soup.select_one("#productTitle").get_text(strip=True)
                    price_whole = soup.select_one('.a-price-whole').get_text(strip=True)
                    price_fraction = soup.select_one('.a-price-fraction').get_text(strip=True)
                    price = price_whole + price_fraction
                    break
                except AttributeError as e:
                    print(e)

        elif "Wypróbuj inny obraz" in soup.get_text():
            item_data = captcha_solver.price(url, threshold_price)
            price = item_data[0]
            product_title = item_data[1]
        else:
            price = str(threshold_price).replace('.', ',')
            product_title = 'None'

        if page.status_code == 200:
            if float(price.replace(',', '.')) < threshold_price:
                sender_email = ""
                receiver_email = [""]
                password = ""
                message = f'The price of the monitored product {product_title} has decreased below {threshold_price} PLN, and is now {price} PLN.\n{url} '
                msg = EmailMessage()
                msg.set_content(message)
                msg['Subject'] = f'Amazon Price Alert: {product_title}'
                msg['From'] = sender_email
                msg['To'] = receiver_email
                port = 587  # SMTP Server port

                with smtplib.SMTP("", port) as server:
                    server.login(sender_email, password)
                    server.send_message(msg)
                print("The email has been sent.")
            else:
                print(f"The price of the {product_title} is too high.")
        wait_time = random.uniform(60, 120)
        time.sleep(wait_time)
