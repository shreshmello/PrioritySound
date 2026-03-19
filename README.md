![Logo](docs/PrioritySoundLogo.png)

# PrioritySound – Real-Time Sound Awareness for Deaf and Hard-of-Hearing Users

## Overview

**PrioritySound** is a real-time sound awareness system designed to help Deaf and Hard-of-Hearing individuals detect and understand important environmental sounds.  

Using machine learning, PrioritySound continuously monitors surrounding audio, identifies important sounds, and displays visual alerts that indicate both **the type of sound and where it is coming from**.

The goal is to improve **safety, awareness, and independence** by ensuring that critical sounds are never missed.

---

# Problem Statement

Over **1.5 billion people worldwide** experience some degree of hearing loss [^1]. Many of these individuals face challenges detecting important environmental sounds such as:

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

As a result, Deaf and Hard-of-Hearing individuals may miss critical auditory cues, increasing safety risks and reducing independence [^2] [^3].

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

PrioritySound includes a web-based **AR visualization system** that helps users locate sounds in their environment [^4].

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
- **Machine Learning**: Transformers, TensorFlow, NumPy
- **Audio Processing**: SoundDevice
- **Frontend**: HTML, CSS, JavaScript

## Citation

[^1]: World Health Organization. (2021). *World report on hearing*. https://www.who.int/publications/i/item/world-report-on-hearing

[^2]: Rosenblum, L. D., et al. (2019). Risk perception and perceived self-efficacy of deaf and hard-of-hearing seniors and young adults in emergencies. *Disability and Health Journal, 12*(3), 425–431. https://doi.org/10.1016/j.dhjo.2019.01.001

[^4]: Kudo, K., et al. (2020). Augmented-Reality Presentation of Household Sounds for Deaf and Hard-of-Hearing People. *Sensors, 20*(5), 1409. https://doi.org/10.3390/s20051409

```bibtex
@software{huggingface_transformers,
  title     = {Transformers: State-of-the-Art Natural Language Processing},
  author    = {Wolf, Thomas and Debut, Lysandre and Sanh, Victor and Chaumond, Julien and Delangue, Clement and Moi, Anthony and Cistac, Pierric and Rault, Tim and Louf, R{\'e}mi and Funtowicz, Morgan and Davison, Joe and Shleifer, Sam and von Platen, Patrick and Ma, Clara and Jernite, Yacine and Plu, Julien and Xu, Canwen and Le Scao, Teven and Gugger, Sylvain and Drame, Mariama and Lhoest, Quentin and Rush, Alexander},
  year      = {2019},
  publisher = {Hugging Face},
  url       = {https://github.com/huggingface/transformers},
  note      = {Versioned software library for natural language processing; includes pipeline API}
}
@software{flask,
  title     = {Flask},
  author    = {Ronacher, Armin},
  year      = {2010},
  publisher = {Pallets},
  url       = {https://flask.palletsprojects.com/},
  note      = {A lightweight WSGI web application framework}
}
@software{sqlalchemy,
  title     = {SQLAlchemy},
  author    = {Bayer, Michael},
  year      = {2006},
  publisher = {SQLAlchemy Authors},
  url       = {https://www.sqlalchemy.org/},
  note      = {The Python SQL Toolkit and Object Relational Mapper}
}
@software{sounddevice,
  title     = {SoundDevice},
  author    = {Hofmann, Matthias},
  year      = {2016},
  publisher = {Python Software Foundation},
  url       = {https://python-sounddevice.readthedocs.io/},
  note      = {Play and Record Sound with Python}
}
@software{pytorch,
  title     = {PyTorch},
  author    = {Paszke, Adam and Gross, Sam and Massa, Francisco and Lerer, Adam and Bradbury, James and Chanan, Gregory and Killeen, Trevor and Lin, Zeming and Gimelshein, Natalia and Antiga, Luca and Desmaison, Alban and Kopf, Andreas and Yang, Edward and DeVito, Zachary and Raison, Martin and Tejani, Alykhan and Chilamkurthy, Sasank and Steiner, Benoit and Fang, Lu and Bai, Junjie and Chintala, Soumith},
  year      = {2019},
  publisher = {Linux Foundation},
  url       = {https://pytorch.org/},
  note      = {An open source machine learning framework}
}
@software{numpy,
  title     = {NumPy},
  author    = {Harris, Charles R. and Millman, K. Jarrod and van der Walt, St{\'e}fan J. and Gommers, Ralf and Virtanen, Pauli and Cournapeau, David and Wieser, Eric and Taylor, James and Berg, Sebastian and Smith, Nathaniel J. and Kern, Robert and Picus, Matti and Hoyer, Stephan and van Kerkwijk, Marten H. and Brett, Matthew and Haldane, Allan and del R{\'i}o, Jaime Fern{\'a}ndez and Wiebe, Mark and Peterson, Pearu and G{\'e}rard-Marchant, Pierre and Sheppard, Kevin and Reddy, Tyler and Weckesser, Warren and Abbasi, Hameer and Gohlke, Christoph and Oliphant, Travis E.},
  year      = {2020},
  publisher = {NumPy Developers},
  url       = {https://numpy.org/},
  note      = {Fundamental package for array computing in Python}
}
@software{tensorflow,
  title     = {TensorFlow},
  author    = {Abadi, Mart{\'i}n and Agarwal, Ashish and Barham, Paul and Brevdo, Eugene and Chen, Zhifeng and Citro, Craig and Corrado, Greg S. and Davis, Andy and Dean, Jeffrey and Devin, Matthieu and Ghemawat, Sanjay and Goodfellow, Ian and Harp, Andrew and Irving, Geoffrey and Isard, Michael and Jia, Yangqing and Jozefowicz, Rafal and Kaiser, Lukasz and Kudlur, Manjunath and Levenberg, Josh and Man{\'e}, Dan and Monga, Rajat and Moore, Sherry and Murray, Derek and Olah, Chris and Schuster, Mike and Shlens, Jonathon and Steiner, Benoit and Sutskever, Ilya and Talwar, Kunal and Tucker, Paul and Vanhoucke, Vincent and Vasudevan, Vijay and Vi{\'e}gas, Fernanda and Vinyals, Oriol and Warden, Pete and Wattenberg, Martin and Wicke, Martin and Yu, Yuan and Zheng, Xiaoqiang},
  year      = {2015},
  publisher = {Google Brain Team},
  url       = {https://www.tensorflow.org/},
  note      = {An end-to-end open source machine learning platform}
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





