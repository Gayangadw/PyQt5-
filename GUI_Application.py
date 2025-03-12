from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QDialog, QMessageBox, QHBoxLayout, QFrame, QWidget)
from PyQt5.QtCore import Qt, QTimer
import sys
import cv2

camera_img = r"D:\Internship\PyQt5\camera.png"  # Replace with the actual path to your camera icon
image_path = r"D:\Internship\PyQt5\log.png"


# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumHeight(1080)
        self.setMinimumWidth(1920)
        self.setWindowTitle("Measuring GUI")

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(128, 128, 128))
        self.setPalette(palette)

        # Create the menu bar
        menu_bar = self.menuBar()

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

        # Disable all menu actions except Log In
        self.disable_menus()

        self.central_widget = QWidget()  # Define central widget
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        self.left_sidebar = QFrame()
        self.left_sidebar.setFrameShape(QFrame.StyledPanel)
        self.left_sidebar.setStyleSheet("background-color:#404040; border: 1px solid black;")
        self.left_sidebar.setFixedWidth(150)  # Sidebar width

        # Camera icon (clickable QLabel)
        self.camera_icon = QLabel(self.left_sidebar)
        pixmap = QPixmap(camera_img)
        if pixmap.isNull():
            print("Error: Camera icon not found.")
        else:
            self.camera_icon.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
        self.camera_icon.setAlignment(Qt.AlignCenter)
        self.camera_icon.mousePressEvent = self.open_camera  # Make the icon clickable

        # Layout for left sidebar
        left_sidebar_layout = QVBoxLayout()
        left_sidebar_layout.addWidget(self.camera_icon)
        self.left_sidebar.setLayout(left_sidebar_layout)

        # Content Area
        self.content_area = QFrame()  # Define content area
        self.content_area.setFrameShape(QFrame.StyledPanel)
        self.content_area.setStyleSheet("background-color:	#404040; border: 1px solid black;")

        # Right Sidebar
        self.right_sidebar = QFrame()
        self.right_sidebar.setFrameShape(QFrame.StyledPanel)
        self.right_sidebar.setFixedWidth(450)  # Sidebar width

        right_sidebar_layout = QVBoxLayout()

        # Top Section
        self.top_section = QFrame()
        self.top_section.setFrameShape(QFrame.StyledPanel)
        self.top_section.setStyleSheet("background-color: #404040; border-bottom: 1px solid black;")
        self.top_section.setFixedHeight(540)  # Fixed height for section

        # Bottom Section
        self.bottom_section = QFrame()
        self.bottom_section.setFrameShape(QFrame.StyledPanel)
        self.bottom_section.setStyleSheet("background-color: #404040;border-bottom: 1px solid black;")

        # Add sections to right sidebar layout
        right_sidebar_layout.addWidget(self.top_section)
        right_sidebar_layout.addWidget(self.bottom_section)

        self.right_sidebar.setLayout(right_sidebar_layout)

        # Adding widgets to the content layout
        content_layout.addWidget(self.left_sidebar)  # Left sidebar
        content_layout.addWidget(self.content_area, 1)  # Content area with stretch
        content_layout.addWidget(self.right_sidebar)  # Right sidebar

        # Label on top of the right sidebar's top section
        self.label_7 = QLabel("Result", self.top_section)
        font = self.label_7.font()  # Get the current font of the label
        font.setPointSize(36)
        self.label_7.setFont(font)  # Apply the font to the label
        self.label_7.setStyleSheet("color: white; font-weight: bold;")
        self.label_7.setAlignment(Qt.AlignCenter)

        # Layout for top section
        top_section_layout = QVBoxLayout()
        top_section_layout.addWidget(self.label_7)
        self.top_section.setLayout(top_section_layout)

        # Adding content layout to main layout
        main_layout.addLayout(content_layout)

        self.central_widget.setLayout(main_layout)

    def disable_menus(self):
        """Disable all menu items except Log In."""
        for menu in [self.run_menu, self.edit_menu, self.setting_menu, self.help_menu]:
            for action in menu.actions():
                action.setDisabled(True)
        self.new_action_2.setDisabled(True)  # Disable Log Out
        self.new_action_3.setDisabled(True)  # Disable Exit
        # self.camera_icon.setDisabled(True)

    def enable_menus(self):
        """Enable all menu items after a successful login."""
        for menu in [self.run_menu, self.edit_menu, self.setting_menu, self.help_menu]:
            for action in menu.actions():
                action.setDisabled(False)
        self.new_action_2.setDisabled(False)  # Enable Log Out
        self.new_action_3.setDisabled(False)  # Enable Exit
        # self.camera_icon.setDisabled(False)

    def show_log_in_window(self):
        """Display the login window."""
        log_in_window = LogIn()
        if log_in_window.exec_() == QDialog.Accepted:
            self.enable_menus()  # Enable menus after successful login

    def open_camera(self, event):
        """Open the webcam feed in the content area."""
        self.camera_window = CameraWindow(self.content_area)
        self.camera_window.show()


class CameraWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Store the parent (content_area)
        self.setFixedSize(parent.width(), parent.height())  # Match the size of the content area
        self.layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        # Start video capture
        self.capture = cv2.VideoCapture(0)

        # Timer for updating the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms

    def update_frame(self):
        """Update the camera frame."""
        ret, frame = self.capture.read()
        if ret:
            # Resize the frame to fit the content area
            frame = cv2.resize(frame, (self.width(), self.height()))

            # Convert the frame to RGB format
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = rgb_image.shape
            qt_image = QImage(rgb_image.data, width, height, width * 3, QImage.Format_RGB888)

            # Set the pixmap to display the image
            self.label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        """Release the camera when the window is closed."""
        self.capture.release()
        event.accept()


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
        pixmap = QPixmap(image_path)  # Use the camera_img path
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