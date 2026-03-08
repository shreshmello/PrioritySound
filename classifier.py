import csv
import sounddevice as sd
from transformers import pipeline


class SoundClassifier:
    def __init__(self, labels_file: str = "labels.csv", sample_rate: int = 16000, duration: int = 2): 
        self.labels_file = labels_file
        self.sample_rate = sample_rate
        self.duration = duration
        self.labels = self._load_labels()
        self.classifier = pipeline(task="zero-shot-audio-classification",model="laion/clap-htsat-unfused")
        #TODO: allow parameterized duration and sample rate to save device resources, expand labels.csv and emergency handle 


    def _load_labels(self):
        labels = []
        with open(self.labels_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                label = row.get("label", "").strip()
                if label:
                    labels.append(label)
        return labels
        
    def get_labels(self):
        return self.labels

    def record_audio(self):
        audio = sd.rec(int(self.duration * self.sample_rate),samplerate=self.sample_rate,channels=1,dtype="float32")
        sd.wait()
        return audio.flatten()

    def classify_audio(self, audio):
        return self.classifier(audio, candidate_labels=self.labels)

    def classify_once(self):
        audio = self.record_audio()
        return self.classify_audio(audio)