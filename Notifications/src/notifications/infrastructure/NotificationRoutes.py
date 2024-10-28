from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.notifications.application.NotificationCreator import NotificationCreator
from src.notifications.infrastructure.MySqlNotificationRepository import MySqlNotificationRepository
from src.users.infrastructure.MySqlUserRepository import MySqlUserRepository
from src.notifications.application.NotificationUpdater import NotificationUpdater
from src.notifications.application.NotificationEliminator import NotificationEliminator
from src.auth.jwt_handler import get_current_user
from slowapi.util import get_remote_address
from slowapi import Limiter
from src.auth.jwt_handler import get_current_user
from config.database import get_db
from pydantic import BaseModel
from typing import Optional
from fastapi import Query
from src.users.domain.exceptions import UserNotFoundException
from src.notifications.domain.exceptions import InvalidNotificationTypeException

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix=("/api/v1/notifications"),
    tags=["notifications"]
)

class NotificationCreateModel(BaseModel):
    user_id: int
    title: str
    message: str
    type: str 
    link: Optional[str] = None
    
class NotificationUpdateModel(BaseModel):  
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[str] = None
    link: Optional[str] = None

class NotificationUpdateResponse(BaseModel):
    id: int
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[str] = None
    link: Optional[str] = None
    status: str

@router.post("/")
@limiter.limit("2/minute")  
def create_notification(
    notification_data: NotificationCreateModel,
    request:Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
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
    
@router.put("/{notification_id}")
@limiter.limit("2/minute")  
def update_notifications(
    notification_id: int, 
    notification_data: NotificationUpdateModel,
    request:Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    ):
    
    repo = MySqlNotificationRepository(db)
    
    try:
        existing_notification = repo.find_by_id(notification_id)
        if not existing_notification:
            raise HTTPException(status_code=404, detail='Notification not found')
        
        if notification_data.title is not None:
            existing_notification.title = notification_data.title
        if notification_data.message is not None:
            existing_notification.message = notification_data.message
        if notification_data.type is not None:
            existing_notification.type = notification_data.type
        if notification_data.link is not None:
            existing_notification.link = notification_data.link
        
        updated_notification = repo.update(existing_notification)
        
        return NotificationUpdateResponse(
            id=updated_notification.id,
            status="success",
            title=updated_notification.title,
            message=updated_notification.message,
            type=updated_notification.type,
            link=updated_notification.link
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.delete("/")
@limiter.limit("2/minute")  
def delete_notifications(
    request: Request,
    notification_id = Query(..., description="ID of the notification to be deleted"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    
    repo = MySqlNotificationRepository(db)
    notification_eliminator = NotificationEliminator(repo)
    
    try:
        notification_eliminator.delete(notification_id)
        return {"message": f"Notifications with ID {notification_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
