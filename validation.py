from fastapi import FastAPI

app = FastAPI()





@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/validate")
async def validate(image_path: str):
    import numpy as np
    import urllib.request
    import os
    import pathlib
    from PIL import Image
    import requests
    from io import BytesIO
    import pandas as pd
    import pyrebase
    firebaseConfig = {
        'apiKey': "AIzaSyDrdZvpXaHRUujP-jWBrd02643CqzAZ1Y0",
        'authDomain': "ezbill-1.firebaseapp.com",
        'databaseURL': "https://ezbill-1-default-rtdb.firebaseio.com",
        'projectId': "ezbill-1",
        'storageBucket': "ezbill-1.appspot.com",
        'messagingSenderId': "1018480204152",
        'appId': "1:1018480204152:web:e33488e0e6f36bf9f2d08d",
        'measurementId': "G-JMQ6T5NT9E"
        }
    firebase = pyrebase.initialize_app(firebaseConfig)
    db= firebase.database()
    auth = firebase.auth()
    storage = firebase.storage()
    path = image_path
    # import urllib.request

    storage.child(path).download("","downloaded.jpeg")
    import torch

    # Model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

    # Images
    img = "downloaded.jpeg"  # or file, Path, PIL, OpenCV, numpy, list

    # Inference
    results = model(img)

    # Results
    switch = 0
    for index, row in results.pandas().xyxy[0].iterrows():
        detect_name = str(row['name'])
        if detect_name == "person":
            switch = 1
            return {"message:": "No Person Detected"}
    if switch == 0:
        return {"message:": "No Person Detected"}

