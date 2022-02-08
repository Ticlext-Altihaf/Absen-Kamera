import numpy as np
import cv2
import os
import sys
from urllib.request import Request, urlopen



def load(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    req = urlopen(req)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'
    return img

print(os.getcwd())

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
face_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_eye.xml'))




img = load("https://cdn.discordapp.com/attachments/939013407842127882/940591793098088448/3289223.png")
if(img is None):
    print("NO IMAGE")
    sys.exit()
    
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
