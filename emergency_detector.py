class EmergencySoundDetector:
    def __init__(self) -> None:
        self.emergency_labels = {
            "smoke alarm",
            "fire alarm",
            "carbon monoxide alarm",
            "glass breaking",
            "window breaking",
            "gunshot",
            "explosion",
            "police siren",
            "ambulance siren",
            "fire truck siren",
        }

        self.important_labels = {
            "door knocking",
            "doorbell ringing",
            "baby crying",
            "person shouting",
            "someone calling your name",
            "car horn",
            "dog barking",
        }

        self.emergency_threshold = 0.35 #confidence score
        self.important_threshold = 0.45

    def get_alert_level(self, label: str, score: float) -> str:
        if label in self.emergency_labels and score >= self.emergency_threshold:
            return "emergency"
        if label in self.important_labels and score >= self.important_threshold:
            return "important"
        return "normal"