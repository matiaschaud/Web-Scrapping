from selenium import webdriver
import time
from bs4 import BeautifulSoup

# browser = webdriver.PhantomJS()
browser = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
browser.get("https://supermercado.carrefour.com.ar/almacen.html")

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# click radio button
python_button = browser.find_elements_by_xpath("/html/body/div[1]/div[1]/div[1]/div[8]/div/div/div[4]/a")[0]
python_button.click()

page = BeautifulSoup(browser.page_source,"html.parser")

links = page.findAll("a")

for link in links:

    print(link)

# browser.close()