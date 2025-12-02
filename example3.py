import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def draw_stick_figure(image, landmarks):
    h, w, c = image.shape

    def to_pixel(landmark):
        return (int(landmark.x * w), int(landmark.y * h))
    
    # Get landmarks
    nose = landmarks[mp_pose.PoseLandmark.NOSE]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

    color = (0, 100, 255)  # Orange
    thickness = 24

    # Calculate head size from shoulder width
    shoulder_width = abs(left_shoulder.x - right_shoulder.x) * w
    head_radius = int(shoulder_width * 0.4)

    # Calculate center of body
    neck_x = (left_shoulder.x + right_shoulder.x) / 2
    neck_y = (left_shoulder.y + right_shoulder.y) / 2
    
    hip_center_x = (left_hip.x + right_hip.x) / 2
    hip_center_y = (left_hip.y + right_hip.y) / 2

    # Convert to pixel
    neck_pixel = (int(neck_x * w), int(neck_y * h))
    hip_center_pixel = (int(hip_center_x * w), int(hip_center_y * h))

    # Put head above neck
    head_center_x = neck_x
    head_center_y = neck_y - (head_radius + thickness) / h
    head_center_pixel = (int(head_center_x * w), int(head_center_y * h))

    # Draw main body (neck to hip)
    cv2.line(image, neck_pixel, hip_center_pixel, color, thickness)

    # Draw arms (with elbows)
    cv2.line(image, neck_pixel, to_pixel(left_elbow), color, thickness)
    cv2.line(image, to_pixel(left_elbow), to_pixel(left_wrist), color, thickness)
    cv2.line(image, neck_pixel, to_pixel(right_elbow), color, thickness)
    cv2.line(image, to_pixel(right_elbow), to_pixel(right_wrist), color, thickness)

    # Draw legs (with knees)
    cv2.line(image, hip_center_pixel, to_pixel(left_knee), color, thickness)
    cv2.line(image, to_pixel(left_knee), to_pixel(left_ankle), color, thickness)
    cv2.line(image, hip_center_pixel, to_pixel(right_knee), color, thickness)
    cv2.line(image, to_pixel(right_knee), to_pixel(right_ankle), color, thickness)

    # Draw head
    cv2.circle(image, head_center_pixel, head_radius, color, thickness)

# Read webcam
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        white_canvas = np.ones((h, w, 3), dtype=np.uint8) * 255  # White background

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw stick figure on white canvas
        if results.pose_landmarks:
            draw_stick_figure(white_canvas, results.pose_landmarks.landmark)

        cv2.imshow('Stick Figure', white_canvas)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()