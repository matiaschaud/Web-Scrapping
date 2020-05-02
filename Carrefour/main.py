
#---------------------------------------- Importa las librerias a utilizar ----------------------------------------#
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from paquetes.utils import *
import pandas as pd

# Obtenemos los distintos links a scrappear en formato de diccionario
# links = obtiene_links()

links = {
# 'bebidas': 'https://supermercado.carrefour.com.ar/bebidas.html', 
# 'almacen': 'https://supermercado.carrefour.com.ar/almacen.html', 
# 'desayuno-y-merienda': 'https://supermercado.carrefour.com.ar/desayuno-y-merienda.html', 
# 'golosinas-y-snacks': 'https://supermercado.carrefour.com.ar/golosinas-y-snacks.html', 
# 'lacteos-y-productos-frescos': 'https://supermercado.carrefour.com.ar/lacteos-y-productos-frescos.html', 
# 'congelados': 'https://supermercado.carrefour.com.ar/congelados.html', 
# 'carnes-y-pescados': 'https://supermercado.carrefour.com.ar/carnes-y-pescados.html', 
# 'quesos-y-fiambres': 'https://supermercado.carrefour.com.ar/quesos-y-fiambres.html',
# 'frutas-y-verduras': 'https://supermercado.carrefour.com.ar/frutas-y-verduras.html', 
'panaderia': 'https://supermercado.carrefour.com.ar/panaderia.html'#, 
# 'limpieza': 'https://supermercado.carrefour.com.ar/limpieza.html', 
# 'perfumeria': 'https://supermercado.carrefour.com.ar/perfumeria.html', 
# 'mundo-bebe': 'https://supermercado.carrefour.com.ar/mundo-bebe.html', 
# 'mascotas': 'https://supermercado.carrefour.com.ar/mascotas.html', 
# 'hogar-y-bazar': 'https://supermercado.carrefour.com.ar/hogar-y-bazar.html'
}


#---------------------------------------- Carga todos los items de la pag ----------------------------------------#


SCROLL_PAUSE_TIME = 0.5
DRIVER_DIR = "C:\\chromedriver_win32\\chromedriver.exe"
OUTPUT_DIR = "C:\\Users\\Matias\\Documents\\Matias\\Repositorios\\Web Scrapping\\Carrefour\\output"

for seccion,link in links.items():
    # browser = webdriver.PhantomJS()
    browser = webdriver.Chrome(DRIVER_DIR)
    browser.get(link)

    while True:
        soup = BeautifulSoup(browser.page_source,"html.parser",multi_valued_attributes=None)
        all = soup.findAll("div", {"class": "block-body"})
        try:
            all[0]
        except:
            break
        
        # Si no se rompe la ejecución, cierra y vuelve a abrir.
        browser.close()
        time.sleep(1)
        browser = webdriver.Chrome(DRIVER_DIR)
        browser.get(link)

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

    # Los botones podrían tener distinto xPath, estos son los 3 más comunes.
    wait = WebDriverWait(browser, 5)
    try:
        python_button_pos3 = wait.until(element_is_displayed((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[8]/div/div/div[4]/a")))
    except:                                                                  
        try:                                                                
            python_button_pos3 = wait.until(element_is_displayed((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[8]/div/div/div[3]/a[2]")))
        except:
            try:                                                                
                python_button_pos3 = wait.until(element_is_displayed((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[8]/div/div/div[2]/a")))
            except:
                print("No coincide con ningún botón")
                exit()
    
    intentos = 5
    t = 1.5
    contador = 0
        # click button "VER MÁS PRODUCTOS"
    while True:
        if python_button_pos3.is_displayed():
            browser.execute_script("arguments[0].click();", python_button_pos3)
            contador = 0
        else:
            contador += 1
            time.sleep(t)
        
        if contador == intentos:
            break


#---------------------------------------- Código scrap de la página cargada ----------------------------------------#

    soup = BeautifulSoup(browser.page_source,"html.parser",multi_valued_attributes=None)
    all = soup.findAll("div", {"class": "col s12 product-card product-card-food"})

    l=[]
    for item in all:
        p={}
        info_producto = item.find("div",{"class":"producto-info"})
        p['ruta_categoria'] = " ".join(info_producto['data-categorytext'].split())
        p['precio_bruto'] = info_producto['data-price'].replace(",","").replace(".",",")
        if item.find("div",{"class":"batches"}) is not None:
            p['etiqueta_png'] = archivo_url(item.find("div",{"class":"batches"})['style'],"png")
        p['precio_medida'],p['medida'] = item.find("div",{"class":"precio-medida"}).text.strip().split('x')
        p['precio_medida'] = p['precio_medida'].replace("($","").strip().replace(".","")
        p['medida'] = p['medida'].replace(".)","").strip()
        try:
            p['oferta'] = " ".join(item.find("p",{"class","offer"}).text.split())
        except:
            p['oferta'] = None
        try:
            p['precio_oferta'] = item.find("span",{"class","precio-numero"}).text.strip().replace("$","")
        except:
            p['precio_oferta'] = None
        try:
            p['texto_oferta'] = " ".join(item.find("span",{"class","precio-texto"}).text.strip.split())
        except:
            p['texto_oferta'] = None
        p['marca'] = " ".join(item.find("p",{"class","brand truncate"}).text.strip().split())
        p['producto'] = " ".join(item.find("p",{"class":"title title-food truncate"}).text.strip().split())
        l.append(p)
            
    browser.close()

#------------------------------ Guarda el archivo en formato CSV -----------------------------#
# Sería muy bueno guardarlo en una bbdd sqlite.
    df = pd.DataFrame(l)
    today = str(datetime.date(datetime.now()))
    df['fecha'] = today
    df['seccion'] = seccion

    df = df.drop_duplicates()

    df.to_csv(OUTPUT_DIR + "\\" + today.replace("-","") + "_carrefour_" + seccion + ".csv",encoding="utf-8")


