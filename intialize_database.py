
from tinydb import TinyDB
import argparse

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-c", "--conf", required=True,help="Path to the input configuration file")
#args = vars(ap.parse_args())

 # load the configuration file
#conf = Conf()

 # initialize the database
db = TinyDB("/home/pi/Desktop/Attendance Management System/database/database.json")

 # insert the details regarding the class
print("[INFO] initializing the database...")
db.insert({"class": "Section_A"})
print("[INFO] database initialized...")

 # close the database
db.close()