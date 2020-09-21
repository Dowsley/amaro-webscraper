from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import json

# --------------- #
# --- CLASSES --- #
# --------------- #
class Product:
    def __init__(self, reviews, has_fitfinder, sizes,
                total_reviews, trim, rating):
        self.reviews = reviews
        self.has_fitfinder = has_fitfinder
        self.sizes = sizes
        self.total_reviews = total_reviews
        self.trim = trim
        self.rating = rating
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Comment:
    def __init__(self, name, rating, trim, title, description):
        self.name = name
        self.rating = rating
        self.trim = trim
        self.title = title
        self.description = description
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


# ----------------- #
# --- FUNCTIONS --- #
# ----------------- #
def scroll_down_page(driver, times):
    """ Scrolls down page by pressing the down key N times
    """
    body = driver.find_element_by_css_selector('body')
    for i in range(times):
        body.send_keys(Keys.PAGE_DOWN)
        sleep(0.01)


def get_products(driver):
    """Returns a list of URLS of every product on the page
    """
    catalog_grid = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'app__grid'))
    )
    products = catalog_grid.find_elements_by_class_name('app__product-box')
    return list(
        map(
            lambda p: p.find_element_by_tag_name('a').get_attribute("href"),
            products
        )
    )


def get_star(driver, i):
    """Returns the clickable element of "i" stars
    """
    try:
        return get_star_util(driver,i)
    except Exception as e:
        print(e)
        wait_and_cancel_popup(driver)
        return get_star_util(driver,i)


def get_star_util(driver,i):
    i = f'"{str(i)}"'
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
    except Exception as e:
        print(e)
        print("[[Elemento não encontrado.]]")


def parse_product(driver):
    """Parses the product data and its reviews and returns
    them encapsulated within a class instance
    """
    for i in (1, 2, 3):
        # STEP 1: Click star and load reviews
        print(f"<< Estrela: {i} >>")
        star = get_star(driver, i)
        try:
            star.click()
        except Exception as e:
            print(e)
            wait_and_cancel_popup(driver)
            star.click()
        sleep(1)
        
        page = 1
        while True:
            print(f"<< Página: {page}")
            # STEP 2: DEAL WITH THE REVIEWS (AND PARSE THEM)
            container = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'yotpo-reviews'))
            )
            reviews = container.find_elements_by_class_name(
                'yotpo-review'
            )
            print(len(reviews))

            # STEP 3: GO TO THE NEXT PAGE (OR END FUNCTION IF THATS ALL)
            button = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 
                    'a[rel="next"]')
                )
            )
            if not button.get_attribute("href"):
                break
            try:
                button.click()
            except Exception as e:
                print(e)
                wait_and_cancel_popup(driver)
            page += 1


def serialize_product(data):
    pass

# -- MAIN -- #
URL = 'https://amaro.com/moda-feminina/roupas-essenciais'

driver = Chrome(ChromeDriverManager().install())
driver.get(URL)

wait_and_cancel_popup(driver)
scroll_down_page(driver, 500)
products = get_products(driver)
print(f"<< Total de produtos: {len(products)} >>")

for url in products:
    print(f"<< Produto: {url} >>")
    driver.get(url)
    data = parse_product(driver)
    serialize_product(data)

driver.close()