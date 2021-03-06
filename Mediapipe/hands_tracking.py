import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
drawing_utils = mp.solutions.drawing_utils

# detection
hands = mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6)

hand_landmark_style = drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=3)
hand_connect_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=3)

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
        if hands_result.multi_hand_landmarks:
            for hand_landmark in hands_result.multi_hand_landmarks:
                drawing_utils.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS, hand_landmark_style, hand_connect_style)
                # mark number
                for i, landmark in enumerate(hand_landmark.landmark):
                    x_position = int(landmark.x * img_height)
                    y_position = int(landmark.y * img_width)
                    cv2.putText(img, str(i), (x_position-25, y_position+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
                    print(i, x_position, y_position)

                    # change single point
                    # if i == 4:
                    #     cv2.circle(img, (xPos, yPos), 20, (166, 56, 56), cv2.FILLED)
                    # print(i, xPos, yPos)

        # FPS setting
        # cTime = time.time()
        # fps = 1/(cTime-pTime)
        # pTime = cTime
        # cv2.putText(img, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
