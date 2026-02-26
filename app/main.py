from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="RetrievalStack API",
    version="1.0.0"
)

# Root endpoint (professional polish)
@app.get("/")
def root():
    return {
        "service": "RetrievalStack API",
        "version": "1.0.0",
        "status": "running"
    }

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.3:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")