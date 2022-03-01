import sqlite3

connection = sqlite3.connect('traindatabase.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# for now just add the single station the api will handle
cur.execute("INSERT INTO station (id, name) VALUES (?,?)",
            (1, 'Fulton Street')
            )

connection.commit()
connection.close()