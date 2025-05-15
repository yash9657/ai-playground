import cv2
import mediapipe as mp
import webbrowser

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def fingers_up(hand_landmarks):
    tips       = [4, 8, 12, 16, 20]
    pip_joints = [2, 6, 10, 14, 18]
    f = []
    # thumb: pointing sideways
    f.append(hand_landmarks.landmark[tips[0]].x 
             < hand_landmarks.landmark[pip_joints[0]].x)
    # other fingers: tip above PIP → extended
    for i in range(1,5):
        f.append(
          hand_landmarks.landmark[tips[i]].y 
          < hand_landmarks.landmark[pip_joints[i]].y
        )
    return f  # [thumb, idx, mid, ring, pinky]

def is_w_gesture_new(hand_landmarks):
    thumb, idx, mid, ring, pinky = fingers_up(hand_landmarks)
    # index & pinky up; thumb, middle, ring down
    if idx and pinky and not thumb and mid and ring:
        lm = hand_landmarks.landmark
        # 1) check index–pinky spread
        spread = abs(lm[8].x - lm[20].x)
        # 2) check middle–ring are close together
        close_mid_ring = abs(lm[12].x - lm[16].x)
        if spread > 0.20 and close_mid_ring < 0.05:
            return True
    return False

cap = cv2.VideoCapture(0)
video_opened = False
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hl in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)
                if is_w_gesture_new(hl):
                    if not video_opened:
                        webbrowser.open("https://www.youtube.com/watch?v=rzRqEWJYwX4&ab_channel=IceCubeVEVO&t=11s")
                        video_opened = True
                    # Center the text and make it larger
                    text = "Westside Bestside Babayyy"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 2
                    thickness = 4
                    color = (200, 0, 0)
                    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
                    frame_height, frame_width = frame.shape[:2]
                    x = (frame_width - text_width) // 2
                    y = (frame_height + text_height) // 2
                    cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)

        cv2.imshow("Westside Detector", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

cap.release()
cv2.destroyAllWindows()
