import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)

mp_face_mesh = mp.solutions.face_mesh
drawing_utils = mp.solutions.drawing_utils

face_landmark_style = drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=1)
face_connect_style = drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=3)

face = mp_face_mesh.FaceMesh(static_image_mode=False, min_tracking_confidence=0.6, min_detection_confidence=0.6)

while True:
    frame, img = cap.read()
    if frame:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_result = face.process(imgRGB)
        if face_result.multi_face_landmarks:
            for i in face_result.multi_face_landmarks:
                # print(i.landmark[0].y*480)
                drawing_utils.draw_landmarks(img, i, mp_face_mesh.FACEMESH_CONTOURS, face_landmark_style, face_connect_style)

        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
