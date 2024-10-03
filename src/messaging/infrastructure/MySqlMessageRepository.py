from src.messaging.domain.MessageRepository import MessageRepository
from src.messaging.domain.Message import Message
from sqlalchemy.orm import Session
from typing import Optional, List

class MySqlMessageRepository(MessageRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, message: Message) -> Message:
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def update(self, message: Message) -> Message:
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def find_by_id(self, message_id: int) -> Optional[Message]:
        return self.db_session.query(Message).filter_by(id=message_id).first()

    def find_all(self) -> List[Message]:
        return self.db_session.query(Message).all()