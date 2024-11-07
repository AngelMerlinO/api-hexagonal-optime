from fastapi import APIRouter, Depends, HTTPException, Request, Query
from src.notifications.infrastructure.NotificationDependecies import get_notification_service
from src.auth.jwt_handler import get_current_user
from src.notifications.domain.exceptions import InvalidNotificationTypeException
from slowapi.util import get_remote_address
from slowapi import Limiter
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from bson import ObjectId
from src.notifications.application.services.NotificationService import NotificationService

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/api/v1/notifications",
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
    id: str
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[str] = None
    link: Optional[str] = None
    status: Optional[str] = None

@router.post("/")
@limiter.limit("2/minute")  
def create_notification(
    notification_data: NotificationCreateModel,
    request: Request,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: str = Depends(get_current_user)
):
    try:
        notification = notification_service.create_notification(
            user_id=notification_data.user_id,
            title=notification_data.title,
            content=notification_data.message,
            type=notification_data.type,
            link=notification_data.link
        )
        
        notification_dict = jsonable_encoder(notification)
        return {"message": "Notification created successfully", "notification_id": notification_dict}
    
    except InvalidNotificationTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
@router.put("/{notification_id}")
@limiter.limit("2/minute")
def update_notification_by_id(
    request: Request,
    notification_id: str,
    notification_data: NotificationUpdateModel,
    notification_service=Depends(get_notification_service),
    current_user: str = Depends(get_current_user)
):
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(status_code=400, detail="Invalid notification ID format.")
    
    try:
        # Verifica si la notificación existe
        existing_notification = notification_service.get_notification_by_id(notification_id)
        if existing_notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        updated_notification = notification_service.update_notification(
            identifier=notification_id,
            title=notification_data.title,
            content=notification_data.message,
            type=notification_data.type,
            link=notification_data.link
        )
        
        return {"message": "Notification updated successfully", "notification_id": jsonable_encoder(updated_notification)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/{notification_id}")
@limiter.limit("2/minute")  
def delete_notifications(
    notification_id: str,
    request: Request,
    notification_service: NotificationService = Depends(get_notification_service),
    current_user: str = Depends(get_current_user)
):
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(status_code=400, detail="Invalid notification ID format. It must be a 24-character hex string.")

    try:
        notification_service.delete_notification(identifier=notification_id)
        return {
            "message": f"Notification with ID {notification_id} deleted successfully"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")