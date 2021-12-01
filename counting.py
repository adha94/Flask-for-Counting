from flask import Flask, jsonify, request
import json
from json import JSONEncoder
import numpy as np
import urllib
import cv2
import imutils
import werkzeug

response = ''

app = Flask(__name__)
@app.route('/upload', methods = ['POST'])
def upload():
    global response
    if (request.method == "POST"):
        imageFile = request.files['image']
        filename = werkzeug.utils.secure_filename(imageFile.filename)
        imageFile.save("./uploaded/" + filename)
        
        image = cv2.imread("./uploaded/" + filename)
        cv2.imshow("Image", image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale", gray)

        edged = cv2.Canny(gray, 30, 150)
        cv2.imshow("Canny", edged)

        thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
        cv2.imshow("Threshold", thresh)
        cv2.waitKey(10000)

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        answer = len(cnts)

        return jsonify({
            "message" : f'{answer}'
        })

if __name__ == "__main__":
    app.run(debug=True, port=4000)



