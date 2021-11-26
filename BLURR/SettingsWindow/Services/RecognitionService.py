from Tracking.ObjectTracker import ObjectTracker
import face_recognition as fr
import cv2
import base64


class RecognitionService():

    def __init__(self, objectTracker: ObjectTracker) -> None:
        self.objectTracker = objectTracker

    # grab a frame from the object tracker and encode it as a base64 string
    def getFrame(self):
        frame = self.grabFrame()
        ret = self.objectTracker.markFrame(frame)
        val, buf = cv2.imencode(".png", ret)
        retEncoded = base64.b64encode(buf)
        return str(retEncoded)

    # get a current from the object tracker
    def grabFrame(self):
        # if tracking is currently disabled -> start the camera first
        if not self.objectTracker.isRunning:
            self.objectTracker.startCamera()

        frame = self.objectTracker.grabLastFrame()
        return frame

    # get encodings for the faces in the current frame
    def getEncodings(self):
        return self.objectTracker.getFaceEndodings(self.grabFrame())
