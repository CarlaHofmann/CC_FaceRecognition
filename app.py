import os

import cv2
from flask import Flask, request, send_from_directory
from flask import render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'images'

cascade_path = "templates/haarcascade_frontalface_default.xml"


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

'''
Method to detect the containing faces for the given image. For this OpenCV and a cascade classifier for faces is used.
Return the name of the new image with the marked faces.
'''
def face_detect(imgpath, imgname):
    image = cv2.imread(imgpath)
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    new_imgname = f"FR_{imgname}"

    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(
        image_grayscale,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + h, y + h), (0, 255, 0), 2)

    os.chdir(app.config["UPLOAD_FOLDER"])
    cv2.imwrite(new_imgname, image)
    os.chdir(os.path.dirname(os.getcwd()))

    return new_imgname


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
