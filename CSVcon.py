from utils import Conf
#from imutils.video import VideoStream
#from datetime import datetime
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
from enroll import eenroll
import time as t
from datetime import datetime,timedelta
import tkinter.messagebox
db = sqlite3.connect("D://IoT//AI-FR//Attendance Management System//database//attendance.db")
cur = db.cursor()
conf = Conf("D://IoT//AI-FR//Attendance Management System//config//config.json")
query = "Select * from login;"
col=pd.read_sql_query(query,db)
#results = cur.execute(query).fetchall()
#names = list(map(lambda x: x[0], cur.description))
#print(names)
#print(results)
df = pd.DataFrame(data=col)
df.reset_index(drop=True, inplace=True)
print(df.head())

#print(col)
timestr = t.strftime("%Y-%m-%d")
fpath = r"D://IoT//AI-FR//Attendance Management System//main//Report//"
filename = fpath + timestr + ".csv"
df.to_csv(filename,index=False)
db.close()