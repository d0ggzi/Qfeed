from sql import SQL

db = SQL()
q = db.cursor
q.execute("""SELECT * from users""")

res = q.fetchall()
print(res)

db.conn.close()