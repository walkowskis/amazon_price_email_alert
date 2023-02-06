from amazoncaptcha import AmazonCaptcha
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def price(url, threshold_price):
    webdriver_path = 'chromedriver.exe'
    webdriver_service = Service(webdriver_path)
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=webdriver_service, chrome_options=chrome_options)
    driver.get(url)

    try:
        image = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']/img")
        link = image.get_attribute('src')
        captcha = AmazonCaptcha.fromlink(link)
        solution = captcha.solve()
        driver.find_element(By.ID, "captchacharacters").send_keys(solution)
        driver.find_element(By.ID, "captchacharacters").send_keys(Keys.ENTER)
    except:
        print('captcha issue')

    try:
        price_whole = driver.find_element(By.XPATH, "//span[@class='a-price-whole']").text
        price_fraction = driver.find_element(By.XPATH, "//span[@class='a-price-fraction']").text
        product_title = driver.find_element(By.XPATH, "//span[@id='productTitle']").text
        price = price_whole + price_fraction
    except:
        price = str(threshold_price).replace('.', ',')
        product_title = 'None'
    driver.quit()
    return price, product_title
