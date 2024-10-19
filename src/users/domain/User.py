class User:
    def __init__(self,contact_id: int, username: str, email: str, password: str, id: int = None, uuid: str = None):
        self.id = id
        self.uuid = uuid
        self.contact_id = contact_id
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"