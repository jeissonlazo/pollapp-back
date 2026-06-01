from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import matches, users, groups, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundial 2026 API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matches.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(auth.router)

@app.get("/", tags=["Home"])
def home():
    return {"message": "Mundial 2026 API"}
