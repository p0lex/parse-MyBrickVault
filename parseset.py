from bs4 import BeautifulSoup as soup
import psycopg2

with open(r"C:\Users\unnamed\Desktop\LEGO Set 10159-1 City Airport (2004 City _ Airport) _ Rebrickable - Build with LEGO.html") as f:
    html = f.read()

# html parsing
page1_soup = soup(html, 'html.parser')

# grabbing data
containers = page1_soup.findAll('div', {'class': 'part-text'})

# Make the connection to PostgreSQL
conn = psycopg2.connect(database='MyBrickVault', user='postgres', password='123', port=5433)
cursor = conn.cursor()

# Insert data into table
for container in containers:
    print(container.text)
    print(container.find_all_next('small', {'class': 'trunc'})[0].text.split()[0].replace('{', '').replace('-1', ''))
    num_parts = int(container.find_all_next('small', {'class': 'text-right'})[0].text.strip().split()[0][1:])
    if num_parts > 0:
        size = 'small' if num_parts <= 500 else ('medium' if num_parts <= 1000 else 'large')
        query = "INSERT INTO sets (id, size) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
        data = (id, size)
        cursor.execute(query, data)

# Commit the transaction
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
