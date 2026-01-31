from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, students, utils

app = FastAPI(title="FastAPI Backend")

origins = [
    "http://localhost:5173",
    "https://react-api-frontend-weld.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows all origins for testing. Replace with specific domains in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(
    students.router, prefix=f"{settings.API_V1_STR}/students", tags=["students"]
)
app.include_router(utils.router, prefix=f"{settings.API_V1_STR}/utils", tags=["utils"])


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Backend"}
