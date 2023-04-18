from utils import Conf
#from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
import sqlite3
import face_recognition
import argparse
import imutils
#import pyttsx3
import time
import cv2
import os
import tkinter as tk
import ttk
from ttk import Frame
from PIL import Image
from PIL import ImageTk
def eenroll():
    #ids = input("Input The no: ")
    #name = input("Input the name of the person: ")
    config_file = "E://IOT//AI-FR//Attendance Management System//config//config.json"
    conf = Conf(config_file)
    ewin = tk.Tk()
    ewin.geometry('800x800')
    ewin.resizable(width=False, height=False)
    ewin.resizable(True, True)
    ewin.title("Employee Enrollment ")
    ewin.configure(background='#4b8bbe')
    tk.Label(ewin, text="Employee Enrollment Form", font=("Arial Bold", 32)).place(x=100, y=0)
    '''fname1= tk.StringVar()
    id1 = tk.StringVar()
    lname1 = tk.StringVar()
    dept = tk.StringVar()'''
    tk.Label(ewin, text="Employee Id:   ").place(x=50, y=80)
    id1=tk.Entry(ewin)
    id1.place(x=150, y=80)
    tk.Label(ewin, text= "First Name: ").place(x=50, y=120)
    fname1=tk.Entry(ewin)
    fname1.place(x=150,y=120)
    tk.Label(ewin, text="Last Name: ").place(x=50, y=170)
    lname1=tk.Entry(ewin)
    lname1.place(x=150, y=170)
    tk.Label(ewin, text="Department : ").place(x=50, y=200)
    dept=tk.Entry(ewin)
    dept.place(x=150, y=200)
    print(id1)
    # initialize the database and student table objects

    def get_data():
        ids = (id1.get())
        name = (fname1.get())
        lname = (lname1.get())
        dept1= (dept.get())
        #print(ids)
        db = sqlite3.connect(conf["db_path"])
        cur = db.cursor()
        # qry = "Select * from entry where id= {} ;".format(id)
        # retrieve student details from the database
        employee = cur.execute("Select * from entry where id= '{}' ;".format(ids)).fetchall()
        # print(employee)
        if len(employee) == 0:

            # initialize the video stream and allow the camera sensor to warmup
            print("[INFO] warming up camera...")
            vs = WebcamVideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start()
            time.sleep(2.0)

        # initialize the number of face detections and the total number of images saved to disk
            faceCount = 0
            total = 0
            status = "detecting"

# create the directory to store the student's data
            os.makedirs(os.path.join(conf["dataset_path"], ids), exist_ok=True)
 # loop over the frames from the video stream
            while True:
                frame = vs.read()
                frame = imutils.resize(frame, width=400)
                frame = cv2.flip(frame, 1)
                orig = frame.copy()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb,
                                                        model=conf["detection_method"])

 # loop over the face detections
                for (top, right, bottom, left) in boxes:
                    cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
                    if faceCount < conf["n_face_detection"]:
                        faceCount += 1
                        status = "detecting"
                        p = os.path.join(conf["dataset_path"],
                        ids, "{}.png".format(str(total).zfill(5)))
                        cv2.imwrite(p, orig[top:bottom, left:right])
                        total += 1
                        status = "saving"
                        cv2.putText(frame, "Status: {}".format(status), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                        cv2.imshow("Frame", frame)
                        cv2.waitKey(1)

                if total == conf["face_count"]:
            # let the student know that face enrolling is over
            #ttsEngine.say("Thank you {} you are now enrolled in the {} " \
            #"class.".format(name, conf["class"]))
            #ttsEngine.runAndWait()
                    print("Thank you you have been enrolled")
                    l = [(ids,name,"enrolled")]
                    q2="Insert into entry (id,name,status) values(?,?,?);"
                    cur.executemany(q2, l)
                    s=cur.execute("Select  * from entry;").fetchall()
                    print(s)
                    db.commit()
            
                    print("[INFO] {} face images stored".format(total))
                    print("[INFO] cleaning up...")
                    break

# otherwise, a entry for the student id exists
            else:

 # get the name of the student
                name = "Select fname from attendance;"
                print("[INFO] {} has already already been enrolled...".format(name))
                cv2.destroyAllWindows()
                #submit=tk.Button(ewin,text="Enroll Employee", command = get_data())

        vs.stop()
        cur.close()
        db.close()

    img1 = tk.PhotoImage(file=r"E://IoT//AI-FR//Attendance Management System//img//eroll.png")
    img2 = tk.PhotoImage(file=r"E://IoT//AI-FR//Attendance Management System//img//exit.png")
    submit = tk.Button(ewin,text="Enroll Employee",command=get_data)
    submit.place(x=100, y=300)
    def reset_entry():
        id1.delete(0,tk.END)
        fname1.delete(0,tk.END)
        lname1.delete(0,tk.END)
        dept.delete(0,tk.END)

    reset = tk.Button(ewin,text="Reset",command= reset_entry)
    reset.place(x=700, y=300)
    close = tk.Button(ewin,text="Exit",command = ewin.destroy)
    close.place(x=400, y=400)
    ewin.mainloop()
