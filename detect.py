import cv2
import databases
import traceback
from preprocess import drawDictOverPicture
# capture camera
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
databases.load()

while True:
    ret, frame = cap.read()
    if ret:
        try:
            obj = databases.index(frame)
            outcome = {}
            for o in obj:
                name = o['index']
                dist = o['distance']
                if name not in outcome:
                    outcome[name] = 99999999999
                if dist < outcome[name]:
                    outcome[name] = dist
            # 0 = 100%
            for out in outcome:
                outcome[out] = 100 - outcome[out]
            drawDictOverPicture(frame, outcome)
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: ", e, tb)
        # show image
        cv2.imshow('frame', frame)
        # press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


