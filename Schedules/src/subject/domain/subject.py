from typing import List

class Subject:
    def __init__(self, name: str, period: int, group: str,
                 semester_grade: int, serialization_raiting: int, clearance_raiting: int,
                 monday: List[int], tuesday: List[int], wednesday: List[int], thursday: List[int], friday: List[int], uuid: str = None, id: int = None):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.period = period
        self.group = group
        self.semester_grade = semester_grade
        self.serialization_raiting = serialization_raiting
        self.clearance_raiting = clearance_raiting
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
    
    def __repr__(self):
        return f"<Subject {self.name}>"