import os
from flask import Flask, request, redirect, url_for, send_from_directory
from flask import render_template
import sys
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = 'images'


@app.route('/')
def upload_image():
    return render_template('index.html')


@app.route('/response', methods=['POST'])
def recognize_image():
    f = request.files['img']
    filename = secure_filename(f.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(filepath)
    new_imgname = face_detect(filepath, filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], new_imgname)


def face_detect(imgpath, imgname, cascasdepath = "templates/haarcascade_frontalface_default.xml"):
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    new_imgname = f"FR_{imgname}"

    face_cascade = cv2.CascadeClassifier(cascasdepath)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize = (30,30)
        )

    print("The number of faces found = ", len(faces))

    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

    os.chdir(app.config["UPLOAD_FOLDER"])
    cv2.imwrite(new_imgname, image)
    os.chdir(os.path.dirname(os.getcwd()))

    return new_imgname


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')


