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

print(print('retrieved classlist: ' + str(classlist)))
if not os.path.isdir('/home/fras/Desktop/device-files/Facial_Recognition/dataset/'):
    os.mkdir('/home/fras/Desktop/device-files/Facial_Recognition/dataset/')

print('downloading pictures')
for name in classlist:
    filename1 = 'AttendanceData/photo-dataset/' + name
    newdir = '/home/fras/Desktop/device-files/Facial_Recognition/dataset/' + name
    print('downloading pictures for ' + name + " at: " + filename1)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
    x = 1
    while x <= 10:
        print('downloading pictures: ' + str(x) + '/10')
        filename = filename1 + '/Photo-' + str(x) + '.jpeg'

        blob = bucket.blob(filename)
        blob.download_to_filename("dataset/" + name + '/' + 'Photo-' + str(x) + ".jpg")
        x += 1

os.system("python /home/fras/Desktop/device-files/Facial_Recognition/train_model.py")
