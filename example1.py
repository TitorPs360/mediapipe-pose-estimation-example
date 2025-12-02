import cv2
import mediapipe as mp

# Initialize
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Read image
image = cv2.imread('person2.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process
with mp_pose.Pose(static_image_mode=True) as pose:
    results = pose.process(image_rgb)

    # Draw landmarks
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=8, circle_radius=6),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=4)
        )

        # Print landmark positions
        print("Detected landmarks:")
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            print(f"Landmark {idx}: x={landmark.x:.3f}, y={landmark.y:.3f}, z={landmark.z:.3f}")

# Display
cv2.imshow('Pose Detection', image)
cv2.imwrite('out.png', image)
cv2.waitKey(0)
cv2.destroyAllWindows()