*Facial Recognition Attendance Management System.*


This project is a Facial Recognition-based Attendance Management System developed using Python. The system utilizes advanced facial recognition algorithms and OpenCV for real-time face detection and attendance logging, providing a secure and efficient way to manage attendance. The system integrates with MySQL for database management, allowing seamless record-keeping, and supports CSV export for logging attendance records.

Key Features
Face Detection and Recognition: The system captures and processes faces using OpenCV and the face_recognition library, encoding the facial features for matching.
Attendance Logging: Attendance is automatically logged in a MySQL database. Once a person is recognized, their name and the time of attendance are stored, and a confirmation popup is displayed.
Blink Detection: To prevent spoofing through photos, the system incorporates a blink detection mechanism. It calculates the Eye Aspect Ratio (EAR) using facial landmarks to detect whether a person has blinked before logging attendance.
Real-time Camera Feed: The system captures a live video feed and processes each frame to detect and recognize faces, providing real-time feedback and updating attendance status.
User-friendly Interface: A Tkinter-based graphical user interface (GUI) provides an intuitive display of the attendance log and real-time video feed. The GUI allows users to view the attendance records in a table format.
CSV Export: Attendance records are also saved in a CSV file for offline access, ensuring data persistence even outside the database.
Face Encoding Storage: Detected faces are saved as encoded data for future recognition, making it easier to compare and recognize the same person over multiple sessions.
Technical Stack
Programming Language: Python
Libraries:
OpenCV for real-time video processing
face_recognition for face detection and recognition
MySQL Connector for database interactions
Tkinter for the GUI
PIL (Python Imaging Library) for image handling in the interface
SciPy for blink detection (Eye Aspect Ratio calculation)
Database: MySQL for storing attendance logs
CSV Logging: Saves attendance records in CSV format for easy reference and reporting.
Workflow
Database Setup: The MySQL database is connected, and a table (Atnd) is created if it does not exist. This table stores the name of the individual and the time their attendance was marked.
Face Encoding: Faces from known individuals are pre-processed and encoded. These encodings are used for comparing and recognizing faces from the live video feed.
Live Feed Processing: The camera feed is processed in real-time, detecting and recognizing faces in each frame.
Blink Detection: To ensure a valid presence, the system checks if the detected person blinks before logging attendance.
Attendance Logging: Once a person is successfully recognized and passes the blink detection test, their attendance is logged in both the MySQL database and a CSV file.
Real-time GUI: The GUI displays a live video feed on one side and an attendance log on the other, making it easy to monitor the process.
Installation and Setup
Clone the Repository:


git clone https://github.com/nyxisback/Facial-Recognition-Attendance-Management.git

Install Dependencies:


pip install -r requirements.txt
Configure MySQL Database:
Set up MySQL locally with a database named Attendance.
Update the host, user, password, and database in the code to match your MySQL credentials.
Run the Application:


python attendance_system.py
Future Enhancements
Mobile App Integration: Extend the project by developing a mobile app that can interface with the system and display attendance data on the go.
Cloud Integration: Shift database operations to a cloud platform like AWS or Firebase for better scalability and remote accessibility.
Multi-Camera Support: Enable the system to support multiple cameras for larger venues or classrooms.
