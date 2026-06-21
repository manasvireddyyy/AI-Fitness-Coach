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
        ankle_landmark = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Check visibility
        if (
            shoulder_landmark.visibility > 0.6 and
            elbow_landmark.visibility > 0.6 and
            wrist_landmark.visibility > 0.6 and
            hip_landmark.visibility > 0.6 and
            ankle_landmark.visibility > 0.6
        ):

            shoulder = [shoulder_landmark.x, shoulder_landmark.y]
            elbow = [elbow_landmark.x, elbow_landmark.y]
            wrist = [wrist_landmark.x, wrist_landmark.y]
            hip = [hip_landmark.x, hip_landmark.y]
            ankle = [ankle_landmark.x, ankle_landmark.y]

            body_line_angle = calculate_angle(
            shoulder,
            hip,
            ankle
            )

            if body_line_angle < 100:
                continue

            print("Body Line:", body_line_angle)

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle < 30:
                continue

            print("Angle:", angle)

            # Check if body is in pushup position
            body_line_angle = calculate_angle(
                shoulder,
                hip,
                ankle
            )

            # print("Body Line:", body_line_angle)
            print(
                f"Body:{body_line_angle:.1f}  Elbow:{angle:.1f}  Stage:{stage}"
            )

            if body_line_angle < 110:

                feedback = "GET INTO PUSHUP POSITION"
                # stage = None

            else:

                if angle > 160:
                    feedback = "PUSH UP"

                elif angle > 80:
                    feedback = "GO LOWER"

                else:
                    feedback = "GOOD PUSHUP"

                if angle > 160:
                    print("UP DETECTED")

                    if stage == "DOWN":
                        counter += 1
                        print("REP COUNTED:", counter)

                    stage = "UP"

                elif angle < 80:

                    stage = "DOWN"
                    print("DOWN DETECTED")
                
                pushup_depth = False

                if angle < 70:
                    pushup_depth = True
                    stage = "DOWN"

                if angle > 160 and stage == "DOWN" and pushup_depth:
                    counter += 1
                    pushup_depth = False
           
            # Angle display
            progress = int((180- angle)/(180-40)*100)
            progress = max(0,min(progress,100))
            cv2.putText(
                frame,
                f"Progress: {progress}%",
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
        feedback_color = (0, 255, 0)

    elif feedback == "GO LOWER":
        feedback_color = (0, 255, 255)

    elif feedback == "PUSH UP":
        feedback_color = (0, 0, 255)

    else:
        feedback_color = (255, 255, 255)

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