import cv2
import os

#classifier
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
print(cv2_base_dir)
face_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_eye.xml'))

#get camera
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        #draw rectangle
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    if(len(faces) == 0):
        img = cv2.putText(img, "No faces found", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Display the resulting frame
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()