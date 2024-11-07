# Notifications/src/notifications/infrastructure/NotificationRoutes.py

from fastapi import APIRouter, Depends, HTTPException, Request
from src.notifications.infrastructure.NotificationDependecies import get_notification_creator
from src.auth.jwt_handler import get_current_user
from src.notifications.domain.exceptions import InvalidNotificationTypeException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
from src.notifications.application.useCases.NotificationCreator import NotificationCreator
from bson import ObjectId

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["notifications"]
)

class NotificationCreateModel(BaseModel):
    user_id: int
    title: str
    message: str
    type: str  # Tipo de la notificación (e.g., "info", "alert")
    service_type: str  # Tipo de servicio de notificación, como "email" o "whatsapp"
    link: Optional[str] = None
    
class NotificationUpdateModel(BaseModel):  
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[str] = None
    link: Optional[str] = None

@router.post("/")
def create_notification(
    notification_data: NotificationCreateModel,
    notification_creator: NotificationCreator = Depends(get_notification_creator),
    current_user: str = Depends(get_current_user)
):
    try:
        notification = notification_creator.create(
            user_id=notification_data.user_id,
            title=notification_data.title,
            message=notification_data.message,
            type=notification_data.type,
            service_type=notification_data.service_type,
            link=notification_data.link
        )
        
        notification_dict = jsonable_encoder(notification)
        return {"message": "Notification created successfully", "notification_id": notification_dict}
    
    except InvalidNotificationTypeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{notification_id}")
def update_notification_by_id(
    request: Request,
    notification_id: str,
    notification_data: NotificationUpdateModel,
    notification_creator: NotificationCreator = Depends(get_notification_creator),
    current_user: str = Depends(get_current_user)
):
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(status_code=400, detail="Invalid notification ID format.")
    
    try:
        updated_notification = notification_creator.update(
            identifier=notification_id,
            title=notification_data.title,
            message=notification_data.message,
            type=notification_data.type,
            link=notification_data.link
        )
        
        return {"message": "Notification updated successfully", "notification_id": jsonable_encoder(updated_notification)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/{notification_id}")
def delete_notifications(
    notification_id: str,
    notification_creator: NotificationCreator = Depends(get_notification_creator),
    current_user: str = Depends(get_current_user)
):
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(status_code=400, detail="Invalid notification ID format. It must be a 24-character hex string.")

    try:
        notification_creator.delete(identifier=notification_id)
        return {
            "message": f"Notification with ID {notification_id} deleted successfully"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")