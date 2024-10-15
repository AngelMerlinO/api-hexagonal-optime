class User:
    def __init__(self, username: str, email: str, password: str, id: int = None, uuid: str = None):
        self.id = id
        self.uuid = uuid
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"