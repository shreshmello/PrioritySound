# Emergency Sound Detection Logic
# Used in console version to determine alert levels based on user preferences
# Maps sound priorities to confidence thresholds

class EmergencySoundDetector:
    """Determines alert levels for detected sounds based on user preferences"""
    def __init__(self, user_preferences, active_threshold):
        self.user_preferences = user_preferences
        self.active_threshold = active_threshold
        self.thresholds = {
            "emergency": active_threshold+0.1,
            "high": active_threshold+0.05,
            "medium": active_threshold,
            "low": active_threshold-0.05,
            "normal": active_threshold
        }

    def get_alert_level(self, label, score):
        priority = self.user_preferences.get(label.lower())
        if priority is None:
            priority = "low"
        if priority == "ignore":
            return "ignore"
        threshold = self.thresholds.get(priority, 0.10)
        if score < threshold:
            return "ignore"
        return priority

