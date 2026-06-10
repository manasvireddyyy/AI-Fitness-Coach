import cv2
import mediapipe as mp
import numpy as np


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


# MediaPipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()

# Counter variables
counter = 0
stage = None

# Camera
cap = cv2.VideoCapture(0)

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        # Right leg landmarks
        hip_landmark = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        knee_landmark = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        ankle_landmark = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Check visibility
        if (
            hip_landmark.visibility > 0.8 and
            knee_landmark.visibility > 0.8 and
            ankle_landmark.visibility > 0.8
        ):

            hip = [hip_landmark.x, hip_landmark.y]
            knee = [knee_landmark.x, knee_landmark.y]
            ankle = [ankle_landmark.x, ankle_landmark.y]

            angle = calculate_angle(hip, knee, ankle)

            # Angle display
            cv2.putText(
                frame,
                f"Angle: {int(angle)}",
                (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )

            # Angle near knee
            cv2.putText(
                frame,
                str(int(angle)),
                (
                    int(knee[0] * frame.shape[1]),
                    int(knee[1] * frame.shape[0])
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # Squat logic
            if angle > 165:
                if stage == "DOWN":
                    counter += 1
                stage = "UP"

            elif angle < 100:
                stage = "DOWN"

            # Draw skeleton
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        else:
            cv2.putText(
                frame,
                "POSITION YOUR WHOLE BODY",
                (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

    # Dashboard
    cv2.rectangle(frame, (0, 0), (250, 180), (245, 117, 16), -1)

    cv2.putText(
        frame,
        "REPS",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        str(counter),
        (15, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        3
    )

    cv2.putText(
        frame,
        "STAGE",
        (120, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        str(stage),
        (120, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        3
    )

    cv2.imshow("AI Fitness Coach", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()