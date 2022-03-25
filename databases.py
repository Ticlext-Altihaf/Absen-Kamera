from typing import Any, List
import faiss
import preprocess
import os
import json
import numpy as np
import atexit

# Files
dataFolder = "data"
indexFile = dataFolder + "/vector.index"
indexToIDFile = dataFolder + "/indexToID.json"

# Check
if not os.path.exists(dataFolder):
    os.makedirs(dataFolder)

# Databases
faissIndex = faiss.IndexFlatL2(preprocess.dimensions)
indexToID = {}

"""
indexToID[index] = identity: Any
"""


def load():
    #if not exists return
    if not os.path.exists(indexFile):
        return
    if not os.path.exists(indexToIDFile):
        return
    global indexToID, faissIndex
    # restore
    faissIndex = faiss.read_index(indexFile)
    with open(indexToIDFile, "r") as f:
        indexToID = json.load(f)
    # assert both length same
    assert len(indexToID) == faissIndex.ntotal


def save():
    global indexToID, faissIndex
    # assert both length same
    assert len(indexToID) == faissIndex.ntotal
    # save
    faiss.write_index(faissIndex, indexFile)
    with open(indexToIDFile, "w") as f:
        json.dump(indexToID, f)


if os.path.exists("vector.index"):
    try:
        print("Loading index...")
        load()
    except Exception as e:
        print("Error loading databases:", e)
        exit()


def add_user(img_path, identity):
    """
    img_path: image path could be URL, Base64, or path
    identity: any
    """
    global indexToID, faissIndex
    # assert both still in sync
    assert len(indexToID) == faissIndex.ntotal
    img = preprocess.toVector(img_path)
    # to 1, dimesion shape
    img = np.expand_dims(img, axis=0)
    faissIndex.add(img)
    le = faissIndex.ntotal - 1
    indexToID[le] = identity
    return le


def index(img_path, k=3):
    """
    img_path: image path could be URL, Base64, or path
    return list of identity with distance
    []{
        distance: float
        identity: Any
    }
    """
    return indexs([img_path], k)[0]


def indexs(img_paths: List = None, k=3):
    """
    img_paths: List of image paths could be URL, Base64, or path
    return list of identity with distance
    [batch][]{
        distance: float
        identity: Any
    }
    """
    global indexToID, faissIndex
    # assert both length are still valid
    assert len(indexToID) == faissIndex.ntotal
    imgs = []
    for img_path in img_paths:
        img = preprocess.toVector(img_path)
        imgs.append(img)
    imgs = np.array(imgs)
    distancesB, neighborsB = faissIndex.search(imgs, k)
    result = []
    for neighbors, distances in zip(neighborsB, distancesB):
        batch = []
        for neighbor, distance in zip(neighbors, distances):
            batch.append({
                "distance": distance,
                "index": indexToID[str(neighbor)]
            })
        result.append(batch)
    return result


def exit_handler():
    print("Saving databases...")
    save()
    print("Done!")


atexit.register(exit_handler)
