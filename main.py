from classifier import SoundClassifier
from emergency_detector import EmergencySoundDetector
from ui_base import BaseUI

class ConsoleUI(BaseUI):
    def show_startup(self, labels):
        print("Loaded labels:")
        for label in labels:
            print(f"- {label}")
        print("\nListening... \n")
    def show_recording(self):
        print("Recording...")
    def show_detection(self, label: str, score: float, alert_level: str):
        if alert_level == "emergency":
            print(f"[EMERGENCY] {label} ({score:.2f})\n")
        elif alert_level == "important":
            print(f"[IMPORTANT] {label} ({score:.2f})\n")
        else:
            print(f"[NORMAL] {label} ({score:.2f})\n")


def main():
    classifier = SoundClassifier(labels_file="labels.csv",sample_rate=16000,duration=2)
    emergency_detector = EmergencySoundDetector()
    ui = ConsoleUI()
    ui.show_startup(classifier.get_labels())
    try:
        while True:
            ui.show_recording()
            results = classifier.classify_once()
            best = results[0]
            label = best["label"]
            score = best["score"]
            alert_level = emergency_detector.get_alert_level(label, score)
            ui.show_detection(label, score, alert_level)

    except KeyboardInterrupt: #just for now w/ console 
        print("Stopped.")


if __name__ == "__main__":
    main()