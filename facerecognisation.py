import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

# Load and encode known faces
path = 'images'
images = []
classNames = []
for cl in os.listdir(path):
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)

# Attendance logging
def markAttendance(name):
    with open('attendance.csv', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        names = [line.split(',')[0] for line in lines]
        if name not in names:
            now = datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{name},{dtString}\n')

# GUI App
class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance")
        self.root.geometry("700x600")
        self.root.configure(bg='white')

        self.label = tk.Label(root, text="Face Recognition Attendance", font=("Arial", 20), bg='white')
        self.label.pack(pady=10)

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.start_button = tk.Button(root, text="Start Camera", command=self.start_camera, bg='green', fg='white', font=('Arial', 12))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Camera", command=self.stop_camera, bg='red', fg='white', font=('Arial', 12))
        self.stop_button.pack(pady=10)

        self.cap = None
        self.running = False

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.process_frame()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='')

    def process_frame(self):
        if not self.running:
            return

        success, img = self.cap.read()
        if not success:
            return

        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                markAttendance(name)

                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgPIL = Image.fromarray(imgRGB)
        imgtk = ImageTk.PhotoImage(image=imgPIL)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.video_label.after(10, self.process_frame)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceAttendanceApp(root)
    root.mainloop()
