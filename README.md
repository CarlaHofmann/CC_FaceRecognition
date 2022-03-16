# CC_FaceRecognition

The target application to deploy on OpenShift and the IBM Cloud is a web application for face recognition. It can be
used due a web interface or an API.

The REST API, that is also used from the web interface, provides two routes:

GET `/` <br />
Returns the index.html for the web interface.

POST `/response` <br />
The request body must provide an image. The response contains the given image with a marking for all the detected faces
in it.