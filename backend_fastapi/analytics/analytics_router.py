from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend_fastapi.database.database import get_db
from backend_fastapi.analytics.factory_analytics import compute_factory_analytics

router = APIRouter()


@router.get("/factory-analytics")
def get_factory_analytics(db: Session = Depends(get_db)):
    return compute_factory_analytics(db)