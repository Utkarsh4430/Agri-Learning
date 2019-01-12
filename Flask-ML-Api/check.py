import numpy as np
import cv2
from keras.models import load_model

model = load_model("utkarsh.h5")

classes = {
    0:'Apple-Apple Scab',
    1:'Apple-Black Rot',
    2:'Apple-Healthy',
    3:'Corn-Common Rust',
    4:'Corn-Healthy',
    5:'Peach-Bacterial Spot',
    6:'Peach-healthy',
    7:'Potato-Early Blight',
    8:'Potato-Late Blight',
    9:'Potato-Healthy',
    10:'Tomato-Bacterial Spot',
    11:'Tomato-Tomato Mosaic Virus',
    12:'Tomato-Healthy'
}
def predict(img):
    pred = model.predict(img)
    final = pred.argmax()
    return classes[final]
mat = cv2.imread(r"C:\Users\UTKARSH\Desktop\Paytm hackathon\segmented\Tomato___healthy\0a205a11-1e64-49f7-93c2-ad59312b4f83___RS_HL 0334_final_masked.jpg")
mat = cv2.resize(mat, (50, 50))
mat = mat / 255.0
mat = mat.reshape(1, 50, 50, 3)
pred = predict(mat)
print(pred)
import keras
# import Keras-Preprocessing
# import Keras-Applications
print (cv2.__version__)
print (keras.__version__)

