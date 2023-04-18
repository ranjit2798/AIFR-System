import pandas as pd
import sqlite3
import time
#import openpyxl
#conf = Conf("D://IoT//AI-FR//Attendance Management System//Attendance Management System//config//config.json")
db = sqlite3.connect("D://IOT//AI-FR//Attendance Management System//Attendance Management System//database//employee.db")
cur=db.cursor()
def convert_to_excel():
    query="Select * from emp;"
    results=cur.execute(query).fetchall()
    print(results)
    df = pd.DataFrame(data=results)
    df.reset_index(drop=True, inplace=True)
    

    print (df)
    timestr=time.strftime("%Y-%m-%d")
    filename= timestr+".csv"
    df.to_csv(filename)
convert_to_excel()
