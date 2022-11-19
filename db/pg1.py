import psycopg2

conn = psycopg2.connect(
    dbname="test1",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
    )

cur = conn.cursor()

cur.execute("select * from table1")

records = cur.fetchall()

print(records)
