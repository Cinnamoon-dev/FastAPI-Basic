import uvicorn
from fastapi import FastAPI
from app.routers import user, mail, authRouter
from app.database import Base, engine
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.include_router(user.router)
app.include_router(authRouter.router)
app.include_router(mail.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
