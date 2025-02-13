from fastapi import FastAPI, Form, Request , Query
from fastapi import FastAPI, Form,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")
@app.get("/")
async def read_homepage(request: Request):
	return templates.TemplateResponse("index.html",{"request":request})

@app.post("/signin")
def signin(account :Annotated[str,Form()],password : Annotated[str,Form()] ):
	if (account != "text") | (password != "text"):
		return RedirectResponse("/error?error=密碼輸入錯誤" , status_code=303)
   
	# return RedirectResponse()
   
# @app.get("/member")
# async def read_memberPage(request: Request):
# 	return templates.TemplateResponse("test.html",{"request":request})

@app.get("/error")
def err(request:Request , error):
      return templates.TemplateResponse("err_page.html",{"request":request , "error":error})
