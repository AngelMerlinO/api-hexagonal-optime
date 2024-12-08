from fastapi import APIRouter
from src.activities.infraestructure.ActivitiesRouter import router as activities_router

router = APIRouter()

router.include_router(activities_router)

