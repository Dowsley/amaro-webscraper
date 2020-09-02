from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json

def get_product_urls(driver):
    """Returns a list of links of every product on the page
    """
    catalog_grid = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'app__catalog__grid'))
    )
    products = catalog_grid.find_elements_by_class_name('app__product-box')
    return map(
        lambda p: p.find_element_by_tag_name('a').get_attribute("href"),
        products
    )

def get_review_data(driver):
    driver.execute_script("window.scrollTo(0, 1500)") 
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'yotpo-star-distribution-content'))
    )
    stars = container.find_elements_by_class_name(
        'review-stars'
    )

    # Get reviews from 1,2,3 stars
    for i in (2, 3, 4):
        stars[i].click()
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'yotpo-reviews'))
        )
        reviews = container.find_elements_by_class_name('yotpo-review')
        for r in reviews:
            print(r.find_element_by_class_name('content-title').text)
        break


# -- MAIN -- #
URL = 'https://amaro.com/moda-feminina/roupas-essenciais'

driver = webdriver.Chrome()
driver.get(URL)

product_urls = get_product_urls(driver)
for url in product_urls:
    driver.get(url)
    data = get_review_data(driver)
    print(data)

driver.close()