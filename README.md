![Logo](docs/PrioritySoundLogo.png)

# PrioritySound -– Real-Time Sound Awareness for the Deaf and Hard-of-Hearing

## Problem Statement 

Over 1.5 billion people worldwide experience some degree of hearing loss, with many facing significant challenges in perceiving critical environmental sounds. These sounds—such as alarms, sirens, door knocks, or a baby crying—play an essential role in safety, awareness, and daily functioning. Existing assistive solutions often fall short because they:
- Treat all sounds equally without prioritizing urgency
- Deliver delayed or unreliable notifications
- Lack intuitive, real-time visual interfaces
- Do not provide spatial awareness of where sounds originate

As a result, Deaf and Hard-of-Hearing individuals may miss time-sensitive auditory cues, increasing safety risks, reducing independence, and causing stress in everyday situations.

There is a need for a system that can intelligently detect, prioritize, and visually represent environmental sounds in real time, while also conveying where those sounds are coming from in a clear and accessible way. 

## Our Solution and Key Features

PrioritySound uses machine learning to deliver intelligent sound detection and accessibility:
- **Live Sound Detection**: Constantly monitors microphone input to analyze sounds consistently
- **Machine Learning Classification**: Uses trained deep learning models to identify and label environmental sounds
- **Priority-Based Alerts**: Categorizes sounds as Emergency, High, Medium, or Low based on safety risk
- **Real-Time Dashboard**: Displays visual alerts, status, and activity history optimized for deaf and hard-of-hearing users
- **AR Visual Sound Mapping**: Overlays directional alerts onto a live webcam feed to help users locate sounds
- **Customizable Modes**: Adjusts priorities and alert styles based on user context (Parent, Outside, School, Home)

## Software Technology

Priority Sound is built by integrating...
- CSS: for UI design and styling
- HTML: page structure
- Javascript: Frontend
- Python: Backend
- Machine Learning Model: Sound classification

## How It Works
 PrioritySound uses machine learning to:
1. Detect live audio input from a microphone
2. Classify sounds into categories
3. Assign priority levels (Emergency, High, Medium, Low)
4. Display alerts in real time

## Audio Classification

PrioritySound uses machine-learning to classify environmental sounds in real time. Built on transformer-based architecture, the system:
- Analyzes audio spectral features to identify sound types
- Assigns confidence scores to each classification
- Automatically prioritizes sounds based on urgency levels (Emergency, High, Medium, Low)
- Continuously learns and adapts to new environmental contexts

The model is trained on diverse sound datasets including alarms, sirens, appliances, and human-generated sounds, ensuring reliable detection across various environments.

## Augmented Reality Sound Mapping

A web-based AR feature that overlays detected sounds onto a live webcam feed. The system:
- Estimates sound direction (Left, Center, Right)
- Displays color-coded visual indicators based on urgency
- Example: Red alert for sirens, yellow notification for door knocks
- Provides spatial awareness for users to locate sounds in their environment

## Modes

PrioritySound includes four customizable environment modes that adjust sound prioritization based on context:

Available Modes:
- **Parent Mode**: Prioritizes baby crying, glass breaking, door knocks, and smoke alarms
- **Outside Mode**: Prioritizes emergency sirens, car horns, and traffic alerts
- **School Mode**: Prioritizes lockdown alarms, fire alarms, and school bells
- **Home Mode**: Prioritizes doorbells, appliance alarms, and security alerts

Each mode automatically adjusts priority levels, alert styles, and filters out low-importance noise for relevant, timely alerts.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/shreshmello/software-design-code.git
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



