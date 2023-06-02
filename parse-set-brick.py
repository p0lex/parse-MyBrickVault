import json
from bs4 import BeautifulSoup as soup
import psycopg2

with open(r"C:\Users\unnamed\Desktop\1.html") as f:
    html = f.read()

# html parsing
page1_soup = soup(html, 'html.parser')

# grabbing data
containers = page1_soup.findAll('div', {'class': 'part-text'})

# Make the connection to PostgresSQL
conn = psycopg2.connect(database='MyBrickVault', user='postgres', password='123', port=5433)
cursor = conn.cursor()

# Insert data into table
bricks_list = []
for container in containers:
    list_ = (container.text.strip()).split('x')
    cnt = list_[0].strip()
    id = list_[1].strip()
    bricks_list.append({'id': id, 'quantity': cnt})

query = "UPDATE sets SET parts = %s WHERE id = %s;"
data = (json.dumps(bricks_list), "60057")
cursor.execute(query, data)

# Commit the transaction
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
