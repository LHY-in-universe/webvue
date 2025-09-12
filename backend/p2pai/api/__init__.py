from fastapi import APIRouter
from .projects import router as projects_router
from .training import router as training_router
from .nodes import router as nodes_router
from .datasets import router as datasets_router
from .models import router as models_router

router = APIRouter()

# Include sub-routers
router.include_router(projects_router, prefix="/projects", tags=["Projects"])
router.include_router(training_router, prefix="/training", tags=["Training"])
router.include_router(nodes_router, prefix="/nodes", tags=["Nodes"])
router.include_router(datasets_router, prefix="/datasets", tags=["Datasets"])
router.include_router(models_router, prefix="/models", tags=["Models"])
