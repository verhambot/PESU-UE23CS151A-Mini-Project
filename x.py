import mysql.connector as sql
sqlc = sql.connect(host="localhost", user="root", password="Amogh2004", database="zomapes")
cur=sqlc.cursor()
cur.execute("insert into log1 values('1','1');")
sqlc.commit()