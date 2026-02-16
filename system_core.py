import sounddevice as sd
import numpy as np
import speech_recognition as sr
import tkinter as tk
import time

from analyzer import classify_audio, adjust_sensitivity
from settings import Sample_Rate, Listen_Seconds
from state_manager import StateManager


class PrioritySoundSystem:

    def __init__(self, user_name):
        self.user_name = user_name.lower()
        self.state_manager = StateManager()
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        self.window = tk.Tk()
        self.window.title("PrioritySound")

        self.label = tk.Label(
            self.window,
            text="System initialized.\nState: IDLE",
            font=("Arial", 14),
            wraplength=500,
            justify="left"
        )
        self.label.pack(padx=20, pady=20)

        self.transcript = ""
        self.last_alert_time = 0

        self.window.bind("<Up>", lambda e: adjust_sensitivity(0.1))
        self.window.bind("<Down>", lambda e: adjust_sensitivity(-0.1))
        self.window.bind("<f>", lambda e: adjust_sensitivity(0.2))

    def check_priority(self):
        audio = sd.rec(
            int(Listen_Seconds * Sample_Rate),
            samplerate=Sample_Rate,
            channels=1,
            dtype="float32"
        )
        sd.wait()
        audio = audio.flatten()

        level, score = classify_audio(audio)

        if level != "GREEN":
            self.state_manager.set_state("ALERT")
            self.last_alert_time = time.time()
            self.label.config(
                text=f"State: ALERT\nPriority Score: {score}"
            )

    def listen_for_name(self):
        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, phrase_time_limit=3)

            text = self.recognizer.recognize_google(audio)

            if self.user_name in text.lower():
                self.state_manager.set_state("TRANSCRIBE")
                self.label.config(text="State: TRANSCRIBE\nListening...")
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

                self.transcript += text + " "
                self.label.config(text=f"State: TRANSCRIBE\n\n{self.transcript}")
                self.window.update()

                silence_start = None

            except:
                if silence_start is None:
                    silence_start = time.time()

                if time.time() - silence_start > 5:
                    self.state_manager.set_state("COOLDOWN")
                    self.label.config(text="State: COOLDOWN\nReturning to IDLE...")
                    time.sleep(2)
                    self.state_manager.set_state("IDLE")
                    self.transcript = ""
                    break

    def run(self):
        while True:
            current_state = self.state_manager.get_state()

            if current_state == "IDLE":
                self.label.config(text="State: IDLE\nMonitoring...")
                self.check_priority()
                self.listen_for_name()

            elif current_state == "ALERT":
                if time.time() - self.last_alert_time > 3:
                    self.state_manager.set_state("IDLE")

            self.window.update()
