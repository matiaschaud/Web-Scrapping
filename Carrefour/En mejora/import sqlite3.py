import sqlite3

from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect("ws.db") #con = sqlite3.connect(':memory:')
        
        return con
    except Error:

        print(Error)

        
def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("""
    CREATE TABLE IF NOT EXISTS         ws_carrefour(
    ID                   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
    ruta_categoria       TEXT,
    precio               REAL,
    precio_medida        REAL,
    medida               VARCHAR(15),
    oferta               VARCHAR(100),
    precio_oferta        REAL,
    texto_oferta         VARCHAR(100),
    marca                VARCHAR(120),
    producto             VARCHAR(350),
    etiqueta_png         VARCHAR(100),
    fecha                DATE)
    """)

    con.commit()

def inserta_ws_carrefour(con,data):
    cursorObj = con.cursor()

    cursorObj.executemany("INSERT INTO ws_carrefour VALUES(null,?,?,?,?,?,?,?,?,?,?,?)", data)

    con.commit()

con = sql_connection()
sql_table(con)


import pandas as pd

df = pd.read_csv("20200426_carrefour_almacen.csv")
tuples = [x.precio_oferta for x in df.values]
print(tuples[0])

# inserta_ws_carrefour(con,tuples[0])