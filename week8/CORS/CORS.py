from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import  FileResponse


app = FastAPI()

# 設定允許的來源（你可以將 * 設置為允許所有來源）
origins = [
    "http://localhost:8000",  
	"https://aizenda.github.io",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # 允許的來源
)

@app.get("/")
async def home():
    return FileResponse("index.html")

@app.get("/example")
async def example():
    return {"message": "This is a shared API"}
