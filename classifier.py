import csv
import time
import sounddevice as sd
from transformers import pipeline


class SoundClassifier:
    def __init__(
        self,
        labels_file: str = "labels.csv",
        sample_rate: int = 16000,
        duration: int = 2,
    ):
        self.labels_file = labels_file
        self.sample_rate = sample_rate
        self.duration = duration
        self.labels = self._load_labels()
        self.classifier = pipeline(
            "audio-classification",
            model="MIT/ast-finetuned-audioset-10-10-0.4593"
        )
        self.label_aliases = {
            "baby crying": ["baby cry, infant cry"],
            "doorbell ringing": ["doorbell", "ding-dong"],
            "smoke alarm": ["smoke detector, smoke alarm", "alarm"],
            "fire alarm": ["fire alarm", "smoke detector, smoke alarm", "alarm"],
            "police siren": ["siren"],
            "ambulance siren": ["siren"],
            "car horn": ["vehicle horn, car horn, honking", "car passing by"],
        }

    def _load_labels(self):
        labels = []
        with open(self.labels_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                label = row.get("label", "").strip()
                if label:
                    labels.append(label.lower())
        return labels

    def get_labels(self):
        return self.labels

    def record_audio(self):
        audio = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )
        sd.wait()
        return audio.flatten()

    def _map_ast_label(self, ast_label: str):
        ast_label = ast_label.lower()

        for app_label, aliases in self.label_aliases.items():
            for alias in aliases:
                if alias in ast_label:
                    return app_label

        return None

    def classify_audio(self, audio):
        raw_results = self.classifier(audio, top_k=10)

        mapped_results = []
        seen = set()

        for result in raw_results:
            ast_label = result["label"]
            score = float(result["score"])
            mapped_label = self._map_ast_label(ast_label)

            if mapped_label and mapped_label not in seen:
                mapped_results.append({
                    "label": mapped_label,
                    "score": score,
                    "raw_label": ast_label
                })
                seen.add(mapped_label)

        if not mapped_results:
            return [
                {
                    "label": r["label"],
                    "score": float(r["score"]),
                    "raw_label": r["label"]
                }
                for r in raw_results[:5]
            ]

        return mapped_results[:5]

    def classify_once(self):
        audio = self.record_audio()
        return self.classify_audio(audio)

    def classify_continuously(self, callback, stop_event, min_confidence):
        while not stop_event.is_set():
            try:
                results = self.classify_once()
                top = results[0] if results else None

                if top:
                    payload = {
                        "label": top["label"],
                        "score": top["score"],
                        "raw_label": top["raw_label"],
                        "results": results,
                        "accepted": top["score"] >= min_confidence
                    }
                    callback(payload)

            except Exception as e:
                callback({
                    "error": str(e),
                    "accepted": False,
                    "results": []
                })

            time.sleep(0.2)