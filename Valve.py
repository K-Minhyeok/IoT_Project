from datetime import datetime
import json

class Valve:
    def __init__(self, valve_number, left=False, right=False):
        self.valve_number = valve_number
        self.left = left
        self.right = right
        self.left_change_time = None
        self.right_change_time = None

    def toggle_left(self):
        self.left = not self.left
        self.left_change_time = self.current_time() 

    def toggle_right(self):
        self.right = not self.right
        self.right_change_time = self.current_time() 
        
    def current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "valve_number": self.valve_number,
            "left": self.left,
            "right": self.right,
            "left_change_time": self.left_change_time,
            "right_change_time": self.right_change_time
        }

    @classmethod
    def from_dict(cls, data):
        valve = cls(data["valve_number"])
        valve.left = data["left"]
        valve.right = data["right"]
        valve.left_change_time = data["left_change_time"]
        valve.right_change_time = data["right_change_time"]
        return valve

    def __str__(self):
        return (
            f"{self.valve_number}번 밸브 - "
            f"좌: {'켜짐' if self.left else '꺼짐'} (변경: {self.left_change_time}), "
            f"우: {'켜짐' if self.right else '꺼짐'} (변경: {self.right_change_time})"
        )
