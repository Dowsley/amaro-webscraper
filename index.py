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
    catalog_grid = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'app__grid'))
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
        try:
            star.click()
        except:
            wait_and_cancel_popup(driver)
            star.click()
        sleep(1)
        container = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'yotpo-reviews'))
        )
        reviews = container.find_elements(By.XPATH, "//div[@class='yotpo-review-wrapper']/div[@class='content-review']")
        #TODO verificar se existe comentarios
        #for r in reviews:
        #    print(r.text)


def function(driver, i):
    try:
        return get_star(driver,i)
    except:
        wait_and_cancel_popup(driver)
        return get_star(driver,i)


def get_star(driver,i):
    i = '"'+str(i)+'"'
    WebDriverWait(driver,20).until(
        EC.presence_of_element_located(
            (By.XPATH,
            f"//div[@class='yotpo-distibutions-stars']/span[@data-score-distribution={i}]")
        )
    )
    star = driver.find_element(
        *(By.XPATH,
        f"//div[@class='yotpo-distibutions-stars']/span[@data-score-distribution={i}]")
    )
    return star


def wait_and_cancel_popup(driver):
    try:
        WebDriverWait(driver,20).until(
            EC.presence_of_element_located(
                (By.XPATH, 
                "//iframe[@title='Modal Message']")
            )
        )
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except:
        print("Elemento não encontrado.")


# -- MAIN -- #
URL = 'https://amaro.com/moda-feminina/roupas-essenciais'

driver = Chrome(ChromeDriverManager().install())
driver.get(URL)
wait_and_cancel_popup(driver)
product_urls = get_product_urls(driver)
counter = 0
for url in product_urls:
    counter = counter + 1
    driver.get(url)
    data = get_review_data(driver)
    print(counter)

driver.close()