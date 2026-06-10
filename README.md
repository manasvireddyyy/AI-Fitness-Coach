# AI Fitness Coach 🏋️‍♀️  version 1

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
<img width="216" height="123" alt="Screenshot 2026-06-10 at 10 38 55 PM" src="https://github.com/user-attachments/assets/8a7192f1-ae8c-4c6c-be39-d45487379c80" />
