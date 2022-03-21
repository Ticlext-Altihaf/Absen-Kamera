from deepface import DeepFace
import cv2
import os
from preprocess import drawDictOverPicture

# iterate all files in the directory
imgFiles = []
for filename in os.listdir('.'):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        imgFiles.append(filename)


def showRace(filename):
    img = cv2.imread(filename)
    try:
        obj = DeepFace.analyze(img_path=img, enforce_detection=True, actions=("race",))
    except:
        return
    cv2.imshow(filename, img)
    obj = obj['race']
    drawDictOverPicture(img, obj)
    # show image
    cv2.imshow(filename, img)


for imgFile in imgFiles:
    showRace(imgFile)

cv2.waitKey(0)
