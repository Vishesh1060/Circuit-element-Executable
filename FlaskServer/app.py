# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 13:31:03 2023

@author: vishesh
"""
import cv2,numpy
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/createAccount')
def createAccount():
    return render_template('createAccount.html') 


#@app.route('/upload', methods=['POST'])

def upload():
    if request.method == 'POST':
        image = request.files['imageInput'].read()
        '''
        file_bytes = numpy.fromstring(image, numpy.uint8)
        img = cv2.imdecode(file_bytes,cv2.IMREAD_UNCHANGED)
        print('Debug Input:',image,type(image))
        cv2.imshow(image) 
        '''
        return render_template('showCode.html')
    
if __name__ == '__main__':
    app.run(debug=True)

