# Emergency Sound Detection Logic
# Used in console version to determine alert levels based on user preferences
# Maps sound priorities to confidence thresholds

class EmergencySoundDetector:
    """Determines alert levels for detected sounds based on user preferences"""
    def __init__(self, user_preferences):
        self.user_preferences = user_preferences
        self.thresholds = {
            "emergency": 0.6,
            "high": 0.55,
            "medium": 0.5,
            "low": 0.45,
            "normal": 0.5
        }

    def get_alert_level(self, label, score):
        """Get alert level for a sound based on priority and confidence score"""
        priority = self.user_preferences.get_priority(label)
        threshold = self.thresholds.get(priority, 0.5)
        if score < threshold:
            return "ignore"
        return priority

