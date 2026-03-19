from collections import deque
class DetectionBuffer:
    def __init__(self, size=5, required_matches=3):
        self.buffer = deque(maxlen=size)
        self.required_matches = required_matches
    def add(self, label, confidence):
        self.buffer.append((label, confidence))
    def confirmed(self, threshold):
        if len(self.buffer) < self.required_matches:
            return None
        labels = {}
        confs = {}
        for label, conf in self.buffer:
            labels[label] = labels.get(label, 0)+ 1
            confs[label] = confs.get(label, 0) + conf
        best_label = max(labels, key = labels.get)
        if labels[best_label] >= self.required_matches:
            avg_conf = confs[best_label]/labels[best_label]
            if avg_conf < threshold:
                return None
            return best_label, avg_conf
        return None

  #stores last predicitons checks to see if a certain sound repeaets a lot
