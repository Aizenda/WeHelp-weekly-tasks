from fastapi import FastAPI, Form, Request , Query
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware

# 初始化
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 添加Session中間件
app.add_middleware(
    SessionMiddleware, 
    secret_key="vuhgfvuvytdfsdxhkbkjb", 
    https_only=False
)
# 根目錄路由
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 登入路由
@app.post("/signin")
async def signin(
    member:Annotated[str , Form()],
    password:Annotated[str , Form()],
    request: Request
    
): 
    # 驗證邏輯
    if not member or not password:
        return RedirectResponse("/error?err=帳號與密碼不能為空", status_code=303)
    
    if member != "test" or password != "test":
        return RedirectResponse("/error?err=請確認帳號密碼是否正確", status_code=303)
    
    # 儲存登入資料到session
    request.session["member"] = member

    return RedirectResponse("/member", status_code=303)

# 會員頁路由
@app.get("/member")
async def member(request: Request): 
    if  len(request.session) == 0:
        return RedirectResponse("/error?err=您尚未登錄", status_code=303)
    response = templates.TemplateResponse("member_page.html", {"request": request, "msg":"恭喜您，成功登入系統" })
    response.headers["Cache-Control"] = "no-store"#禁止儲存
    return response
    

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()  # 清空 session
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("session")  # 確保 session Cookie 被刪除
    return response

# 錯誤路由
@app.get("/error")
async def err(request: Request, err: str):
    return templates.TemplateResponse("err_page.html", {"request": request, "err": err})

@app.get("/square")
async def square(request: Request, num: str = Query(...)):
    try:
        # 嘗試將 num int
        num_int = int(num)

    except ValueError:
        # 如果轉換失敗，表示輸入不是有效的數字
        return RedirectResponse("/error?err=請輸入有效的格式(ex:1,2,3...)")

    if num_int <= 0:
        return RedirectResponse("/error?err=請輸入大於0的數字")
    
    return templates.TemplateResponse("square.html", {"request": request, "num": num_int * num_int})


# 靜態檔案處理
app.mount("/static", StaticFiles(directory="static"), name="static")

#Jinja2處理樣板引擎
templates = Jinja2Templates(directory="templates")