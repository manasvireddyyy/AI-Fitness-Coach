import mediapipe as mp

print("MediaPipe:", mp.__version__)
print("Solutions:", hasattr(mp, "solutions"))

pose = mp.solutions.pose

print("SUCCESS!")