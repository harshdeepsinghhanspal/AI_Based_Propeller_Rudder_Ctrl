import cv2
import mediapipe as mp
import serial

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize Serial Communication with Arduino
arduino = serial.Serial('COM8', 9600)  # Change 'COM3' to the correct port

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Get the landmarks of thumb and index fingers
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Get the x and y coordinates
            thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
            index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])

            # Draw circles at thumb and index finger tips
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)

            # Map the finger positions to servo angles (adjust as needed)
            servo1_angle = int(90 - (thumb_x / frame.shape[1]) * 90)
            servo2_angle = int((index_y / frame.shape[1]) * 90)

            # Send servo angles to Arduino
            arduino.write(f"{servo1_angle} {servo2_angle}\n".encode())

    # Display the frame
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
