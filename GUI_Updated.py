from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QDialog, QMessageBox, QHBoxLayout, QFrame, QWidget)
from PyQt5.QtCore import Qt, QTimer
import sys
import cv2
import mediapipe as mp

camera_img = r"C:\Users\cmbajay8\OneDrive - Ansell Healthcare\Desktop\Gayanga\Img\cam.png"
play_img = r"C:\Users\cmbajay8\OneDrive - Ansell Healthcare\Desktop\Gayanga\Img\play.png"
stop_img = r"C:\Users\cmbajay8\OneDrive - Ansell Healthcare\Desktop\Gayanga\Img\stop.png"
log_in_img = r"C:\Users\cmbajay8\OneDrive - Ansell Healthcare\Desktop\Gayanga\Img\log.png"

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(700)
        self.setMinimumWidth(1366)
        self.setWindowTitle("Measuring GUI")

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(128, 128, 128))
        self.setPalette(palette)

        # Create the menu bar
        menu_bar = self.menuBar()

        # Track the log in
        self.is_logged_in = False

        self.file_menu = menu_bar.addMenu("File")
        self.new_action_1 = QAction("Log In", self)
        self.file_menu.addAction(self.new_action_1)
        self.new_action_2 = QAction("Log Out", self)
        self.file_menu.addAction(self.new_action_2)
        self.new_action_3 = QAction("Exit", self)
        self.file_menu.addAction(self.new_action_3)

        self.run_menu = menu_bar.addMenu("Run")
        self.run_action_1 = QAction("Run All", self)
        self.run_menu.addAction(self.run_action_1)

        self.edit_menu = menu_bar.addMenu("Edit")

        self.setting_menu = menu_bar.addMenu("Setting")
        self.action_1 = QAction("General Setting", self)
        self.setting_menu.addAction(self.action_1)
        self.action_2 = QAction("Camera Setting", self)
        self.setting_menu.addAction(self.action_2)
        self.action_3 = QAction("Other", self)
        self.setting_menu.addAction(self.action_3)

        self.help_menu = menu_bar.addMenu("Help")
        self.open_pdf_action = QAction("User Manual", self)
        self.help_menu.addAction(self.open_pdf_action)

        # Connect Log In action to the login window
        self.new_action_1.triggered.connect(self.show_log_in_window)
        self.new_action_2.triggered.connect(self.log_out_window)

        self.central_widget = QWidget()  # Define central widget
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        # Content Area
        self.content_area = QFrame()  # Define content area
        self.content_area.setFrameShape(QFrame.StyledPanel)
        self.content_area.setStyleSheet("background-color: #404040; border: 1px solid black;")

        # Add a QLabel to the content area to display the camera feed
        self.camera_label = QLabel(self.content_area)
        self.camera_label.setAlignment(Qt.AlignCenter)
        content_area_layout = QVBoxLayout()
        content_area_layout.addWidget(self.camera_label)
        self.content_area.setLayout(content_area_layout)

        # Right Sidebar
        self.right_sidebar = QFrame()
        self.right_sidebar.setFrameShape(QFrame.StyledPanel)
        self.right_sidebar.setFixedWidth(450)  # Sidebar width

        right_sidebar_layout = QVBoxLayout()

        # Top Section
        self.top_section = QFrame()
        self.top_section.setFrameShape(QFrame.StyledPanel)
        self.top_section.setStyleSheet("background-color: #404040; border-bottom: 1px solid black;")
        self.top_section.setFixedHeight(300)  # Fixed height for section

        # Middle Section
        self.middle_section = QFrame()
        self.middle_section.setFrameShape(QFrame.StyledPanel)
        self.middle_section.setStyleSheet("background-color: #404040; border-bottom: 1px solid black;")
        self.middle_section.setFixedHeight(100)  #

        # Bottom Section (Toolbar for image editing tools)
        self.bottom_section = QFrame()
        self.bottom_section.setFrameShape(QFrame.StyledPanel)
        self.bottom_section.setStyleSheet("background-color: #404040;border-bottom: 1px solid black;")

        # Add image editing tools to the bottom section
        self.play_button = QPushButton(self.bottom_section)
        pixmap = QPixmap(play_img)
        if pixmap.isNull():
            print("Error: Play icon not found.")
        else:
            self.play_button.setIcon(QIcon(pixmap))  # Use QIcon to set the icon
            self.play_button.setIconSize(pixmap.size())
        self.play_button.clicked.connect(self.start_camera)  # Connect to start_camera

        self.capture_button = QPushButton(self.bottom_section)
        pixmap = QPixmap(camera_img)
        if pixmap.isNull():
            print("Error: Camera icon not found.")
        else:
            self.capture_button.setIcon(QIcon(pixmap))  # Use QIcon to set the icon
            self.capture_button.setIconSize(pixmap.size())
        self.capture_button.clicked.connect(self.capture_image)  # Connect to capture_image

        self.stop_button = QPushButton(self.bottom_section)
        pixmap = QPixmap(stop_img)
        if pixmap.isNull():
            print("Error: Stop icon not found.")
        else:
            self.stop_button.setIcon(QIcon(pixmap))  # Use QIcon to set the icon
            self.stop_button.setIconSize(pixmap.size())
        self.stop_button.clicked.connect(self.stop_camera)  # Connect to stop_camera

        # Layout for bottom section (toolbar)
        bottom_section_layout = QHBoxLayout()
        bottom_section_layout.addWidget(self.play_button)
        bottom_section_layout.addWidget(self.capture_button)
        bottom_section_layout.addWidget(self.stop_button)
        self.bottom_section.setLayout(bottom_section_layout)

        # Add sections to right sidebar layout
        right_sidebar_layout.addWidget(self.top_section)
        right_sidebar_layout.addWidget(self.middle_section)
        right_sidebar_layout.addWidget(self.bottom_section)

        self.right_sidebar.setLayout(right_sidebar_layout)

        # Adding widgets to the content layout
        content_layout.addWidget(self.content_area, 1)  # Content area with stretch
        content_layout.addWidget(self.right_sidebar)  # Right sidebar

        # Layout for top section
        top_section_layout = QVBoxLayout()

        # Add the "Result" label
        self.label_7 = QLabel("Results", self.top_section)
        font = self.label_7.font()  # Get the current font of the label
        font.setPointSize(25)
        self.label_7.setFont(font)  # Apply the font to the label
        self.label_7.setStyleSheet("color: white; font-weight: bold;")
        top_section_layout.addWidget(self.label_7)

        # Add a horizontal layout for "gesture type" and its variation
        gesture_layout = QHBoxLayout()
        self.gesture_type_label = QLabel("Finger Up Count  ", self.top_section)
        self.gesture_type_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        self.gesture_type_value = QLabel("", self.top_section)  # Placeholder for gesture type value
        self.gesture_type_value.setStyleSheet("color: white; font-size: 16px;")
        gesture_layout.addWidget(self.gesture_type_label)
        gesture_layout.addWidget(self.gesture_type_value)
        top_section_layout.addLayout(gesture_layout)

        # Add a horizontal layout for "person_id" and its variation
        person_layout = QHBoxLayout()
        self.person_id_label = QLabel("Person Name  ", self.top_section)
        self.person_id_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        self.person_id_value = QLabel("Person1", self.top_section)  # Placeholder for person ID value
        self.person_id_value.setStyleSheet("color: white; font-size: 16px;")
        person_layout.addWidget(self.person_id_label)
        person_layout.addWidget(self.person_id_value)
        top_section_layout.addLayout(person_layout)

        # Add the "Offline" label
        self.label_10 = QLabel("Offline", self.top_section)
        font = self.label_10.font()  # Get the current font of the label
        font.setPointSize(20)
        self.label_10.setFont(font)  # Apply the font to the label
        self.label_10.setStyleSheet("color: white; font-weight: bold;")
        self.label_10.setAlignment(Qt.AlignCenter)
        top_section_layout.addWidget(self.label_10)

        # Set the layout for the top section
        self.top_section.setLayout(top_section_layout)

        # Layout for middle section
        middle_section_layout = QVBoxLayout()
        self.label_9 = QLabel("Online", self.middle_section)
        font = self.label_9.font()  # Get the current font of the label
        font.setPointSize(20)
        self.label_9.setFont(font)  # Apply the font to the label
        self.label_9.setStyleSheet("color: white; font-weight: bold;")
        self.label_9.setAlignment(Qt.AlignCenter)
        middle_section_layout.addWidget(self.label_9)
        self.middle_section.setLayout(middle_section_layout)

        # Adding content layout to main layout
        main_layout.addLayout(content_layout)

        self.central_widget.setLayout(main_layout)

        # Disable all menus and icons after initializing all UI elements
        self.disable_menus()

        # Camera-related variables
        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Initialize MediaPipe Hands and FaceMesh
        self.hands = mp.solutions.hands.Hands(max_num_hands=4)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    def disable_menus(self):
        for menu in [self.run_menu, self.edit_menu, self.setting_menu, self.help_menu]:
            for action in menu.actions():
                action.setDisabled(True)
        self.new_action_2.setDisabled(True)  # Disable Log Out
        self.new_action_3.setDisabled(True)  # Disable Exit
        self.play_button.setEnabled(False)  # Disable play button
        self.capture_button.setEnabled(False)  # Disable capture button
        self.stop_button.setEnabled(False)  # Disable stop button

    def enable_menus(self):
        for menu in [self.run_menu, self.edit_menu, self.setting_menu, self.help_menu]:
            for action in menu.actions():
                action.setDisabled(False)
        self.new_action_2.setDisabled(False)  # Enable Log Out
        self.new_action_3.setDisabled(False)  # Enable Exit
        self.play_button.setEnabled(True)  # Enable play button
        self.capture_button.setEnabled(True)  # Enable capture button
        self.stop_button.setEnabled(True)  # Enable stop button

    def show_log_in_window(self):
        log_in_window = LogIn()
        if log_in_window.exec_() == QDialog.Accepted:
            self.enable_menus()  # Enable menus after successful login

    def log_out_window(self):
        self.is_logged_in = False
        self.disable_menus()
        QMessageBox.information(self, "Logged Out", "You have been logged out.")

    def start_camera(self):
        try:
            # Initialize the camera
            self.capture = cv2.VideoCapture(0)
            
            # Check if the camera was successfully opened
            if self.capture is None or not self.capture.isOpened():
                QMessageBox.warning(self, "Camera Error", "Unable to open camera.")
                return
            
            # Start the timer to update the frame
            self.timer.start(30)  # Update every 30 ms
            self.play_button.setEnabled(False)  # Disable play button
            self.stop_button.setEnabled(True)  # Enable stop button
        except Exception as e:
            QMessageBox.warning(self, "Camera Error", f"An error occurred: {str(e)}")

    def stop_camera(self):
        if hasattr(self, 'capture') and self.capture is not None and self.capture.isOpened():
            self.timer.stop()
            self.capture.release()
            self.play_button.setEnabled(True)  # Enable play button
            self.stop_button.setEnabled(False)  # Disable stop button

    def capture_image(self):
        if hasattr(self, 'capture') and self.capture is not None and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                cv2.imwrite("captured_image.png", frame)
                QMessageBox.information(self, "Image Captured", "The image has been saved as 'captured_image.png'.")

    def update_frame(self):
        if hasattr(self, 'capture') and self.capture is not None and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                # Flip the frame horizontally for a mirror effect
                frame = cv2.flip(frame, 1)

                # Convert the frame to RGB format
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect hand landmarks
                hand_landmark_points = self.hands.process(rgb_frame).multi_hand_landmarks
                if hand_landmark_points:
                    for hand_landmarks in hand_landmark_points:
                        # Draw hand landmarks and connections
                        self.draw_hand_landmarks_and_connections(frame, hand_landmarks)

                        # Count the number of fingers that are up
                        landmarks = hand_landmarks.landmark
                        finger_count = self.count_fingers(landmarks)
                        self.gesture_type_value.setText(str(finger_count))  # Update finger count in the UI

                # Detect eye landmarks
                eye_landmark_points = self.face_mesh.process(rgb_frame).multi_face_landmarks
                if eye_landmark_points:
                    for eye_landmarks in eye_landmark_points:
                        # Extract and draw eye landmarks (left and right eyes)
                        left_eye_indices = [33, 133]  # Example indices for left eye
                        right_eye_indices = [362, 263]  # Example indices for right eye
                        left_eye = [eye_landmarks.landmark[i] for i in left_eye_indices]
                        right_eye = [eye_landmarks.landmark[i] for i in right_eye_indices]

                        # Draw eye landmarks
                        self.draw_eye_landmarks(frame, left_eye, frame.shape[1], frame.shape[0])
                        self.draw_eye_landmarks(frame, right_eye, frame.shape[1], frame.shape[0])

                # Convert the frame to RGB format for display in PyQt
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # Set the pixmap to display the image
                self.camera_label.setPixmap(QPixmap.fromImage(qt_image))

    def draw_hand_landmarks_and_connections(self, frame, hand_landmarks):
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            hand_landmarks,
            mp.solutions.hands.HAND_CONNECTIONS,
            mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2)
        )

    def draw_eye_landmarks(self, frame, eye_landmarks, frame_w, frame_h):
        for landmark in eye_landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)  # Draw eye landmarks as blue circles

    def count_fingers(self, landmarks):
        finger_tips = [4, 8, 12, 16, 20]  # Landmark indices for finger tips
        finger_bases = [3, 6, 10, 14, 18]  # Landmark indices for finger bases
        finger_count = 0

        for tip, base in zip(finger_tips, finger_bases):
            if landmarks[tip].y < landmarks[base].y:  # Finger is up if tip is above base
                finger_count += 1

        return finger_count


# Log In Window
class LogIn(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setMinimumHeight(300)
        self.setMinimumWidth(400)

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(0, 0, 205))
        self.setPalette(palette)

        # Icon label
        self.icon_label = QLabel(self)
        pixmap = QPixmap(log_in_img)  # Use the camera_img path
        if pixmap.isNull():
            print("Error: Image not found.")
        else:
            self.icon_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Labels and inputs
        self.log_in_name_label = QLabel("Log In")
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)
        self.log_in_name_label.setFont(font)
        self.log_in_name_label.setAlignment(Qt.AlignCenter)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Buttons
        self.login_button = QPushButton("Log In")
        self.cancel_button = QPushButton("Cancel")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.log_in_name_label)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        # Button styles
        self.login_button.setStyleSheet("background-color: blue; color: white; border-radius: 5px; padding: 10px;")
        self.cancel_button.setStyleSheet("background-color: blue; color: white; border-radius: 5px; padding: 10px;")

        # Connect buttons
        self.login_button.clicked.connect(self.on_login)
        self.cancel_button.clicked.connect(self.reject)

    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "1" and password == "1":
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())