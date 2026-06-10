# AI Fitness Coach 🏋️‍♀️

An AI-powered fitness coach built using Python, OpenCV, and MediaPipe that performs real-time human pose estimation and squat repetition counting through computer vision.

## Features

* Real-time webcam feed
* Human pose detection
* Skeleton tracking
* Knee angle calculation
* Squat detection
* Automatic repetition counting
* Visibility-based filtering for improved accuracy

## Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy

## How It Works

The application tracks the hip, knee, and ankle landmarks using MediaPipe Pose. The knee angle is calculated in real time to determine squat movement stages (UP/DOWN). A repetition is counted whenever a complete squat cycle is detected.

## Future Improvements

* Push-up counter
* Lunge counter
* Form correction feedback
* Voice-based rep counting
* Calorie estimation
* Streamlit web interface

## Run Locally

```bash
pip install -r requirements.txt
python main.py
```
