import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    radians = math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x)
    angle = abs(radians * 180.0 / math.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# Get video
cap = cv2.VideoCapture('pushup_video.mov')
# cap = cv2.VideoCapture(0) # or if you want webcam

# Counting variable
counter = 0
stage = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process
        results = pose.process(image)

        # Convert back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates (base on left arm)
            shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            # Calculate elbow abgle
            angle = calculate_angle(shoulder, elbow, wrist)

            # Logic to count
            if angle > 160:
                stage = "up"
            if angle < 90 and stage == "up":
                stage = "down"
                counter += 1
                print(f"Push-ups: {counter}")
        except:
            pass

        # Setup status box
        cv2.rectangle(image, (0, 0), (300, 100), (245, 117, 16), -1)

        # Rep data
        cv2.putText(image, 'REPS', (15, 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                   (15, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (150, 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, stage if stage else '', 
                   (150, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Angle data
        cv2.putText(image, f'Angle: {int(angle) if "angle" in locals() else 0}',
			        (10, 130),
			        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Draw landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
        
        # Display
        cv2.imshow('Push-up Counter', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

print(f"\nTotal Push-ups: {counter}")