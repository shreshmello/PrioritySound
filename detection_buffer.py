# Sound Detection Buffer
# Used in console version to confirm repeated sound detections
# Maintains a rolling buffer of recent predictions to filter noise

from collections import deque

class DetectionBuffer:
    """Buffer for sound detections to require multiple confirmations"""
    def __init__(self, size=5, required_matches=3):
        self.buffer = deque(maxlen=size)
        self.required_matches = required_matches

    def add(self, label):
        """Add a sound detection to the buffer"""
        self.buffer.append(label)

    def confirmed(self):
        """Check if a sound has been detected enough times to be confirmed"""
        if len(self.buffer) < self.required_matches:
            return None
        most_common = max(set(self.buffer), key=self.buffer.count)
        if self.buffer.count(most_common) >= self.required_matches:
            return most_common
        return None
