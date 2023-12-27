import uvicorn
from fastapi import FastAPI
from app.routers import test


app = FastAPI()

app.include_router(test.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
