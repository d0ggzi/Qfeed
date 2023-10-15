import psycopg2

conn = psycopg2.connect("""
    host=rc1b-2wfn2w8hz6rt5hfv.mdb.yandexcloud.net
    port=6432
    sslmode=verify-full
    dbname=db1
    user=user1
    password=reflectme
    target_session_attrs=read-write
""")

q = conn.cursor()
q.execute("""INSERT INTO posts (post_text, post_label) VALUES (%s, %s);""", ("this is my message to u", '1'))

conn.commit()

conn.close()