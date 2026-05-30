from fastapi import FastAPI
from app.database import engine, Base
from app.routers import matches

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundial 2026 API")

app.include_router(matches.router)


@app.get("/", tags=["Home"])
def home():
    return {"message": "Mundial 2026 API"}
