import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.FAILSAFE = False

print("3초 안에 PPT 슬라이드 쇼 화면 클릭하세요")
time.sleep(3)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cooldown = 0

while True:
    ret, img = cap.read()
    if not ret:
        continue

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if cooldown > 0:
        cooldown -= 1

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        lm = hand.landmark

        index_up = lm[8].y < lm[6].y
        middle_up = lm[12].y < lm[10].y

        # 👆 검지 = 다음
        if index_up and not middle_up and cooldown == 0:
            print("다음 슬라이드")
            pyautogui.press("space")  # ⭐ PPT에서 가장 안정
            cooldown = 20

        # ✌ 브이 = 이전
        elif index_up and middle_up and cooldown == 0:
            print("이전 슬라이드")
            pyautogui.press("left")
            cooldown = 20

    cv2.imshow("카메라", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()