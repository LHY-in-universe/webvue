from fastapi import APIRouter
from .projects import router as projects_router
from .nodes import router as nodes_router
from .training import router as training_router
from .performance import router as performance_router
from .logs import router as logs_router
from .tasks import router as tasks_router

router = APIRouter()

# Include sub-routers
router.include_router(projects_router, prefix="/projects", tags=["Projects"])
router.include_router(nodes_router, prefix="/nodes", tags=["Nodes"])
router.include_router(training_router, prefix="/training", tags=["Training"])
router.include_router(performance_router, prefix="/performance", tags=["Performance"])
router.include_router(logs_router, prefix="/logs", tags=["Logs"])
router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
