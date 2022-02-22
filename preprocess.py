from deepface.basemodels import Facenet as FaceModel
from deepface.commons import functions

model = FaceModel.loadModel()
dimensions = model.getDimensions()

def toVector(img_path, target_size = (160, 160)):
    """
    img_path: image paths could be URL, Base64, or path
    """
    img = functions.preprocess_face(img=img_path, target_size=(160, 160))
    embedding = model.predict(img)[0,:]#(1, 128) to (128, )
    return embedding
