from deepface import DeepFace
import cv2

backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
tempCameraImageFile = "test.jpg"
camera = cv2.VideoCapture(0)
while True:
    return_value, image = camera.read()
    cv2.imwrite(tempCameraImageFile, image)
    obj = DeepFace.analyze(img_path=tempCameraImageFile, enforce_detection=False, actions=("race",))
    for race in obj['race']:
        print(race+":", obj['race'][race])
    print("\n")
