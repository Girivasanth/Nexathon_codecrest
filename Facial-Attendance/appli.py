import mysql.connector
import cv2
import numpy as np
import face_recognition
import os
import csv
from datetime import datetime
from scipy.spatial import distance as dist
import time
from tkinter import Tk, Label, Frame, Toplevel, Scrollbar
from tkinter import ttk
from PIL import Image, ImageTk

# Database connection and setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password= "root",
    database= "attendance"
)

cursor = db.cursor()

# Create the SQL table if not exists    
cursor.execute(
    '''CREATE TABLE IF NOT EXISTS Atnd (
        Name VARCHAR(255),
        Time VARCHAR(255)
    )'''
)

def markatnd(name):
    cursor.execute("SELECT Name FROM Atnd WHERE Name = %s", (name,))
    result = cursor.fetchone()
    
    if result is None:
        now = datetime.now()
        dateString = now.strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
        dtString = now.strftime('%H:%M:%S')
        cursor.execute("INSERT INTO Atnd (Name, Time) VALUES (%s, %s)", (name, dateString+" "+dtString))
        db.commit()
        update_table_display()
        save_to_csv(name)
        popup = Toplevel(root)
        popup.title("Attendance")
        popup.geometry("250x100")
        Label(popup, text=f"Attendance marked for {name} at {dtString}", padx=20, pady=20).pack()
        root.after(1000, popup.destroy)
    else:
        print(f"{name} is already marked for today.")

def save_to_csv(name):
    with open(r'C:\Users\HARISH KUMAR V\Desktop\Attendance\attendance_log.csv', 'r+') as f:
        datlist = f.readlines()
        nlist = []
        for line in datlist:
            ent = line.split(',')
            nlist.append(ent[0])
        if name not in nlist:
            now = datetime.now()
            dateString = now.strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
            timeString = now.strftime('%H:%M:%S')  # Format: HH:MM:SS
            f.writelines(f'\n{name},{dateString},{timeString}')

def update_table_display():
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("SELECT * FROM Atnd")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def close_db_connection():
    cursor.close()
    db.close()

path = r"C:\Users\HARISH KUMAR V\Desktop\Attendance\faces_known"
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for person in myList:
    personFolder = os.path.join(path, person)
    if os.path.isdir(personFolder):
        for imgName in os.listdir(personFolder):
            imgPath = os.path.join(personFolder, imgName)
            curImg = cv2.imread(imgPath)
            if curImg is not None:
                images.append(curImg)
                classNames.append(person)
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def detect_blink(landmarks):
    leftEye = landmarks['left_eye']
    rightEye = landmarks['right_eye']
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0
    return ear

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

BLINK_THRESHOLD = 0.3
CONSEC_FRAMES = 3
BLINK_COOLDOWN = 3

blink_counter = 0
blinked = False
last_blink_time = time.time()
ear_history = []

save_folder = r"C:\Users\HARISH KUMAR V\Desktop\Attendance\saved"

def show_frame():
    global blink_counter, blinked, last_blink_time, ear_history
    success, img = cap.read()
    if not success:
        root.after(10, show_frame)
        return

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    faceLandmarksList = face_recognition.face_landmarks(imgS)

    for encodeFace, faceLoc, landmarks in zip(encodesCurFrame, facesCurFrame, faceLandmarksList):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        cords = (0, 255, 0)

        if faceDis[matchIndex] < 0.50:
            name = classNames[matchIndex].upper()
            ear = detect_blink(landmarks)
            leftEye = np.array(landmarks['left_eye'])
            rightEye = np.array(landmarks['right_eye'])

            leftEyeX, leftEyeY = leftEye[:, 0], leftEye[:, 1]
            rightEyeX, rightEyeY = rightEye[:, 0], rightEye[:, 1]

            cv2.rectangle(img, (min(leftEyeX) * 4, min(leftEyeY) * 4), (max(leftEyeX) * 4, max(leftEyeY) * 4), (0, 255, 0), 2)
            cv2.rectangle(img, (min(rightEyeX) * 4, min(rightEyeY) * 4), (max(rightEyeX) * 4, max(rightEyeY) * 4), (0, 255, 0), 2)

            ear_history.append(ear)
            if len(ear_history) > CONSEC_FRAMES:
                ear_history.pop(0)
            
            avg_ear = sum(ear_history) / len(ear_history)

            if avg_ear < BLINK_THRESHOLD:
                blink_counter += 1
            else:
                if blink_counter >= CONSEC_FRAMES and (time.time() - last_blink_time) > BLINK_COOLDOWN:
                    blinked = True
                    last_blink_time = time.time()
                blink_counter = 0

            if blinked:
                print(f"Blink detected for: {name}")
                markatnd(name)
                save_path = os.path.join(save_folder, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.npy")
                np.save(save_path, encodeFace)
                save_to_csv(name)
                print(f"Encoding saved for {name} at {save_path}")
                blinked = False
        else:
            name = 'Unknown'
            cords = (0, 0, 255)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), cords, 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), cords, cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

root = Tk()
root.title("Attendance System")
root.geometry("1200x600") 

root.grid_columnconfigure(0, weight=1) 
root.grid_columnconfigure(1, weight=2) 

left_frame = Frame(root, width=400, height=500, bg='white')
left_frame.grid(row=0, column=0, padx=10, pady=2, sticky="nsew")

right_frame = Frame(root, width=800, height=480, bg='white')
right_frame.grid(row=0, column=1, padx=10, pady=2, sticky="nsew")

Label(left_frame, text="Attendance Log", font=('Arial', 16)).pack()

columns = ('Name', 'Time')
tree = ttk.Treeview(left_frame, columns=columns, show='headings')
tree.heading('Name', text='Name', anchor='w')
tree.heading('Time', text='Time', anchor='w')
tree.column('Name', anchor='w', width=150)
tree.column('Time', anchor='w', width=150)
tree.pack(side='left', fill='both', expand=True)

scrollbar = Scrollbar(left_frame, orient='vertical', command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.config(yscrollcommand=scrollbar.set)

lmain = Label(right_frame)
lmain.pack()

update_table_display()
show_frame()

root.mainloop()

cap.release()
cv2.destroyAllWindows()
close_db_connection()
