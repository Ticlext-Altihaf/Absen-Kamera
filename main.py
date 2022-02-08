import numpy as np
import cv2
import os
import sys
from urllib.request import Request, urlopen
import shutil


def load(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    req = urlopen(req)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'
    return img

print(os.getcwd())

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
face_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_alt.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_eye.xml'))


def process(url):
    img = load(url)
    if(img is None):
        raise Exception("Could not load image")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    print("Found:", len(faces), "faces")
    #name from URL
    name = url.split('/')[-1]
    name = "faces_" + name
    
    #cleanup
    try:
        shutil.rmtree(name)
    except:
        pass
    #create directory
    os.mkdir(name)
    preview = img.copy()
    counter = 0
    for (x,y,w,h) in faces:
        #crop
        sub_img = img[y:y+h, x:x+w]
        cv2.imwrite(name + "/face_" + str(counter) + ".png", sub_img)
        #files id
        counter += 1
        #draw rectangle
        preview = cv2.rectangle(preview,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imwrite(name+".png", preview)


process("https://cdn.discordapp.com/attachments/939013407842127882/940591793098088448/3289223.png")


cv2.destroyAllWindows()
