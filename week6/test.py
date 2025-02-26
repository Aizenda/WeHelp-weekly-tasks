import mysql.connector
from mysql.connector import errorcode , Error
# 連線到資料庫，建立一個物件 con
con=mysql.connector.connect(
    user="root",
    password="root",
    host="localhost",
    database="website"
)
print("資料庫連線成功")
con.close()

# 建立Cursor物件，用來對資料庫下 SQL指令
cursor=con.cursor()
# 下指令
cursor.execute("insert into product(name) values('Green tea')")
con.commit()