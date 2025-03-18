import cv2
import mediapipe as mp

# Initialize Webcam
def initialize_camera():
    return cv2.VideoCapture(0)

# Initialize MediaPipe Hands
def initialize_hands():
    return mp.solutions.hands.Hands(max_num_hands=4)

# Initialize MediaPipe FaceMesh for eye detection
def initialize_face_mesh():
    return mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Process frame and detect hand landmarks
def detect_hand_landmarks(hands, frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return hands.process(rgb_frame).multi_hand_landmarks

# Process frame and detect eye landmarks
def detect_eye_landmarks(face_mesh, frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_mesh.process(rgb_frame).multi_face_landmarks

# Draw landmarks and connections on the hand
def draw_hand_landmarks_and_connections(frame, hand_landmarks):
    mp.solutions.drawing_utils.draw_landmarks(
        frame,
        hand_landmarks,
        mp.solutions.hands.HAND_CONNECTIONS,
        mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2)
)

# Draw eye landmarks
def draw_eye_landmarks(frame, eye_landmarks, frame_w, frame_h):
    for landmark in eye_landmarks:
        x = int(landmark.x * frame_w)
        y = int(landmark.y * frame_h)
        cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)  # Draw eye landmarks as blue circles

# Count the number of fingers that are up
def count_fingers(landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Landmark indices for finger tips
    finger_bases = [3, 6, 10, 14, 18]  # Landmark indices for finger bases
    finger_count = 0

    for tip, base in zip(finger_tips, finger_bases):
        if landmarks[tip].y < landmarks[base].y:  # Finger is up if tip is above base
            finger_count += 1

    return finger_count

# Main function
def main():
    cam = initialize_camera()
    hands = initialize_hands()
    face_mesh = initialize_face_mesh()

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror effect
        frame_h, frame_w, _ = frame.shape

        # Detect hand landmarks
        hand_landmark_points = detect_hand_landmarks(hands, frame)
        if hand_landmark_points:
            for hand_landmarks in hand_landmark_points:
                # Draw hand landmarks and connections
                draw_hand_landmarks_and_connections(frame, hand_landmarks)

                # Count the number of fingers that are up
                landmarks = hand_landmarks.landmark
                finger_count = count_fingers(landmarks)
                cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Detect eye landmarks
        eye_landmark_points = detect_eye_landmarks(face_mesh, frame)
        if eye_landmark_points:
            for eye_landmarks in eye_landmark_points:
                # Extract and draw eye landmarks (left and right eyes)
                left_eye_indices = [33, 133]  # Example indices for left eye
                right_eye_indices = [362, 263]  # Example indices for right eye
                left_eye = [eye_landmarks.landmark[i] for i in left_eye_indices]
                right_eye = [eye_landmarks.landmark[i] for i in right_eye_indices]

                # Draw eye landmarks
                draw_eye_landmarks(frame, left_eye, frame_w, frame_h)
                draw_eye_landmarks(frame, right_eye, frame_w, frame_h)

        cv2.imshow('Hand and Eye Landmarks', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cam.release()
    cv2.destroyAllWindows()

# Run the program
if __name__ == "__main__":
    main()