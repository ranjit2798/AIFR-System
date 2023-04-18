from utils import Conf
from tinydb import TinyDB
from tinydb import where
import argparse
import shutil
import os
# construct the argument parser and parse the arguments
ids=input("Input the id to be deleted")
config_file="D:/Attendance Management System/config/config.json"
conf = Conf(config_file)
db = TinyDB(conf["db_path"])
studentTable = db.table("student")
student = studentTable.search(where(args["id"]))
student[0][args["id"]][1] = "unenrolled"
studentTable.write_back(student)

 # delete the student's data from the dataset
shutil.rmtree(os.path.join(conf["dataset_path"], conf["class"],ids))
print("[INFO] Please extract the embeddings and re-train the face recognition model...")
db.close()