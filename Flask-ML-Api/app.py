from flask import Flask, url_for, send_from_directory, request, jsonify
from flask_cors import CORS
import logging, os
from werkzeug import secure_filename
import numpy as np
import keras
import keras_applications
import keras_preprocessing
from keras.models import load_model
from keras.models import model_from_json
import sys
import json
import cv2

print(cv2.__version__)
print(np.__version__)
print(keras.__version__)
print(keras_preprocessing.__version__)
print(keras_applications.__version__)

app = Flask(__name__)
CORS(app)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

port = int(os.environ.get('PORT', 33507))

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# filepath = os.getcwd() + "/model2.h5"
# model = load_model(filepath)

# filePath = os.getcwd() + "/modelWeights.h5"
# filePath2 = os.getcwd() + "/model.json"
# json_file = open("model.json","r")
# loaded_model_json = json_file.read()
# json_file.close()
# model = model_from_json(loaded_model_json)
# model.load_weights(filePath)


model = load_model("utkarsh.h5")

classes = {
    0: 'Apple-Apple Scab',
    1: 'Apple-Black Rot',
    2: 'Apple-Healthy',
    3: 'Corn-Common Rust',
    4: 'Corn-Healthy',
    5: 'Peach-Bacterial Spot',
    6: 'Peach-healthy',
    7: 'Potato-Early Blight',
    8: 'Potato-Late Blight',
    9: 'Potato-Healthy',
    10: 'Tomato-Bacterial Spot',
    11: 'Tomato-Tomato Mosaic Virus',
    12: 'Tomato-Healthy'
}


def predict(img):
    pred = model.predict(img)
    final = pred.argmax()
    return classes[final]

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/', methods = ['GET', 'POST'])
def api_root():
    app.logger.info(PROJECT_HOME)
    if request.method == 'GET':
        a = {"server": "running like makhan ;)"}
        return jsonify(a)
    if request.method == 'POST' and request.files['file']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['file']
        img_name = secure_filename(img.filename);
        print("image", img)
        print("image_name", img_name)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        mat = cv2.imread(saved_path)
        mat = cv2.resize(mat, (50, 50))
        mat = mat / 255.0
        mat = mat.reshape(1, 50, 50, 3)
        print(type(mat))
        pred = predict(mat)
        response_data = {"response": pred }
        # os.remove(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
        return jsonify(response_data);
    else:
    	return "Where is the image?"

if __name__ == '__main__':
    app.run(debug=False, port=33507)
