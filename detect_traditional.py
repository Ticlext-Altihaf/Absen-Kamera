from deepface import DeepFace
import cv2
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        try:
            df = DeepFace.find(img_path=frame, db_path="data/images/")
            ress = DeepFace.find(img_path=frame, db_path="data/images/", model_name="Facenet512", enforce_detection=False).to_dict('dict')
            res = ress['identity']
            val = ress['Facenet512_cosine']
            val = str((1-val[0])*100) + "%"
            res = res[0].split('/')[-2]
            cv2.putText(frame, res+": "+val, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        except:
            pass
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break