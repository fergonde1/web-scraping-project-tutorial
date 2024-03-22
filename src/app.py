import requests
import time
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Seleccionar el recurso a descargar
resource_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

# Petición para descargar el fichero de Internet
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
request = requests.get(resource_url, headers = headers)
time.sleep(10)
resource = request.text

soup = BeautifulSoup(resource,"html.parser")
soup

tables = soup.find_all("table")
tables

for index, table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
        break

# Create a DataFrame
tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({
            "Date": Date,
            "Revenue": Revenue
        }, index = [0])], ignore_index = True)

tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]

connection = sqlite3.connect("Tesla_revenue.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE TESLA 
               (Date TEXT, 
               Revenue INT)""")

tesla_revenue.to_sql('TESLA', connection, if_exists='append', index=False)
connection.commit()

cursor.execute('SELECT * FROM TESLA LIMIT 5')
filas = cursor.fetchall()
for fila in filas:
    print(fila)

connection.close()

tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])
tesla_revenue = tesla_revenue.sort_values(by='Date')

plt.figure(figsize=(10, 6))
plt.plot(tesla_revenue['Date'], tesla_revenue['Revenue'], marker='o', linestyle='-')
plt.show()

plt.figure(figsize=(8, 6))
plt.hist(tesla_revenue['Revenue'], bins=20, color='skyblue', edgecolor='black')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(tesla_revenue['Date'], tesla_revenue['Revenue'], color='green', alpha=0.5)
plt.show()