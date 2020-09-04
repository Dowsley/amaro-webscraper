from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import json

def get_product_urls(driver):
    """Returns a list of links of every product on the page
    """
    catalog_grid = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'app__catalog__grid'))
    )
    products = catalog_grid.find_elements_by_class_name('app__product-box')
    return list(map(
        lambda p: p.find_element_by_tag_name('a').get_attribute("href"),
        products
    ))

def get_review_data(driver):
    # Get reviews from 1,2,3 stars
    for i in (1, 2, 3):
        star = function(driver, i)
        star.click()
        sleep(5)
        container = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'yotpo-reviews'))
        )
        reviews = container.find_elements(By.XPATH, "//div[@class='yotpo-review-wrapper']/div[@class='content-review']")
        #TODO verificar se existe comentarios
        for r in reviews:
            print(r.text)


def function(driver, i):
    try:
        WebDriverWait(driver,20).until(
            EC.presence_of_element_clickable(
                (By.XPATH,
                f"//span[@data-score-distribution='{i}' and contains(@class,'review-stars')]")
            )
        )
    except:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    finally:
        star = driver.find_element(
            *(By.XPATH,
            f"//span[@data-score-distribution='{i}' and contains(@class,'review-stars')]")
        )
        return star


# -- MAIN -- #
URL = 'https://amaro.com/moda-feminina/roupas-essenciais'

driver = Chrome(ChromeDriverManager().install())
driver.get(URL)

product_urls = get_product_urls(driver)
for url in product_urls:
    driver.get(url)
    data = get_review_data(driver)
    print(data)

driver.close()