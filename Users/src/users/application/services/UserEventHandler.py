class UserEventHandler:
    def handle_user_created_event(self, message: dict):
        user_id = message.get("user_id")
        username = message.get("username")
        print(f"User created with ID: {user_id}, Username: {username}")
