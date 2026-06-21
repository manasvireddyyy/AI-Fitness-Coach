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
feedback = ""

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
        shoulder_landmark = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow_landmark = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist_landmark = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        # Check visibility
        if (
            shoulder_landmark.visibility > 0.3 and
            elbow_landmark.visibility > 0.3 and
            wrist_landmark.visibility > 0.3 and
            hip_landmark.visibility > 0.3
        ):

            shoulder = [shoulder_landmark.x, shoulder_landmark.y]
            elbow = [elbow_landmark.x, elbow_landmark.y]
            wrist = [wrist_landmark.x, wrist_landmark.y]

            body_angle = abs(
                shoulder_landmark.y - hip_landmark.y
            )
            print("Body Angle:", body_angle)

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle < 30:
                continue

            print("Angle:", angle)

            if body_angle > 0.30:
                feedback = "GET INTO PUSHUP POSITION"
                # stage = None

            else:

                if angle > 165:
                    feedback = "PUSH UP"

                elif angle > 80:
                    feedback = "GO LOWER"

                else:
                    feedback = "GOOD PUSHUP"

                # Pushup counter logic
               # Pushup counter logic
                if angle > 160:
                    if stage == "DOWN":
                        counter += 1
                        print("REP COUNTED:", counter)

                    stage = "UP"
                    print("STAGE = UP")

                elif angle < 80:
                    stage = "DOWN"
                    print("STAGE = DOWN")

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
                    int(elbow[0] * frame.shape[1]),
                    int(elbow[1] * frame.shape[0])
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # Squat logic
            if angle > 160:
                if stage == "DOWN":
                    counter += 1
                stage = "UP"

            elif angle < 80:
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
    cv2.rectangle(frame, (0, 0), (450, 250), (245, 117, 16), -1)
    cv2.putText(
        frame,
        "Pushups ",
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
    cv2.putText(
    frame,
    "FEEDBACK",
    (15, 150),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
    )

    if feedback == "GOOD PUSHUP":
        feedback_color = (0, 255, 0)      # Green

    elif feedback == "PUSH PUSHUP":
        feedback_color = (0, 255, 255)    # Yellow

    elif feedback == "BAD PUSHUP":
        feedback_color = (0, 0, 255)      # Red

    else:
        feedback_color = (255, 255, 255)  # White

    cv2.putText(
        frame,
        feedback,
        (15, 210),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        feedback_color,
        2
    )

    cv2.imshow("AI Fitness Coach - Push Ups", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()