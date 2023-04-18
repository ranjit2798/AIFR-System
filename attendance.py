from utils import Conf
#from imutils.video import VideoStream
from datetime import datetime
from datetime import date
import face_recognition
import numpy as np
import argparse
import imutils
from imutils.video import FPS
import pyttsx3
import sqlite3
import pickle
import time
import cv2
import pandas as pd
from imutils.video import WebcamVideoStream
import tkinter as tk
from enroll import enroll
import datetime
from datetime import datetime
window=tk.Tk()
window.geometry('800x800')
window.resizable(width=False, height=False)
window.resizable(True, True)
window.title("My Attendance Portal")
window.configure(background='#4b8bbe')
conf = Conf("D://IoT//AI-FR//Attendance Management System//Attendance Management System//config//config.json")
lbl=tk.Label(window, text= "AI- Based Attendance System", font = ("Arial Bold", 32)).place(x=100,y=0)
def get_data():
    enroll()
erimg= tk.PhotoImage(file= r"D://IoT//AI-FR//Attendance Management System//Attendance Management System//img//eroll.png")
dataset=tk.Button(window,text="Dataset",highlightcolor="red",image = erimg,command= get_data)
dataset.place(x=50, y=100)

def convert_to_excel():
        query = "Select * from login;"
        results = cur.execute(query).fetchall()
        print(results[2])

        df = pd.DataFrame(data=results)
        df.reset_index(drop=True, inplace=True)


        timestr = time.strftime("%Y-%m-%d")
        filename = timestr + ".csv"
        df.to_csv(filename)
rimg= tk.PhotoImage(file= r"D://IoT//AI-FR//Attendance Management System//Attendance Management System//img//report.png")
report=tk.Button(window,text="Report", highlightcolor="red",image = rimg ,command= convert_to_excel)
report.place(x=50,y=400)
def attendance():
    db = sqlite3.connect(conf["db_path"])
    cur = db.cursor()

    

    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open(conf["recognizer_path"], "rb").read())
    le = pickle.loads(open(conf["le_path"], "rb").read())
    print("[INFO] warming up camera...")
    vs = WebcamVideoStream(src=0).start()  # VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    fps = FPS().start()
    # initialize previous and current person to None
    prevPerson = None
    curPerson = None

    # initialize consecutive recognition count to 0
    consecCount = 0

    # initialize the text-to-speech engine, set the speech language, and
    # the speech rate
    print("[INFO] taking attendance...")
    ttsEngine = pyttsx3.init()
    ttsEngine.setProperty("voice", conf["language"])
    ttsEngine.setProperty("rate", conf["rate"])

    # initialize a dictionary to store the student ID and the time at
    # which their attendance was taken
    studentDict = {}
    logins = 0
    currentTime = datetime.now()
    nextday = (currentTime + datetime.timedelta(minutes=1)).strftime("%H:%M")
    tommo = (currentTime + datetime.timedelta(days=1)).strftime("%D")
    from datetime import datetime
    while True:
        # store the current time and calculate the time difference
        # between the current time and the time for the class

        # grab the next frame from the stream, resize it and flip it
        # horizontally
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=conf["detection_method"])
        
        today = datetime.datetime.now().strftime("%H:%M")
        today1 = datetime.datetime.now().strftime("%D")

        
        currentTime = datetime.now()

        for (top, right, bottom, left) in boxes:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # timeRemaining = conf["max_time_limit"] - timeDiff

        cv2.putText(frame, "Class: {}".format(conf["class"]), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        # cv2.putText(frame, "Class timing: {}".format(conf["timing"]),(10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(frame, "Current time: {}".format(currentTime.strftime("%H:%M:%S")), (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        # cv2.putText(frame, "Time remaining: {}s".format(timeRemaining),(10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        if len(boxes) > 0:
            logins = 0
            encodings = face_recognition.face_encodings(rgb, boxes)
            preds = recognizer.predict_proba(encodings)[0]
            j = np.argmax(preds)
            curPerson = le.classes_[j]
            if prevPerson == curPerson:
                consecCount += 1
            else:
                consecCount = 0
            prevPerson = curPerson
            if consecCount >= conf["consec_count"]:
                from datetime import datetime
                FMT = '%H:%M'

                query = "Select name from entry where id=" + curPerson + ";"
                s = cur.execute(query).fetchall()
                for i in s:
                    for j in i:
                        name = j
                q3 = "Select time from  emp where id=" + curPerson + ";"
                sws = cur.execute(q3).fetchall()
                q2 = "Select logger from  emp where id=" + curPerson + ";"
                sas = cur.execute(q2).fetchall()
                print(sas)
                for i in sas:
                    for j in i:
                        logins = j
                if logins is None:
                    logins = 0
                else:
                    logins = int(logins)
                if (len(sas) == 0 and len(sws) == 0):
                    logins += 1
                    ttsEngine.say("{} your attendance has been taken.".format(name))
                    ttsEngine.runAndWait()
                    s = (curPerson, today1, today, logins)
                    label2 = name + " your attendance has been taken."
                    cv2.putText(frame, label2, (5, 175),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    query = "Insert into emp (id,date,time,logger) values(?,?,?,?)"
                    cur.execute(query, s)
                    db.commit()
                    from datetime import datetime
                    studentDict[curPerson] = [datetime.now().strftime("%H:%M:%S"), logins]
                    print(studentDict)
                    import datetime
                    nextday = (currentTime + datetime.timedelta(minutes=1)).strftime("%H:%M")

                    # print(timeDiff)
                else:
                    for i in sws:
                        for j in i:
                            times = j
                            print(times)
                    import datetime
                    times = datetime.datetime.strptime(times, "%H:%M")
                    timeDiff = (currentTime - times).seconds
                    print(timeDiff)
                    if (timeDiff > 7200):
                        logins += 1
                        s = (curPerson, today1, today, logins)
                        ttsEngine.say("{} your attendance has been taken.".format(name))
                        ttsEngine.runAndWait()
                        label1 = name + " your attendance has been taken."
                        cv2.putText(frame, label1, (5, 175),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                        query = "Insert into emp (id,date,time,logger) values(?,?,?,?)"
                        cur.execute(query, s)
                        db.commit()
                        from datetime import datetime
                        studentDict[curPerson] = [datetime.now().strftime("%H:%M:%S"), logins]
                        print(studentDict)
                        import datetime
                        nextday = (currentTime + datetime.timedelta(minutes=1)).strftime("%H:%M")
                        print(timeDiff)

                if (today1 == tommo):
                    logins=0
                    convert_to_excel()
                    query5 = "delete from emp;"

                    # name = studentTable.search(where(curPerson))[0][curPerson][0]

            else:
                label = "Please stand in front of the camera"
                cv2.putText(frame, label, (5, 175),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow("Attendance System", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    print("[INFO] cleaning up...")
    fps.stop()
    vs.stop()

    db.close()
aimag= tk.PhotoImage(file= r"D://IoT//AI-FR//Attendance Management System//Attendance Management System//img//atimg.png")
eimg= tk.PhotoImage(file= r"D://IoT//AI-FR//Attendance Management System//Attendance Management System//img//exit.png")
att=tk.Button(window,text = "Attendance",highlightcolor = "red",image = aimag,command = attendance)
att.place(x=400, y=100)
ext=tk.Button(window,text="Exit",highlightcolor="red",image = eimg,command= window.destroy)
ext.place(x=400, y=400)
window.mainloop()
