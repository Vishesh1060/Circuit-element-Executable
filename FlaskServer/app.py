# -*- coding: utf-8 -*-
import cv2,numpy
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "C:/Users/vishe.IDEAPADFLEX/Desktop/MiniProject_final/Circuit-element-Executable/MLv2/imgs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
script_name = "../MLv2/test_frcnn.py"
input_data = b"-p imgs"

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/createAccount')
def createAccount():
    return render_template('createAccount.html') 

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/showCode')
def showCode():
    return render_template('showCode.html') 


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files["image-file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        subprocess.run(["python", script_name], input=input_data)
        #print("Received Data=",Data), capture_output=True, text=True
        print("POSTmode")
        return render_template('showCode.html')
    else:
        print('GETmode')
        return render_template('upload.html')
    
if __name__ == '__main__':
    app.run(debug=True)
