import cv2
import mediapipe as mp
import time
import controller

# use cv2 call webcam function then store variable. preset is 0.
cap = cv2.VideoCapture(0)

# use hands, face_mesh and painting unit in mediapipe framework
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
drawing_utils = mp.solutions.drawing_utils

# hands_point
tipID = [4, 8, 12, 16, 20]

# detection
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
face = mp_face_mesh.FaceMesh(static_image_mode=False, min_tracking_confidence=0.6, min_detection_confidence=0.6)

# setting face, hands point and line style 
hand_landmark_style = drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=3)
hand_connect_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=3)
face_landmark_style = drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=1)
face_connect_style = drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=3)

pTime = 0
cTime = 0

while True:
    frame, img = cap.read()
    if frame:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hands_result = hands.process(imgRGB)
        img_height = img.shape[1]
        img_width = img.shape[0]

        # hands
        landmark_list = []
        if hands_result.multi_hand_landmarks:
            for hand_landmark in hands_result.multi_hand_landmarks:
                drawing_utils.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS, hand_landmark_style, hand_connect_style)
                # mark number
                for i, landmark in enumerate(hand_landmark.landmark):
                    x_position = int(landmark.x * img_height)
                    y_position = int(landmark.y * img_width)
                    landmark_list.append([i, x_position, y_position])
                    cv2.putText(img, str(i), (x_position-25, y_position+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
                    print(i, x_position, y_position)

                    # change single point
                    # if i == 4:
                    #     cv2.circle(img, (xPos, yPos), 20, (166, 56, 56), cv2.FILLED)
                    # print(i, xPos, yPos)

        # fingers
        fingers = []
        if len(landmark_list) != 0:
            if landmark_list[tipID[0]][1] >= landmark_list[tipID[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for i in range(1,5):
                if landmark_list[tipID[i]][2] <= landmark_list[tipID[i]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)
            controller.led(total)
            if total == 0:
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),)
                cv2.putText(img, "0", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            if total == 1:
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),)
                cv2.putText(img, "1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            if total == 2:
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),)
                cv2.putText(img, "2", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            if total == 3:
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),)
                cv2.putText(img, "3", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            if total == 4:
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),)
                cv2.putText(img, "4", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            if total == 5:
                cv2.rectangle(img, (20, 300), (270, 425), (0, 255, 0),)
                cv2.putText(img, "5", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)                


        # face
        face_result = face.process(imgRGB)
        if face_result.multi_face_landmarks:
            for i in face_result.multi_face_landmarks:
                # print(i.landmark[0].y*480)
                drawing_utils.draw_landmarks(img, i, mp_face_mesh.FACEMESH_CONTOURS, face_landmark_style)

        # FPS setting
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
