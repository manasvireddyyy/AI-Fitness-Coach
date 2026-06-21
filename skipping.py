import cv2
import mediapipe as mp
import time

# MediaPipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()

# Variables
counter = 0
stage = "GROUND"
feedback = "READY"
last_rep_time = 0

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

        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        if (
            left_ankle.visibility > 0.6 and
            right_ankle.visibility > 0.6
        ):

            avg_y = (
                left_ankle.y +
                right_ankle.y
            ) / 2

            ankle_diff = abs(
                left_ankle.y -
                right_ankle.y
            )

            # print("Ankle Height:", avg_y)
            cv2.putText(
                frame,
                f"Y:{avg_y:.2f}",
                (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )
            # print("Ankle Difference:", ankle_diff)

            # ---------------------------
            # SKIPPING LOGIC
            # ---------------------------

            if avg_y < 0.82 and ankle_diff < 0.03:

                stage = "AIR"
                feedback = "JUMPING"

            elif avg_y > 0.87:

                if stage == "AIR":

                    current_time = time.time()

                    if current_time - last_rep_time > 0.6:

                        counter += 1
                        last_rep_time = current_time

                        print("SKIP:", counter)

                stage = "GROUND"
                feedback = "READY"

            # Draw skeleton
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        else:

            feedback = "SHOW FEET"

    # Dashboard
    cv2.rectangle(frame, (0, 0), (450, 250), (245, 117, 16), -1)

    cv2.putText(
        frame,
        "SKIPPING",
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
        stage,
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

    if feedback == "JUMPING":
        feedback_color = (0, 255, 0)

    elif feedback == "READY":
        feedback_color = (0, 255, 255)

    else:
        feedback_color = (0, 0, 255)

    cv2.putText(
        frame,
        feedback,
        (15, 210),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        feedback_color,
        2
    )

    cv2.imshow("AI Fitness Coach - Skipping", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()