from utils import Conf
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle
config_file="D://IoT//AI-FR//Attendance Management System/config//config.json"
conf = Conf(config_file)
print("[INFO] loading face encodings...")
data = pickle.loads(open(conf["encodings_path"], "rb").read())

print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])
print("[INFO] training model...")
recognizer = SVC(C=1.0, kernel="linear", probability=True)
recognizer.fit(data["encodings"], labels)
print("[INFO] writing the model to disk...")
f = open(conf["recognizer_path"], "wb")
f.write(pickle.dumps(recognizer))
f.close()
 # write the label encoder to disk
f = open(conf["le_path"], "wb")
f.write(pickle.dumps(le))
f.close()