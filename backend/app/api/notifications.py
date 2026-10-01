from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.schemas import DBNotification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("")
def get_notifications(role: str = "ALL", db: Session = Depends(get_db)):
    query = db.query(DBNotification)
    if role != "ALL":
        query = query.filter((DBNotification.recipient_role == role) | (DBNotification.recipient_role == "ALL"))
    notifs = query.order_by(DBNotification.created_at.desc()).limit(20).all()
    return notifs
