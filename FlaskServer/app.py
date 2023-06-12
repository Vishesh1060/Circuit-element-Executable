# -*- coding: utf-8 -*-
import cv2,numpy
from flask import Flask, render_template, request
app = Flask(__name__)

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
        image = request.files['imageInput'].read()
        file_bytes = numpy.fromstring(image, numpy.uint8)
        img = cv2.imdecode(file_bytes,cv2.IMREAD_UNCHANGED)
        print('Debug Input:',image,type(image))
        cv2.imshow(image) 
        return render_template('index.html')
    else:
        return render_template('upload.html')
    
if __name__ == '__main__':
    app.run(debug=True)
