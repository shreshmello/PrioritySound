from collections import deque
class DetectionBuffer:
    def __init__(self, size=5, required_matches=3):
        self.buffer = deque(maxlen=size)
        self.required_matches = required_matches
    def add(self, label):
        self.buffer.append(label)
    def confirmed(self):
        if len(self.buffer) < self.required_matches:
            return None
        most_common = max(set(self.buffer), key=self.buffer.count)
        if self.buffer.count(most_common) >= self.required_matches:
            return most_common
        return None

  #stores last predicitons checks to see if a certain sound repeaets a lot
