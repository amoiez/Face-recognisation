Face Recognition Attendance System 📷✅
This project is a Python-based Face Recognition Attendance System with a Graphical User Interface (GUI) built using Tkinter. It uses the OpenCV and face_recognition libraries to detect and recognize faces in real-time through your webcam, automatically marking attendance in a CSV file.

🚀 Features
✅ Real-time face detection via webcam

🧠 Face encoding and recognition using face_recognition

📂 Automatically logs recognized faces with timestamp in attendance.csv

🖼️ User-friendly GUI with Start/Stop camera buttons

📸 Easy integration of new users by adding images to the images/ folder

🛠️ How It Works
Known Faces:
The app loads all images from the images/ folder, encodes them, and stores their names for recognition.

Live Camera Feed:
Once the camera is started, it captures frames and checks for known faces.

Face Recognition & Logging:
If a face is recognized, it draws a bounding box with the name and logs the name with the current timestamp in attendance.csv.

🧾 File Structure
bash
Copy
Edit
├── images/               # Folder containing known faces (name.jpg/png)
├── attendance.csv        # Automatically created and updated with logs
├── main.py               # Main script to run the GUI app
🖥️ Requirements
Python 3.x

OpenCV (cv2)

face_recognition

numpy

Pillow

tkinter (comes with Python)

Install dependencies with:

bash
Copy
Edit
pip install opencv-python face_recognition numpy Pillow
📷 How to Use
Add clear face images to the images/ folder. File name = person’s name.

Run the script:

bash
Copy
Edit
python main.py
Use the GUI to start/stop the camera.

Recognized faces will be logged in attendance.csv.

