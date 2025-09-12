from fastapi import APIRouter
from .auth import router as auth_router
from .system import router as system_router

router = APIRouter()

# Include sub-routers
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(system_router, prefix="/system", tags=["System"])