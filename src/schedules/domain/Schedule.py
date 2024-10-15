class Schedule:
    def __init__(self, user_id: int, uuid: str = None, id: int = None):
        self.id = id
        self.uuid = uuid
        self.user_id = user_id
        self.schedule_items = []

    def add_schedule_item(self, item):
        self.schedule_items.append(item)

    def __repr__(self):
        return f"<Schedule {self.uuid} for User {self.user_id}>"
