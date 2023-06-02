from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import psycopg2

my_url = 'https://legouniverse.fandom.com/wiki/List_of_Bricks'
uClient = uReq(my_url)
page1_html = uClient.read()
uClient.close()

# html parsing
page1_soup = soup(page1_html, 'html.parser')

# grabing data
containers = page1_soup.findAll('tr')

# Make the connection to PostgreSQL
conn = psycopg2.connect(database='MyBrickVault', user='postgres', password='123', port=5433)
cursor = conn.cursor()

# Insert data into table
for container in containers:
    code = container.find_all_next('td')[2].text.strip()
    name = container.find_all_next('td')[1].text.strip()
    query = "INSERT INTO bricks (code, name) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
    data = (code, name)
    cursor.execute(query, data)

# Commit the transaction
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
