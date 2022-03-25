from deepface import DeepFace
import cv2
from preprocess import drawDictOverPicture

# capture camera
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
while True:
    ret, frame = cap.read()
    if ret:
        try:
            obj = DeepFace.analyze(img_path=frame, enforce_detection=True, actions=("race",))
            obj = obj["race"]
            drawDictOverPicture(frame, obj)
        except:
            pass
        # show image
        cv2.imshow('frame', frame)
        # press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
