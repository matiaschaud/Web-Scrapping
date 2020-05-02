#---------------------------------------- Importa las librerias a utilizar ----------------------------------------#
import requests
from bs4 import BeautifulSoup
import re
# from selenium import webdriver
import time
# from datetime import datetime

#---------------------------------------- Funciones complementarias ----------------------------------------#
def archivo_url(texto,formato_archivo):
    """Función para despejar el nombre de un archivo en una url."""
    patron = re.compile("." + formato_archivo.lower())
    patron2 = re.compile("/")

    s2 = patron2.split(texto)

    for txt in s2:
        s = patron.search(txt)
        if type(s) == re.Match:
            txt2 = patron.split(txt)
            return(txt2[0])


#---------------------------------------- Obtiene los links a scrappear ----------------------------------------#
def obtiene_links():
    while True:
        try:
            r = requests.get("https://supermercado.carrefour.com.ar/")
            c = r.content
            soup = BeautifulSoup(c,"html.parser",multi_valued_attributes=None)
            ol_primary = soup.find("ol",{"class":"nav-primary"})
            h2 = ol_primary.findAll("h2")
            break
        except:
            time.sleep(1)
            pass

    links = {}
    for categoria in h2:
        try:
            link = categoria.find("a")
            links[archivo_url(link.get("href"),"html")] = link.get("href")
        except:
            pass
    
    return links

class element_is_displayed(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator):
    self.locator = locator

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if element.is_displayed():
        return element
    else:
        return False