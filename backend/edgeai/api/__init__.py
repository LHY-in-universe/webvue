from fastapi import APIRouter
from .projects import router as projects_router
from .nodes import router as nodes_router
from .training import router as training_router
from .performance import router as performance_router
from .logs import router as logs_router
from .tasks import router as tasks_router
from .models import router as models_router
from .real_data import router as real_data_router
from .clusters import router as clusters_router

router = APIRouter()

# Include sub-routers
router.include_router(projects_router, prefix="/projects", tags=["Projects"])
router.include_router(nodes_router, prefix="/nodes", tags=["Nodes"])
router.include_router(training_router, prefix="/training", tags=["Training"])
router.include_router(performance_router, prefix="/performance", tags=["Performance"])
router.include_router(logs_router, prefix="/logs", tags=["Logs"])
router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
router.include_router(models_router, prefix="/models", tags=["Models"])
router.include_router(real_data_router, prefix="/real-data", tags=["Real Data"])
router.include_router(clusters_router, prefix="/clusters", tags=["Clusters"])
