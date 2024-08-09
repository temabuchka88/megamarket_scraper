from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = '/usr/bin/chromium'

service = Service('/usr/local/bin/chromedriver')

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://megamarket.ru/catalog/?q=%D0%B8%D0%B3%D1%80%D0%BE%D0%B2%D0%BE%D0%B5%20%D0%BA%D1%80%D0%B5%D1%81%D0%BB%D0%BE")

driver.implicitly_wait(0.2)

catalog_container = driver.find_element(By.CSS_SELECTOR, 'div.catalog-items-list')

product_elements = catalog_container.find_elements(By.CSS_SELECTOR, '[data-test="product-item"]')

selected_products = product_elements[:20]

product_data = []

product_links = []

# Знаю, что правильно бы было достать ссылку на фотку из карточки товара, но оттуда никак не получилось почему то ;)
product_image_urls = []

for product in selected_products:
    try:
        product_link_element = product.find_element(By.TAG_NAME, 'a')
        product_link = product_link_element.get_attribute('href')
        product_links.append(product_link)

        product_image_element = driver.find_element(By.CSS_SELECTOR, 'img[data-test="product-image"]')
        product_image_url = product_image_element.get_attribute('src')
        product_image_urls.append(product_image_url)
    except Exception as e:
        print(f'Ошибка при получении URL: {e}')
        

for i, product_link in enumerate(product_links):
    driver.get(product_link)

    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]').text

        product_price = driver.find_element(By.CSS_SELECTOR, 'span.sales-block-offer-price__price-final').text

        product_price = product_price.replace('₽', '').strip()

        product_image_url = product_image_urls[i]

        try:
            product_description = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[itemprop="description"]'))
            ).text.strip()

        except TimeoutException:
            product_description = 'Описание отсутствует.'
        
        product_data.append({
            'Product URL': product_link,
            'Product Name': product_name,
            'Price (RUB)': product_price,
            'Image URL': product_image_url,
            'Description': product_description,
        })

    except Exception as e:
        print(f'Произошла ошибка {e}')

dataframe = pd.DataFrame(product_data)

dataframe.to_excel('/app/goods.xlsx', index=False, engine='openpyxl')

driver.quit()
