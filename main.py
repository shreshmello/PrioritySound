from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock

import sounddevice as sd
import numpy as np
import speech_recognition as sr
import time

from analyzer import classify_audio, adjust_sensitivity
from state_manager import StateManager
from settings import Sample_Rate, Listen_Seconds

class PrioritySoundUI(BoxLayout):
    status_text = StringProperty("Idle: Monitoring...")
    banner_color = ListProperty([0.8, 0.8, 0.8, 1])
    transcript_text = StringProperty("")

    def __init__(self, user_name, **kwargs):
        super().__init__(**kwargs)
        self.user_name = user_name.lower()
        self.state_manager = StateManager()
        self.transcript = ""
        self.last_alert_time = 0

        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        state = self.state_manager.get_state()

        if state == "IDLE":
            self.status_text = "State: IDLE | Monitoring..."
            self.check_audio()
            self.listen_for_name()
        elif state == "ALERT":
            if time.time() - self.last_alert_time > 3:
                self.state_manager.set_state("IDLE")
        elif state == "TRANSCRIBE":
            pass  # transcription handled separately
        elif state == "COOLDOWN":
            self.status_text = "State: COOLDOWN | Returning to IDLE..."
            time.sleep(1)
            self.state_manager.set_state("IDLE")
            self.transcript = ""

    def check_audio(self):
        try:
            audio = sd.rec(
                int(LISTEN_SECONDS * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32"
            )
            sd.wait()
            audio = audio.flatten()
            level, score = classify_audio(audio)

            colors = {
                "RED": [1, 0.4, 0.4, 1],
                "YELLOW": [1, 1, 0.7, 1],
                "GREEN": [0.7, 1, 0.7, 1]
            }

            self.banner_color = colors[level]
            if level != "GREEN":
                self.state_manager.set_state("ALERT")
                self.last_alert_time = time.time()
                self.status_text = f"State: ALERT | Priority {level} | Score: {score}"

        except Exception as e:
            print("Audio error:", e)

    def listen_for_name(self):
        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, phrase_time_limit=3)
            text = self.recognizer.recognize_google(audio).lower()
            if self.user_name in text:
                self.state_manager.set_state("TRANSCRIBE")
                self.status_text = "State: TRANSCRIBE | Listening..."
                self.transcribe()
        except:
            pass

    def transcribe(self):
        silence_start = None
        while True:
            try:
                with self.mic as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=4)
                text = self.recognizer.recognize_google(audio)
                self.transcript += text + "\n"
                self.transcript_text = self.transcript
                self.ids.scroll_label  # force update
                silence_start = None
            except:
                if silence_start is None:
                    silence_start = time.time()
                if time.time() - silence_start > 5:
                    self.state_manager.set_state("COOLDOWN")
                    break

    def increase_sensitivity(self):
        adjust_sensitivity(0.1)
        self.status_text += " | Sensitivity ↑"

    def decrease_sensitivity(self):
        adjust_sensitivity(-0.1)
        self.status_text += " | Sensitivity ↓"

    def false_alert(self):
        adjust_sensitivity(0.2)
        self.status_text += " | False Alert Noted"

class PrioritySoundApp(App):
    def build(self):
        name = input("Enter your name: ")
        return PrioritySoundUI(name)

if __name__ == "__main__":
    PrioritySoundApp().run()
