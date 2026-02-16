# INSTALL FIRST
pip install sounddevice numpy SpeechRecognition pyaudio
-------------------------------------------------------------
Sample_Rate = 16000
Listen_in_Seconds = 2

Context_Modes = {
    "Classroom": {
        "alarm_freq": 1800,
        "vehicle_freq": 250,
        "sensitivity": 1.0
    },
    "Street": {
        "alarm_freq": 2200,
        "vehicle_freq": 400,
        "sensitivity": 1.2
    },
    "Home": {
        "alarm_freq": 1500,
        "vehicle_freq": 200,
        "sensitivity": 0.8
    },
    "Night": {
        "alarm_freq": 1400,
        "vehicle_freq": 180,
        "sensitivity": 0.6
    }
}

Current_Mode = "Classroom"
# Figure out how the user can change the current mode 

Base_Threshold = 2.0
