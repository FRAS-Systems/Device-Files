import os
import firebase_admin
from firebase_admin import credentials, storage

# Set up the Firebase Storage client
cred = credentials.Certificate("fras-systems-web-firebase-adminsdk-358l4-d9ea74c356.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'fras-systems-web.appspot.com'
})
bucket = storage.bucket()

# setup vars
classlist = []
filename = 'AttendanceData/ClassList.txt'

# download file
blob = bucket.blob(filename)
csv_string = blob.download_as_string().decode('utf-8')
print(csv_string)
for name in csv_string.split(','):
    classlist.append(name)

print(classlist)
os.mkdir('/home/fras/Desktop/device-files/Facial_Recognition/dataset')

for name in classlist:
    filename = 'AttendanceData/photo-dataset/' + name
    newdir = '/home/fras/Desktop/device-files/Facial_Recognition/dataset/' + name
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    blob = bucket.blob(filename)
    blob.download_to_filename("attendancedata.txt")

os.system("python /home/fras/Desktop/device-files/Facial_Recognition/train_model.py")
