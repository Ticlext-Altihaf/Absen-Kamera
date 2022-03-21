import cv2
from deepface.basemodels import Facenet as FaceModel
from deepface.commons import functions

model = FaceModel.loadModel()
dimensions: int = model.output_shape[1]
font = cv2.FONT_HERSHEY_SIMPLEX


def toVector(img_path, target_size=(160, 160)):
    """
    img_path: image paths could be URL, Base64, or path
    """
    img = functions.preprocess_face(img=img_path, target_size=(160, 160))
    embedding = model.predict(img)[0, :]  # (1, 128) to (128, )
    return embedding


def drawDictOverPicture(img, valueDict):
    # sort dict by value
    obj = {k: v for k, v in sorted(valueDict.items(), key=lambda item: item[1])}
    # write text to image
    frameWidth = img.shape[0]
    frameHeight = img.shape[1]
    height: float = frameHeight * 0.05
    for race in obj:
        text = race + ": " + str("{:.3f}".format(obj[race])) + " %"
        cv2.putText(img, text, (int(frameWidth*0.02), int(height)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        height = height + frameHeight * 0.05
