# USAGE
# python object_tracker.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
# python object_tracker.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from Logging.Logger import Logger
import Logging.Logger as Log
from LocalData.Settings import Settings
from pyimagesearch.centroidtracker import CentroidTracker
import Lib.Constants as const
from FaceTracker import FaceTracker
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

class ObjectTracker():

    def __init__(self) -> None:
        # initialize our centroid tracker and frame dimensions
        self.ct = CentroidTracker()
        self.faceTracker = FaceTracker()
        self.H = None
        self.W = None
        self.isRunning = False
        self.currentFrame = None
        self.hasCamera = False
        
        # load our serialized model from disk
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe('models/deploy.prototxt', 'models/res10_300x300_ssd_iter_140000.caffemodel')

    #starts the camera for tracking
    def startTracking(self):
        self.isRunning = True
        self.startCamera()

    #starts the camera
    def startCamera(self):
        print("Starting camera")
        if not self.hasCamera:
            # initialize the video stream and allow the camera sensor to warmup
            self.hasCamera = True
            self.vs = VideoStream(src=0).start()
            time.sleep(2.0)
        
    #resets the current state of the tracker
    def reset(self):
        self.ct.reset()
        self.faceTracker.reset()
        time.sleep(2.0)

    #returns False if invalid camera input is detected
    def checkSample(self):
        if not self.vs:
            raise Exception("You need to initialize the video stream first")
        
        #is face recognition enabled?
        faceRecognition = Settings.get(Settings.FACE_RECOGNITION)

        #grab the next frame
        frame = self.vs.read()
        frame = imutils.resize(frame, width=400)

        #save the current frame for other parts of blurr to use
        self.currentFrame = frame

        #set the shape of the frame if needed
        if self.W is None or self.H is None:
            (self.H, self.W) = frame.shape[:2]
        
        # construct a blob from the frame, pass it through the network,
        # obtain our output predictions, and initialize the list of
        # bounding box rectangles
        blob = cv2.dnn.blobFromImage(frame, 1.0, (self.W, self.H),
                                 (104.0, 177.0, 123.0))

        self.net.setInput(blob)
        detections = self.net.forward()
        rects = []
        # loop over the detections
        for i in range(0, detections.shape[2]):
            # filter out weak detections by ensuring the predicted
            # probability is greater than a minimum threshold
            if detections[0, 0, i, 2] > 0.5:
                # compute the (x, y)-coordinates of the bounding box for
                # the object, then update the bounding box rectangles list
                box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                rects.append(box.astype("int"))

        # update our centroid tracker using the computed set of bounding
        # box rectangles
        objects = self.ct.update(rects)

        #update the face tracker using the computed objects
        if faceRecognition:
            self.faceTracker.update(frame, rects, objects)

        #noone detected
        if len(objects) == 0:
                return (False, Log.LOG_LOCKING_NOONE)

        #if face recognition is enabled, check if everyone is authorized
        if faceRecognition:
            if not self.faceTracker.isEveryoneAuthorized():
                return (False, Log.LOG_LOCKING_UNAUTH)
        else:
            #otherwise allow only one user at a time
            if len(objects) > 1:
                return (False, Log.LOG_LOCKING_UNAUTH)

        #everything is fine here
        #wait before next iteration
        cv2.waitKey(1)
        return (True, None)

    #grabs a frame from the camera stream
    def grabLastFrame(self):
        #if tracking is enabled just use the last grabbed frames
        if self.isRunning:
            return self.currentFrame
        else:
            #otherwise grab a new one
            frame = self.vs.read()
            frame = imutils.resize(frame, width=400)
            return frame

    #stops the tracking -> turns of the camera stream
    def stopTracking(self):
        self.vs.stream.release()
        self.vs.stop()
        self.reset()
        self.hasCamera = False
        self.isRunning = False
        self.currentFrame = None
    
    #ends the camera stream if it is not used for tracking
    def stopCamera(self):
        if self.hasCamera and not self.isRunning:
            self.hasCamera = False
            self.vs.stream.release()
            self.vs.stop()
            self.currentFrame = None 

    #makes a red rectangle around each face in the frame
    def markFrame(self, frame):
        locations = self.faceTracker.getFaceLocations(frame)
        for (top, right, bottom, left) in locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
        return frame

    #gets encodings of all faces in the frame
    def getFaceEndodings(self, frame):
        return self.faceTracker.getFaceEncodings(frame)

