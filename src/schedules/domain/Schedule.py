class Schedule:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.schedule_items = []

    def add_schedule_item(self, item):
        self.schedule_items.append(item)

    def __repr__(self):
        return f"<Schedule for User {self.user_id}>"