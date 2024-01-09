import uvicorn
from fastapi import FastAPI
from app.routers import user, mail
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(mail.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
