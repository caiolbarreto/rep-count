# pose_detection.py
import cv2
import time
import mediapipe as mp
from helpers import calculate_angles, get_joints_for_movement, draw_angle


class Exercise:
    def __init__(self, name, start_angle, finish_angle):
        self.name = name
        self.start_angle = start_angle
        self.finish_angle = finish_angle


exercises = [
    Exercise(name="biceps_curl", start_angle=130, finish_angle=30),
    Exercise(name="shoulder_press", start_angle=70, finish_angle=150),
    Exercise(name="squat", start_angle=170, finish_angle=120),
]


def pose_detection(exercise: Exercise):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    count = 0
    stage = None
    cap = cv2.VideoCapture(0)
    finished_rep = None

    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        while cap.isOpened():
            _, frame = cap.read()

            frame = cv2.flip(frame, 1)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                left_joints, right_joints = get_joints_for_movement(
                    landmarks, mp_pose, exercise
                )

                left_angle = calculate_angles(left_joints)
                right_angle = calculate_angles(right_joints)

                draw_angle(image, left_angle, left_joints)
                draw_angle(image, right_angle, right_joints)

                if exercise.start_angle > exercise.finish_angle:
                    start_condition = (
                        left_angle > exercise.start_angle
                        and right_angle > exercise.start_angle
                    )
                    end_condition = (
                        left_angle < exercise.finish_angle
                        and right_angle < exercise.finish_angle
                    )
                else:
                    start_condition = (
                        left_angle < exercise.start_angle
                        and right_angle < exercise.start_angle
                    )
                    end_condition = (
                        left_angle > exercise.finish_angle
                        and right_angle > exercise.finish_angle
                    )

                if start_condition:
                    stage = "start"

                if end_condition and stage == "start":
                    stage = "end"
                    count += 1
                    finished_rep = time.time()

            except:
                pass

            if finished_rep and time.time() - finished_rep < 0.3:
                color = (0, 255, 0)
            elif stage == "start":
                color = (0, 255, 255)
            else:
                color = (245, 66, 230)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(245, 117, 66), thickness=2, circle_radius=2
                ),
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
            )

            cv2.putText(
                image,
                f"Contagem: {count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow("Mediapipe Feed", image)

            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    return count
