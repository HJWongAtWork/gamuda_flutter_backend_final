from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

from app.api.routes import auth, users, analytics
from app.utils.db_utils import init_db
from app.config.settings import SECRET_KEY

# Load environment variables
load_dotenv()

# FastAPI app initialization
app = FastAPI(
    title="User Analytics API",
    description="API for user data and analytics",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Authentication operations"
        },
        {
            "name": "Analytics",
            "description": "Analytics operations"
        },
        {
            "name": "Users",
            "description": "User operations"
        }
    ]
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gamuda-flutter-homework-01.web.app",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Accept",
        "Authorization",
        "Origin",
        "X-Requested-With",
        "X-CSRF-Token",
    ],
    expose_headers=["*"],
    max_age=3600,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    max_age=30 * 24 * 60 * 60,  # 30 days in seconds
)

# Add this middleware for handling preflight requests
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return Response(status_code=200)

# Add these middleware for handling COOP and COEP
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(analytics.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
