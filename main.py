# Console Version of PrioritySound 
# Alternative command-line interface for testing sound detection 
# Not used in the web application - kept for development/testing purposes 

def main():
    """Main console application loop"""
    username = input("Enter username: ")
    user_preferences = UserPreferences(username)

    classifier = SoundClassifier(
        labels_file="labels.csv",
        sample_rate=16000,
        duration=2
    )

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
                alert_level = emergency_detector.get_alert_level(
                    confirmed_label,
                    score
                )

                if alert_level == "ignore":
                    continue

                ui.show_detection(
                    confirmed_label,
                    score,
                    alert_level
                )

    except KeyboardInterrupt:
        print("Stopped.")
