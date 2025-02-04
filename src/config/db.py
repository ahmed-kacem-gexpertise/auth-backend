import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="user_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()
conn.commit()
cur.close()
conn.close()