import cv2
import mediapipe as mp
import pyautogui

def control_ocular():
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[1:4]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    amplification_factor = 1  # Valores menores a 1 desplaza Up Left y valores mayores Down Right
                    screen_x = screen_w * landmark.x * amplification_factor
                    screen_y = screen_h * landmark.y * amplification_factor
                    pyautogui.moveTo(screen_x, screen_y)

            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

            right = [landmarks[374], landmarks[386]]
            for landmark in right:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))

            if ((left[0].y - left[1].y) or (right[0].y - right[1].y)) < 0.004:
                pyautogui.click()
                pyautogui.sleep(1)

        cv2.imshow('Eye Controlled Mouse', frame)
        cv2.waitKey(1)

control_ocular()