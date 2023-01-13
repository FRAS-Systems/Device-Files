##! /usr/bin/python

# import packages
# Facial req pakages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import cv2
import time
import csv
import firebase_admin
from firebase_admin import credentials, storage


# vars
current_face = []
attendanceinfo = {}

# facial req setup
currentname = "unknown"
encodingsP = "encodings.pickle"  # faces
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# video
vs = VideoStream(usePiCamera=True, ).start()
time.sleep(2.0)
fps = FPS().start()

# Set up the Firebase Storage client
cred = credentials.Certificate("fras-systems-web-firebase-adminsdk-358l4-d9ea74c356.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'fras-systems-web.appspot.com'
})
bucket = storage.bucket()

# class list

# download file
filename = 'AttendanceData/ClassList.txt'
blob = bucket.blob(filename)
csv_string = blob.download_as_string().decode('utf-8')
print(csv_string)
for name in csv_string.split('/'):
    attendanceinfo.update({name: 'N/A'})

filename = 'AttendanceData/AttendanceData.txt'
blob = bucket.blob(filename)
# loop
currenttime = time.time()
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    # Detect faces
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    # loop over faces
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"  # if face is not recognized, then print Unknown

        # check matches
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}  # face count

            # count each face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

            # face identified
            if currentname != name:
                currentname = name
                print("Face detected:" + currentname + " at " + str(time.time()))
                attendanceinfo.update({currentname: time.time()})

                if time.time() > currenttime + 8:
                    currenttime = time.time()
                    blob.upload_from_string(str(attendanceinfo))


        names.append(name)  # list of names

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        .8, (0, 255, 255), 2)

        # display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

        # quit when 'q' key is pressed
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
