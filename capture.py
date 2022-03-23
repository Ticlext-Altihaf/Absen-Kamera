import cv2
import databases
import traceback
name = input("Enter your name: ")
camera = cv2.VideoCapture(0)
databases.load()
for i in range(10):
    while True:
        try:
            ret, frame = camera.read()
            cv2.imshow("Capturing", frame)
            index = databases.add_user(frame, name)
            print("Capturing: ", i + 1, ", Index: ", index)
            cv2.waitKey(250)
            break
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: ", e, tb)

databases.save()
cv2.destroyAllWindows()