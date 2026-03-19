![Logo](docs/PrioritySoundLogo.png)

# PrioritySound – Real-Time Sound Awareness for Deaf and Hard-of-Hearing Users

## Overview

**PrioritySound** is a real-time sound awareness system designed to help Deaf and Hard-of-Hearing individuals detect and understand important environmental sounds.  

Using machine learning, PrioritySound continuously monitors surrounding audio, identifies important sounds, and displays visual alerts that indicate both **the type of sound and where it is coming from**.

The goal is to improve **safety, awareness, and independence** by ensuring that critical sounds are never missed.

---

# Problem Statement

Over **1.5 billion people worldwide** experience some degree of hearing loss. Many of these individuals face challenges detecting important environmental sounds such as:

- Fire alarms
- Emergency sirens
- Door knocks
- Baby crying
- Breaking glass

These sounds are essential for safety and daily awareness.

Existing assistive technologies often fall short because they:

- Treat all sounds equally without prioritizing urgency
- Provide delayed or unreliable alerts
- Lack clear visual interfaces
- Do not indicate where a sound is coming from

As a result, Deaf and Hard-of-Hearing individuals may miss critical auditory cues, increasing safety risks and reducing independence.

**PrioritySound addresses this problem by detecting, prioritizing, and visually representing important sounds in real time.**

---

# Key Features

PrioritySound combines machine learning and accessible design to deliver intelligent sound detection.

### Live Sound Detection
Continuously monitors microphone input to detect environmental sounds in real time.

### Machine Learning Classification
Uses trained deep learning models to classify different types of sounds.

### Priority-Based Alerts
Sounds are categorized by urgency:

- 🔴 **Emergency**
- 🟠 **High**
- 🟡 **Medium**
- 🟢 **Low**

Color-coded alerts help users quickly understand the importance of a sound.

### Real-Time Dashboard
A visual dashboard displays:

- Current sound alerts
- Priority levels
- Detection history

The interface is designed to be clear and accessible for Deaf and Hard-of-Hearing users.

### Augmented Reality Sound Mapping
PrioritySound overlays sound alerts onto a **live webcam feed**, helping users understand where sounds are coming from.

### Customizable Modes
Users can switch between environment-specific modes that adjust sound priorities and alert behavior.

---

# Software Architecture

PrioritySound is built using a modern web and machine learning stack.

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- Flask
- SQLAlchemy

**Machine Learning**
- Transformers
- TensorFlow
- NumPy

**Audio Processing**
- SoundDevice

---

# Audio Classification

The system uses a **transformer-based audio classification model** that:

- Analyzes audio spectral features
- Identifies sound categories
- Assigns confidence scores to predictions
- Automatically prioritizes sounds based on urgency

Priority levels include:

- Emergency
- High
- Medium
- Low

The model is trained on diverse environmental audio datasets including:

- Alarms
- Sirens
- Household appliances
- Human-generated sounds

This ensures reliable detection across many environments.

---

# Augmented Reality Sound Mapping

PrioritySound includes a web-based **AR visualization system** that helps users locate sounds in their environment.

The system:

- Displays sound alerts on a live camera feed
- Estimates sound direction (Left, Center, Right)
- Uses color-coded indicators to show urgency

This provides spatial awareness and helps users quickly respond to important events.

---

# Environment Modes

PrioritySound includes four customizable modes that adjust sound priorities depending on the user's environment.

### Parent Mode
Prioritizes sounds such as:

- Baby crying
- Glass breaking
- Door knocks
- Smoke alarms

### Outside Mode
Prioritizes:

- Emergency sirens
- Car horns
- Traffic alerts

### School Mode
Prioritizes:

- Lockdown alarms
- Fire alarms
- School bells

### Home Mode
Prioritizes:

- Doorbells
- Appliance alarms
- Security alerts

Each mode filters out low-importance noise and ensures users receive the most relevant alerts.

---
## Installation

1. Clone the repository:
   ```
   git clone https://github.com/shreshmello/PrioritySound.git
   cd software-design-code
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000` to access the web dashboard.

## Usage

- **Web Interface**: Register or log in to access the dashboard. Start detection to begin monitoring sounds.
- **Console Mode**: Run `python main.py` for a command-line version of the application.
- **Configuration**: Adjust user preferences in the settings to customize alert behaviors.

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Machine Learning**: Transformers, TesorFlow, NumPy
- **Audio Processing**: SoundDevice
- **Frontend**: HTML, CSS, JavaScript

## Citation

```bibtex
@software{huggingface_transformers,
  title     = {Transformers: State-of-the-Art Natural Language Processing},
  author    = {Wolf, Thomas and Debut, Lysandre and Sanh, Victor and Chaumond, Julien and Delangue, Clement and Moi, Anthony and Cistac, Pierric and Rault, Tim and Louf, R{\'e}mi and Funtowicz, Morgan and Davison, Joe and Shleifer, Sam and von Platen, Patrick and Ma, Clara and Jernite, Yacine and Plu, Julien and Xu, Canwen and Le Scao, Teven and Gugger, Sylvain and Drame, Mariama and Lhoest, Quentin and Rush, Alexander},
  year      = {2019},
  publisher = {Hugging Face},
  url       = {https://github.com/huggingface/transformers},
  note      = {Versioned software library for natural language processing; includes pipeline API}
}
@article{emergencies_risk_perception_dhh,
  title   = {Risk perception and perceived self-efficacy of deaf and hard-of-hearing seniors and young adults in emergencies},
  author  = {Rosenblum, L. D. and others},
  journal = {Disability and Health Journal},
  year    = {2019},
  volume  = {12},
  number  = {3},
  pages   = {425--431},
  doi     = {10.1016/j.dhjo.2019.01.001},
  url     = {https://pubmed.ncbi.nlm.nih.gov/}
}
@article{traffic_hearing_impaired_safety,
  title   = {Self-reported experiences of incidents and injury events in traffic among hearing impaired people as pedestrians and cyclists: A follow-up study of mobility and use of hearing equipment},
  author  = {Iwarsson, S. and others},
  journal = {Accident Analysis \& Prevention},
  year    = {2012},
  volume  = {49},
  pages   = {419--424},
  doi     = {10.1016/j.aap.2012.02.007},
  url     = {https://pubmed.ncbi.nlm.nih.gov/}
}
@article{ar_household_sounds_dhh,
  title   = {Augmented-Reality Presentation of Household Sounds for Deaf and Hard-of-Hearing People},
  author  = {Kudo, K. and others},
  journal = {Sensors},
  year    = {2020},
  volume  = {20},
  number  = {5},
  pages   = {1409},
  doi     = {10.3390/s20051409},
  publisher = {MDPI},
  url     = {https://www.mdpi.com/}
}
```

## License

This project is open-source. Please check the license file for details.



