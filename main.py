from classifier import SoundClassifier
from emergency_detector import EmergencySoundDetector
from ui_base import BaseUI
from detection_buffer import DetectionBuffer
from user_preferences import UserPreferences

buffer = DetectionBuffer()
def get_consensus_label(results, threshold=0.40):
    valid = []
    for r in results:
        if r["score"] >= threshold:
            valid.append(r["label"])
    if not valid:
        return None
    # pick most frequent label
    return max(set(valid), key=valid.count)

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
    username = input("Enter username: ")
    user_preferences = UserPreferences(username)
    classifier = SoundClassifier(labels_file="labels.csv",sample_rate=16000,duration=2)
    emergency_detector = EmergencySoundDetector(user_preferences)
    ui = ConsoleUI()
    ui.show_startup(classifier.get_labels())
    try:
        while True:
            ui.show_recording()
            results = classifier.classify_once()
label = get_consensus_label(results)
if label is None:
    continue
score = results[0]["score"]

# ignore low confidence predictions
if score < 0.55:
    continue
buffer.add(label)
confirmed_label = buffer.confirmed()

if confirmed_label:
       alert_level = emergency_detector.get_alert_level(label, score)
       if alert_level == "ignore":
          continue
       ui.show_detection(label, score, alert_level)

    except KeyboardInterrupt: #just for now w/ console 
        print("Stopped.")


if __name__ == "__main__":

    main()



