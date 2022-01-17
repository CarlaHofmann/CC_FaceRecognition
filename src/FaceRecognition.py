#!/usr/bin/python

import sys
import cv2


def face_detect(imgpath, imgname, cascasdepath = "haarcascade_frontalface_default.xml"):

    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    new_imgpath = f"images/FR_{imgname}"

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

    with open(new_imgpath, "wb+") as file_object:
        file_object.write(image)

    return new_imgpath
