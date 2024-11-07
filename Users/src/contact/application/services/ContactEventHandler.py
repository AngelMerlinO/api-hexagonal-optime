class ContactEventHandler:
    def handle_contact_created_event(self, message: dict):
        contact_id = message.get("contact_id")
        email = message.get("email")
        print(f"User created with ID: {contact_id}, Email: {email}")
