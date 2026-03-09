import json
import os

class UserPreferences:
    def __init__(self, username):
        self.username = username
        self.file = f"users/{username}.json"
        if not os.path.exists("users"):
            os.makedirs("users")
        if os.path.exists(self.file):
            self.load()
        else:
            self.create_new_user()
    def create_new_user(self):
        print("\nChoose a profile:")
        print("1 - Parent Mode")
        print("2 - Home Mode")
        print("3 - Outdoor Mode")

        choice = input("Select profile: ")
        if choice == "1":
            priorities = {
                "baby crying": "high",
                "glass breaking": "high",
                "smoke alarm": "emergency",
                "fire alarm": "emergency"
            }

        elif choice == "2":
            priorities = {
                "doorbell ringing": "high",
                "door knocking": "high",
                "smoke alarm": "emergency",
                "fire alarm": "emergency"
            }

        elif choice == "3":
            priorities = {
                "car horn": "high",
                "police siren": "emergency",
                "ambulance siren": "emergency",
                "fire truck siren": "emergency"
            }
        else:
            priorities = {}

        self.priorities = priorities
        self.save()
    def load(self):
        with open(self.file, "r") as f:
            data = json.load(f)
            self.priorities = data["priorities"]
    def save(self):
        with open(self.file, "w") as f:
            json.dump({"priorities": self.priorities}, f, indent=4)
    def get_priority(self, label):
        return self.priorities.get(label, "normal")
