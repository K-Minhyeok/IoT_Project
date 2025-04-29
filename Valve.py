class Valve:
    def __init__(self, valve_number, left=False, right=False):
        self.valve_number = valve_number
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.valve_number}번 밸브 - 좌: {'켜짐' if self.left else '꺼짐'}, 우: {'켜짐' if self.right else '꺼짐'}"
