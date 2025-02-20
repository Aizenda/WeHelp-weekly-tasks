from fastapi import FastAPI, Form, Request , Query , Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from mysql.connector import errorcode , Error

# 初始化
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 添加Session中間件
app.add_middleware(
    SessionMiddleware, 
    secret_key="vuhgfvuvytdfsdxhkbkjb", 
    https_only=False
)

def connect_to_database(user: str, password: str, host: str, database: str ):
    try:
        cnx = mysql.connector.connect(user=user,
                                      password=password,
                                      host=host,
                                      database=database)
        cursor = cnx.cursor(dictionary=True)
        print('SQL Connected check')
        return cnx, cursor  # 返回連線和游標以供後續操作
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(f"Error: {err}")
        return None, None  # 返回 None，表示連線失敗


# 根目錄路由
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#註冊路由
@app.post("/signup")
async def signup(request:Request,
                 name:str = Form(...),
                 username:str = Form(...),
                 password:str = Form(...)
):
    if not username.strip() or not password.strip() :
        return RedirectResponse("/error?message=帳號或密碼不能為空白", status_code=303)
    if not name.strip():
        return RedirectResponse("/error?message=姓名不能為空白", status_code=303)
    
    cnx, cursor = connect_to_database('root', 'root', '127.0.0.1', 'website')
    if not cnx or not cursor:
        return RedirectResponse("/error?message=資料庫連接失敗", status_code=303)
    
    try:
        query = "SELECT * FROM member WHERE username = %s"
        cursor.execute(query, (username,))
        request = cursor.fetchone()

        if request != None:
            return RedirectResponse("/error?message=註冊失敗，帳號重複" ,status_code=303)

        query_inert = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)" 
        cursor.execute(query_inert,(name, username, password))
        cnx.commit()
        return RedirectResponse("/",status_code=303)
    
    except Error as e:
        print(f"資料庫操作錯誤: {e}")  
        return RedirectResponse("/error?message=資料庫操作失敗", status_code=303)
    
    finally:
        cursor.close()
        cnx.close()

# 登入路由
@app.post("/signin")
async def signin(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):  
    if not username.strip() or not password.strip():
        return RedirectResponse("/error?message=帳號或密碼不能為空白", status_code=303)

    cnx, cursor = connect_to_database('root', 'root', '127.0.0.1', 'website')
    if not cnx or not cursor:
        return RedirectResponse("/error?message=資料庫連接失敗", status_code=303)

    try:
        query = "SELECT * FROM member WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result is None:
            return RedirectResponse("/error?message=登錄失敗，帳號或密碼錯誤", status_code=303)
        
        # 儲存登入資訊到 session
        request.session["member"] = {"name": result["name"],"username": result["username"]}

        return RedirectResponse("/member",status_code=303)
    
    except Error as e:
        print(f"資料庫操作錯誤: {e}")  
        return RedirectResponse("/error?message=資料庫操作失敗", status_code=303)

    finally:
        cursor.close()
        cnx.close()

# 會員頁路由
@app.get("/member")
async def member(request: Request): 
    if  len(request.session) == 0:
        return RedirectResponse("/error?message=您尚未登錄", status_code=303)
    
    cnx, cursor = connect_to_database('root', 'root', '127.0.0.1', 'website')
    if not cnx or not cursor:
        return RedirectResponse("/error?message=資料庫連接失敗", status_code=303)
    query = "SELECT member.name, message.content FROM member INNER JOIN message ON member.id = message.member_id"

    cursor.execute(query)
    all_message = cursor.fetchall()
    response = templates.TemplateResponse("member_page.html", {"request": request, "name":request.session["member"]["name"],"message_name": all_message ,"all_message":all_message})
    response.headers["Cache-Control"] = "no-store"#禁止儲存
    return response

#留言路由
@app.post("/createMessage")
async def createMessage(request: Request,
                        content: str = Form(...)
):  
     
    if not content.strip():
        return RedirectResponse("/error?message=留言不可為空", status_code=303)

    cnx, cursor = connect_to_database('root', 'root', '127.0.0.1', 'website')
    if not cnx or not cursor:
        return RedirectResponse("/error?message=資料庫連接失敗", status_code=303)

    try:
        # 1. 取得會員的 id
        cursor.execute("SELECT id FROM member WHERE username = %s", (request.session["member"]["username"], ))
        member = cursor.fetchone()

        if not member:
            return RedirectResponse("/error?message=找不到會員", status_code=303)

        member_id = member.get("id")  # 取得會員 id
        print(member_id)

        # 2. 插入訊息
        cursor.execute(
            "INSERT INTO message (member_id, content) VALUES (%s, %s)",
            (member_id, content),
        )
        cnx.commit()
        return RedirectResponse("/member",status_code=303)
    
    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse("/error?message=發表失敗", status_code=303)
    finally:
        cursor.close()
        cnx.close()

#留言顯示

#登出路由
@app.get("/signout")
async def signout(request: Request):
    request.session.clear()  # 清空 session
    return RedirectResponse("/", status_code=303)

# 錯誤路由
@app.get("/error")
async def err(request: Request, message: str):
    if  len(request.session) == 0:
        return templates.TemplateResponse("err_page.html", {"request": request, "err": message})
    else:
        return templates.TemplateResponse("err_member_page.html", {"request": request, "err": message})


# 靜態檔案處理
app.mount("/static", StaticFiles(directory="static"), name="static")
