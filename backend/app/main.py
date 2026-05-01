from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import locations, admin
from app.db.base import engine
from app.models import location

app = FastAPI(
    title="Indian Village Location API",
    description="B2B API for hierarchical Indian location data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locations.router)
app.include_router(admin.router)

@app.on_event("startup")
def create_tables():
    location.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Indian Village Location API", "docs": "/docs"}
