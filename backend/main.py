from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

# Import routers
from common.api import router as common_router
from p2pai.api import router as p2pai_router
from edgeai.api import router as edgeai_router

# Create FastAPI app
app = FastAPI(
    title="OpenTMP LLM Engine API",
    description="Secure and Efficient Distributed Machine Learning Solutions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)

# Include routers
app.include_router(common_router, prefix="/api/common", tags=["Common"])
app.include_router(p2pai_router, prefix="/api/p2pai", tags=["P2P AI"])
app.include_router(edgeai_router, prefix="/api/edgeai", tags=["Edge AI"])

@app.get("/")
async def root():
    return {
        "message": "OpenTMP LLM Engine API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )