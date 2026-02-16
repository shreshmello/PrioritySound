# software-design-code

Overview: 
Priority Sound is a smart audio management system designed to prioritize and manage multiple sound inputs in real time. The system detects, analyzes, and ranks incoming audio signals based on predefined importance levels, ensuring that critical sounds are amplified while lower-priority sounds are reduced or filtered out.
------------------------------------------------------------------------------------------------------------------------------------------
Key Features:
- Captures multiple audio inputs simultaneously.
- Assigns priority levels based on:
    Volume threshold
    Frequency patterns
    Predefined signal importance
    User-defined settings
- Optimized for fast response time to prevent delays in urgent situations.
- Users can modify which sounds receive higher priority.
-------------------------------------------------------------------------------------------------------------------------------------------
Libraries Used:
pyaudio – Captures live audio input
numpy – Performs signal processing and numerical operations
scipy – Frequency analysis and filtering
wave – Audio file handling
threading – Enables simultaneous multi-input processing
-------------------------------------------------------------------------------------------------------------------------------------------
How it Works:
1.Audio input streams are captured in real time.
2.Signals are converted into numerical arrays.
3.The system performs:
4.Amplitude detection
5.Frequency analysis (FFT)
6.Noise filtering
7.Each signal is assigned a priority score and is shown on the screen. 
