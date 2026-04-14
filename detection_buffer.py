# Sound Detection Buffer
# Maintains a rolling buffer of recent predictions to confirm detections

from collections import deque

class DetectionBuffer:
    def __init__(self, size=5, required_matches=3):
        self.buffer = deque(maxlen=size)
        self.required_matches = required_matches

    def add(self, label, conf):
        """Add a sound detection (label + confidence) to the buffer"""
        self.buffer.append((label, conf))

    def confirmed(self, threshold):
        """Check if a sound is confirmed based on repeated detections"""
        if len(self.buffer) < self.required_matches:
            return None

        label_counts = {}
        conf_sums = {}

        # Count occurrences + sum confidences
        for label, conf in self.buffer:
            label_counts[label] = label_counts.get(label, 0) + 1
            conf_sums[label] = conf_sums.get(label, 0) + conf

        # Find most frequent label
        best_label = max(label_counts, key=label_counts.get)

        # Check if it meets required matches
        if label_counts[best_label] >= self.required_matches:
            avg_conf = conf_sums[best_label] / label_counts[best_label]

            # Check confidence threshold
            if avg_conf < threshold:
                return None

            return best_label, avg_conf

        return None
