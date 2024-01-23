import uvicorn
from fastapi import FastAPI
from app.database import Base, engine, SQLALCHEMY_DATABASE_URL
from app.routers import auth, user, mail
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Template API", description="A template designed for reusability in LIA projects.")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(mail.router)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
