import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    # opencv 에서는 사진을 BGR 순서로 저장한다. 
    # mp.hands는 RGB를 받으므로 이를 RGB로 바꿔준다.
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks: # 손이 인식되면 좌표값을 반환한다.
        for hand_lms in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_lms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                # landmark는 반환 값으로 전체 이미지에서 위치의 비율값을 반환한다.
                # 따라서 반환 값에 이미지의 크기를 곱하면 좌표의 픽셀 값을 구할 수 있다.
                
                if id == 15 or id == 12:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    # 원을 그린다.
                    # 응용하면 특정 마디만 표시할 수 있다.
                    # cv2.circle(그릴 이미지, 위치(x, y), 원 크기, 색, 채울지 말지)
                
            #mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            
    # mp_hands.HAND_CONNECTIONS: 점사이의 선을 잇는데 사용한다.
    
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # cv2.putText(이미지, 표시할 텍스트, 위치, 폰트, 폰트 스케일, 색, 두께)
    
    cv2.imshow("Image", img)
    ret = cv2.waitKey(1) # 입력 값 ms초 동안 입력이 없으면 다음 줄로 넘어간다. 0을 넣으면 무한대기 입력한 키의 ASCIII 코드가 반환
    if ret == 27:
        break