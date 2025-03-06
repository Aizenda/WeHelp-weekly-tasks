from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 設定允許的來源（你可以將 * 設置為允許所有來源）
origins = [
    "http://localhost:3000",   # 本地開發網站的來源
    "https://example.com",     # 你希望允許的其他域名
    "*",                       # 這樣設置可以允許所有來源，根據需要設置
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,    # 允許的來源
# )

@app.get("/example")
async def example():
    return {"message": "This is a shared API"}
