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
        self.stage = None
        self.count = 0
        self.finished_rep = None


def pose_detection(exercise: Exercise, img):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as pose:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
                exercise.stage = "start"

            if end_condition and exercise.stage == "start":
                exercise.stage = "end"
                exercise.count += 1
                exercise.finished_rep = time.time()

        except Exception as e:
            print(e)

        if exercise.finished_rep and (time.time() - exercise.finished_rep) < 0.3:
            color = (0, 255, 0)
        elif exercise.stage == "start":
            color = (0, 255, 255)
        else:
            color = (245, 66, 230)

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
        )

        cv2.putText(
            image,
            f"Contagem: {exercise.count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    return image, exercise.count
