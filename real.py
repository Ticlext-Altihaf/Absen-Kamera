from deepface import DeepFace
import databases

DeepFace.stream(db_path=databases.dataFolder)