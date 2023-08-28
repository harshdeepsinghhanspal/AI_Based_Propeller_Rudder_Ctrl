import cv2
import mediapipe as mp
import serial

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize Serial
ser = serial.Serial('COM3', 9600)  # Update with your Arduino's serial port

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Extract index finger and thumb landmarks
            index_finger = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Map landmarks to servo positions (between 0 and 180)
            index_finger_pos = int(index_finger.y * 180)
            thumb_pos = int(thumb.y * 180)

            # Send positions to Arduino
            ser.write(f"{index_finger_pos} {thumb_pos}\n".encode())

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
