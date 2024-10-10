class Message:
    def __init__(self, recipient_phone_number, message_type, message_content, status=None, error_message=None, id=None):
        self.id = id
        self.recipient_phone_number = recipient_phone_number
        self.message_type = message_type
        self.message_content = message_content
        self.status = status
        self.error_message = error_message

    def __repr__(self):
        return f"<Message {self.id} to {self.recipient_phone_number}>"
