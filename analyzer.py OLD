# processes incoming audio signals and analyzes their properties such as frequency, amplitude, and waveform patterns.outputs a decision about whether the sound should be enhanced, filtered, or deprioritized.

import numpy as np
from settings import Sample_Rate, Context_Modes, Current_Mode, Base_Threshold

adaptive_multiplier = 1.0

def adjust_sensitivity(amount):
    global adaptive_multiplier
    adaptive_multiplier += amount
    adaptive_multiplier = max(0.5, min(2.0, adaptive_multiplier))

def analyze_audio(audio):
    fft = np.abs(np.fft.rfft(audio))
    freqs = np.fft.rfftfreq(len(audio), 1 / Sample_Rate)

    dominant = freqs[np.argmax(fft)]

    low = np.mean(fft[freqs < 300])
    mid = np.mean(fft[(freqs >= 300) & (freqs < 2000)])
    high = np.mean(fft[freqs >= 2000])

    return dominant, low, mid, high

def classify_audio(audio):
    dominant, low, mid, high = analyze_audio(audio)
    mode = Context_Modes[Current_Mode]

    threshold = Base_Threshold * mode["sensitivity"] * adaptive_multiplier

    score = 0

    if high > mid * threshold and dominant > mode["alarm_freq"]:
        score += 60
    if low > mid and dominant < mode["vehicle_freq"]:
        score += 40

    score = min(score, 100)

    if score >= 60:
        return "RED", score
    elif score >= 30:
        return "YELLOW", score
    else:
        return "GREEN", score
