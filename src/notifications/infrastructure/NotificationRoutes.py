from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.notifications.application.NotificationCreator import NotificationCreator
from src.notifications.infrastructure.MySqlNotificationRepository import MySqlNotificationRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from config.database import get_db
from pydantic import BaseModel
from typing import Optional

from src.users.domain.exceptions import UserNotFoundException
from src.notifications.domain.exceptions import InvalidNotificationTypeException

router = APIRouter()

# Modelos Pydantic
class NotificationCreateModel(BaseModel):
    user_id: int
    title: str
    message: str
    type: str  # 'email', 'sms', 'push', 'in_app'
    link: Optional[str] = None

@router.post("/notifications/")
def create_notification(
    notification_data: NotificationCreateModel,
    db: Session = Depends(get_db)
):
    notification_repo = MySqlNotificationRepository(db)
    user_repo = MySqlUserRepository(db)
    notification_creator = NotificationCreator(notification_repo, user_repo)
    try:
        notification = notification_creator.create(
            notification_data.user_id,
            notification_data.title,
            notification_data.message,
            notification_data.type,
            notification_data.link
        )
        return {"message": "Notification created successfully", "notification_id": notification.id}
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidNotificationTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))