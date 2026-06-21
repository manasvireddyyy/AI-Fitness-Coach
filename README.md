# AI Fitness Coach

AI Fitness Coach is a computer vision-based fitness tracking application built using Python, OpenCV, and MediaPipe. The system analyzes body posture in real time through a webcam and provides exercise counting, progress tracking, and form feedback.

## Features

* Real-time pose detection using MediaPipe
* Squat counter with posture feedback
* Push-up counter with progress tracking
* Exercise selection menu
* Real-time visual feedback
* Progress percentage tracking
* Experimental skipping counter
* Live webcam-based monitoring

## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy

## Project Structure

```text
AI-Fitness-Coach/
│
├── main.py
├── pushup.py
├── requirements.txt
├── README.md
└── assets/
```

## How It Works

The application uses MediaPipe Pose Estimation to detect key body landmarks such as shoulders, elbows, hips, knees, and ankles. Joint angles are calculated using geometric relationships between landmarks to determine exercise form and repetition counts.

### Squat Detection

* Tracks lower body movement
* Provides form feedback
* Counts completed repetitions

### Push-Up Detection

* Tracks elbow flexion and extension
* Validates push-up position
* Calculates progress percentage
* Counts completed repetitions

### Skipping Detection (Experimental)

* Detects jumping motion using ankle movement
* Provides real-time feedback
* Currently under development

## Installation

Clone the repository:

```bash
git clone https://github.com/manasvireddyyy/AI-Fitness-Coach.git
cd AI-Fitness-Coach
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Future Improvements

* Workout history tracking
* Calorie estimation
* Improved skipping detection
* Exercise analytics dashboard
* Web deployment
* Mobile application support

## Author

Manasvi Reddy

## Version History

### V1.0

* Basic squat counter

### V2.0

* Squat feedback system

### V3.0

* Push-up counter implementation

### V4.0

* Exercise selection menu

### V5.0

* Experimental skipping counter
* Improved project structure
* Enhanced exercise tracking

<img width="238" height="156" alt="Screenshot 2026-06-21 at 10 56 00 PM" src="https://github.com/user-attachments/assets/d2871e23-117d-4b41-81d9-4d96733f436c" />


<img width="511" height="324" alt="Screenshot 2026-06-21 at 10 58 39 PM" src="https://github.com/user-attachments/assets/0b7e13b4-fbd8-4a0f-b144-33241623dfd0" />



