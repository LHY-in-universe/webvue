from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import os
import sys
from pathlib import Path

# Add the root directory to Python path for database imports
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Add the backend directory to Python path for router imports
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

# Import routers
from common.api import router as common_router
from p2pai.api import router as p2pai_router
from edgeai.api import router as edgeai_router

# Import database initialization
from database.edgeai.database import create_tables, get_database_info
from database.edgeai.init_db import init_database

# Import background tasks
from edgeai.background_tasks import start_background_tasks, stop_background_tasks

# Create FastAPI app
app = FastAPI(
    title="OpenTMP LLM Engine API",
    description="Secure and Efficient Distributed Machine Learning Solutions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=True  # 允许重定向斜杠
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177", "http://localhost:5178", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175", "http://127.0.0.1:5176", "http://127.0.0.1:5177", "http://127.0.0.1:5178", "http://127.0.0.1:8000"],
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

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库和后台任务"""
    try:
        print("🚀 Starting OpenTMP LLM Engine API...")

        # 获取数据库信息
        db_info = get_database_info()
        print(f"📊 Database URL: {db_info['database_url']}")

        # 检查数据库文件是否存在
        db_path = db_info['database_url'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            print("✅ Database file already exists")
        else:
            print("🔄 Initializing database...")
            # 初始化数据库（创建表和示例数据）
            init_database()
            print("✅ Database initialized successfully")

        # 启动后台任务（每60秒同步一次远程状态）
        print("🔄 Starting background tasks...")
        await start_background_tasks(sync_interval=60)
        print("✅ Background tasks started")

        print("🎉 Application startup completed!")

    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        # 不抛出异常，让应用继续启动
        print("⚠️  Application will continue with limited functionality")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时停止后台任务"""
    try:
        print("🛑 Stopping background tasks...")
        await stop_background_tasks()
        print("✅ Background tasks stopped")
        print("👋 Application shutdown completed")

    except Exception as e:
        print(f"❌ Error during shutdown: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )