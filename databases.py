from typing import Any, List
import faiss
import preprocess
import os
import json
import numpy as np
import atexit


#Files
dataFolder = "data"
indexFile = dataFolder+"/vector.index"
indexToIDFile = dataFolder+"/indexToID.json"

#Check
if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)

#Databases
index = faiss.IndexFlatL2(preprocess.dimensions)
indexToID = {}


def load():
    #restore
    index = faiss.read_index("vector.index")
    with open(indexToIDFile, "r") as f:
        indexToID = json.load(f)

def save():
    #save
    faiss.write_index(index, indexFile)
    with open(indexToIDFile, "w") as f:
        json.dump(indexToID, f)

if os.path.exists("vector.index"):
    try:
        print("Loading index...")
        load()
    except Exception as e:
        print("Error loading databases:", e)
        exit()



def add(img_path, identity: int):
    """
    img_path: image path could be URL, Base64, or path
    identity: int
    """
    img = preprocess.toVector(img_path)
    index.add(img)
    indexToID[index.ntotal] = identity
    save()

def index(img_path, k=5):
    """
    img_path: image path could be URL, Base64, or path
    return list of identity with distance
    []{
        distance: float
        index: int
    }
    """
    return indexs([img_path], k)[0]

def indexs(img_paths: List = None, k= 3):
    """
    img_paths: List of image paths could be URL, Base64, or path
    return list of identity with distance
    [batch][]{
        distance: float
        index: int
    }
    """
    imgs = []
    for img_path in img_path:
        img = preprocess.toVector(img_path)
        imgs.append(img)
    imgs = np.numpy(imgs)
    distancesB, neighborsB = index.search(imgs, k)
    result = []
    for neighbors, distances in zip(neighborsB, distancesB):
        batch = []
        for neighbor, distance in zip(neighbors, distances):
            batch.append({
                "distance": distance,
                "index": indexToID[neighbor]
            })
        result.append(batch)
    return result
    
    

        
def exit_handler():
    print("Saving databases...")
    save()
    print("Done!")

atexit.register(exit_handler)