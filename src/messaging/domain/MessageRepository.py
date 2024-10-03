from abc import ABC, abstractmethod
from typing import Optional, List
from .Message import Message

class MessageRepository(ABC):
    @abstractmethod
    def save(self, message: Message) -> Message:
        pass

    @abstractmethod
    def update(self, message: Message) -> Message:
        pass

    @abstractmethod
    def find_by_id(self, message_id: int) -> Optional[Message]:
        pass

    @abstractmethod
    def find_all(self) -> List[Message]:
        pass