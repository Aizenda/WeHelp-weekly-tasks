from fastapi import FastAPI, Form, Request , Query , Body
from fastapi.responses import  RedirectResponse,JSONResponse
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
    https_only=True
)

def connect_to_database(user: str, password: str, host: str, database: str ):
    try:
        cnx = mysql.connector.connect(user=user,
                                      password=password,
                                      host=host,
                                      database=database)
        cursor = cnx.cursor(dictionary=True)
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
        query = "SELECT id, name, username FROM member WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result is None:
            return RedirectResponse("/error?message=登錄失敗，帳號或密碼錯誤", status_code=303)
        
        # 儲存 **id, name, username** 到 session
        request.session["member"] = {
            "id": result["id"],
            "name": result["name"],
            "username": result["username"]
        }

        return RedirectResponse("/member", status_code=303)
    
    except Exception as e:
        print(f"資料庫操作錯誤: {e}")  
        return RedirectResponse("/error?message=資料庫操作失敗", status_code=303)

    finally:
        cursor.close()
        cnx.close()

#會員頁
@app.get("/member")
async def member(request: Request):
    if "member" not in request.session:
        return RedirectResponse("/error?message=您尚未登錄", status_code=303)

    cnx, cursor = connect_to_database('root', 'root', '127.0.0.1', 'website')
    if not cnx or not cursor:
        return RedirectResponse("/error?message=資料庫連接失敗", status_code=303)

    try:
        # 取得所有留言
        query = """
        SELECT message.id, member.name, message.content, message.member_id
        FROM member 
        INNER JOIN message ON member.id = message.member_id
        """
        cursor.execute(query)
        all_message = cursor.fetchall()
        # 取得當前登入用戶的 ID
        session_member_id = request.session["member"]["id"]

        response = templates.TemplateResponse("member_page.html", {
            "request": request, 
            "name": request.session["member"]["name"], 
            "all_message": all_message,
            "session_member_id": session_member_id  # 傳到前端做比對
        })
        response.headers["Cache-Control"] = "no-store"  # 禁止緩存
        
        return response

    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse("/error?message=無法加載留言", status_code=303)

    finally:
        cursor.close()
        cnx.close()

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

        member_id = member.get("id") 

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

#留言刪除路由
@app.post("/deleteMessage")
async def delete_message(request: Request, message_id: int = Form(...)):
    if "member" not in request.session:
        return RedirectResponse("/error?message=您尚未登錄", status_code=303)

    cnx, cursor = connect_to_database('root', 'root', '127.0.0.1', 'website')
    if not cnx or not cursor:
        return RedirectResponse("/error?message=資料庫連接失敗", status_code=303)

    try:
        # 取得當前登入的會員 ID
        session_member_id = request.session["member"]["id"]

        # 確保當前會員只能刪除自己的留言
        cursor.execute("SELECT member_id FROM message WHERE id = %s", (message_id,))
        message = cursor.fetchone()

        if not message:
            return RedirectResponse("/error?message=留言不存在", status_code=303)

        if message["member_id"] != session_member_id:
            return RedirectResponse("/error?message=您無權刪除此留言", status_code=303)

        # 刪除留言
        cursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
        cnx.commit()

        return RedirectResponse("/member", status_code=303)

    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse("/error?message=刪除留言失敗", status_code=303)

    finally:
        cursor.close()
        cnx.close()

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

#會員查詢路由
@app.get("/api/member")
async def query_member(request:Request , username:str = Query(None)):
    if "member" not in  request.session:
        return {"data":None}

    if not username:
        return {"data":None}

    cnx,cursor = connect_to_database('root','root','127.0.0.1','website')
    try:
        query = "SELECT id, name, username From member WHERE BINARY username = %s"
        cursor.execute(query,(username,))
        data = cursor.fetchone()
        
        if not data:
            return {"data":None}
        else:
            return {"data":data}
    
    finally:
        cursor.close()
        cnx.close()
        

#會員名稱更新路由
@app.patch("/api/member")
async def update_username(request:Request ,body :dict = Body(None)):

    new_name = body.get("name")
    user_id = request.session["member"]["id"]

    if "member" not in  request.session:
        return {"error":True}
    
    if not new_name:
        return {"error": True}
    
    cnx,cursor = connect_to_database('root','root','127.0.0.1','website')
    
    try:
        if request.session["member"]["name"] == new_name:
            return {"error":True}
        
        update_query = "UPDATE member SET name = %s WHERE id = %s"
        cursor.execute(update_query,(new_name, user_id))
        cnx.commit()

        return {"ok": True}
    
    finally:
        cursor.close()
        cnx.close() 

# 靜態檔案處理
app.mount("/static", StaticFiles(directory="static"), name="static")

