from src.messaging.domain.MessageRepository import MessageRepository
from src.messaging.domain.Message import Message
from src.messaging.infrastructure.orm.MessageModel import MessageModel
from sqlalchemy.orm import Session
from typing import Optional, List

class MySqlMessageRepository(MessageRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, message: Message) -> Message:
        message_model = MessageModel(
            recipient_phone_number=message.recipient_phone_number,
            message_type=message.message_type,
            message_content=message.message_content,
            status=message.status
        )
        self.db_session.add(message_model)
        self.db_session.commit()
        self.db_session.refresh(message_model)

        message.id = message_model.id
        return message

    def update(self, message: Message) -> Message:
        message_model = self.db_session.query(MessageModel).filter_by(id=message.id).first()
        if message_model:
            message_model.recipient_phone_number = message.recipient_phone_number
            message_model.message_type = message.message_type
            message_model.message_content = message.message_content
            message_model.status = message.status

            self.db_session.commit()
            self.db_session.refresh(message_model)

        return message

    def find_by_id(self, message_id: int) -> Optional[Message]:
        message_model = self.db_session.query(MessageModel).filter_by(id=message_id).first()
        if message_model:
            return Message(
                id=message_model.id,
                recipient_phone_number=message_model.recipient_phone_number,
                message_type=message_model.message_type,
                message_content=message_model.message_content,
                status=message_model.status,
                updated_at=message_model.updated_at  # Include this line
            )
        return None

    def find_all(self) -> List[Message]:
        message_models = self.db_session.query(MessageModel).all()
        return [
            Message(
                id=message_model.id,
                recipient_phone_number=message_model.recipient_phone_number,
                message_type=message_model.message_type,
                message_content=message_model.message_content,
                status=message_model.status
            )
            for message_model in message_models
        ]