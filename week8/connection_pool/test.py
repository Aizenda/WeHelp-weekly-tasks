import time
import mysql.connector
from mysql.connector import pooling

# 測量不使用連線池時的時間
start_time = time.time()

# 不使用連線池，每次都創建新的資料庫連線
cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='website')
cursor = cnx.cursor()
cursor.execute("SELECT * FROM member")
result = cursor.fetchall()
cnx.close()

end_time = time.time()

print(f"Time taken (no connection pool): {end_time - start_time} seconds")



# 創建連線池
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, user='root', password='root', host='127.0.0.1', database='website')

# 測量使用連線池時的時間
start_time = time.time()

# 從連線池獲取連線
cnx = connection_pool.get_connection()
cursor = cnx.cursor()
cursor.execute("SELECT * FROM member")
result = cursor.fetchall()
cnx.close()

end_time = time.time()

print(f"Time taken (with connection pool): {end_time - start_time} seconds")
