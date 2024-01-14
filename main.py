import uvicorn
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import authRouter, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(authRouter.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
