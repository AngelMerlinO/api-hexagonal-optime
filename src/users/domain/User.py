class User:
    def __init__(self, username: str, email: str, password: str, id: int = None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"