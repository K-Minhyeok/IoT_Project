from datetime import datetime

class Valve:
    def __init__(self, valve_number, left=False, right=False):
        self.valve_number = valve_number
        self.left = left
        self.right = right
        self.left_change_time = None
        self.right_change_time = None

    def toggle_left(self):
        self.left = not self.left
        self.left_change_time = self.current_time() if self.left else None

    def toggle_right(self):
        self.right = not self.right
        self.right_change_time = self.current_time() if self.right else None

    def current_time(self):
        return datetime.now()

    def elapsed_time(self, side):
        if side == 'left' and self.left and self.left_change_time:
            delta = datetime.now() - self.left_change_time
            return int(delta.total_seconds() / 60) 
        elif side == 'right' and self.right and self.right_change_time:
            delta = datetime.now() - self.right_change_time
            return int(delta.total_seconds() / 60)
        return 0  

    def __str__(self):
        return (
            f"{self.valve_number}번 밸브 - "
            f"좌: {'켜짐' if self.left else '꺼짐'} (변경: {self.left_change_time}), "
            f"우: {'켜짐' if self.right else '꺼짐'} (변경: {self.right_change_time})"
        )
