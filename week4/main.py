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
        return RedirectResponse("/error?message=帳號與密碼不能為空", status_code=303)
    
    if member != "test" or password != "test":
        return RedirectResponse("/error?message=請確認帳號密碼是否正確", status_code=303)
    
    # 儲存登入資料到session
    request.session["member"] = member
    return RedirectResponse("/member", status_code=303) 
 
# 會員頁路由
@app.get("/member")
async def member(request: Request): 
    if  len(request.session) == 0:
        return RedirectResponse("/error?message=您尚未登錄", status_code=303)
    response = templates.TemplateResponse("member_page.html", {"request": request, "msg":"恭喜您，成功登入系統" })
    response.headers["Cache-Control"] = "no-store"#禁止儲存
    return response
    

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()  # 清空 session
    return RedirectResponse("/", status_code=303)

# 錯誤路由
@app.get("/error")
async def err(request: Request, message: str):
    return templates.TemplateResponse("err_page.html", {"request": request, "err": message})

#平方路由
@app.get("/square/{num}")
async def square(request: Request, num):

    if not num.isdigit():
        return RedirectResponse('/error?message=請輸入有效的"正"整數')
    num_int = int(num)

    return templates.TemplateResponse("square.html", {"request": request, "num": num_int * num_int})


# 靜態檔案處理
app.mount("/static", StaticFiles(directory="static"), name="static")
