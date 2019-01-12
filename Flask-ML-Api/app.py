from flask import Flask, url_for, send_from_directory, request, jsonify
from flask_cors import CORS
import logging, os
from werkzeug import secure_filename
import numpy as np
from keras.models import load_model
import sys
import json
import cv2

app = Flask(__name__)
CORS(app)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

port = int(os.environ.get('PORT', 33507))

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

filePath = os.getcwd() + "/model.h5"
model = load_model(filePath)

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
        a = {"hellooooo": "from the python sideeeeee"}
        mat = cv2.imread(saved_path)
        mat = cv2.resize(mat, (50, 50))
        mat = mat / 255.0
        mat = mat.reshape(1, 50, 50, 3)
        predict = model.predict(mat)
        response_data = {"response": predict.tolist()}
        os.remove(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
        return jsonify(response_data);
    else:
    	return "Where is the image?"

if __name__ == '__main__':
    app.run(debug=True, port=33507)