import tensorflow.keras
from tensorflow.keras.models import load_model
import cv2 
import numpy as np
import time
import face_recognition

#display scientific notation for clarity
np.set_printoptions(suppress=True)

#load model
new_model = tensorflow.keras.models.load_model("face_recog/models/face_recognition_model.h5")

#load the test_labels
with open("face_recog/labels.txt", "r") as f:
    class_names = f.read().split("\n")
    
    color = np.random.uniform(0, 255, size=(len(class_names), 3))
    
min_confidence_score = 0.5
#run the camera
cap = cv2.VideoCapture(0)
while cap.isOpened():
    #Read in the image
    success, img = cap.read()
    
    height, width, channels = img.shape
    
    #create blob
    blob = cv2.dnn.blobFromImage(img, size=(224, 224), mean=(104, 117, 123), swapRB = True)
    
    #set input to model
    new_model.setInput(blob)
    
    #start the time
    start = time.time()
    
    #cal FPS for current frame detection
    totalTime = end - start
    
    fps = 1/totalTime

    #Make foward pass in model
    output = new_model.forward()
    
    # run over each of the detections
    for detection in output[0,0,:,:]:
        confidence = detection[2]
        if confidence  > min_confidence_score:
            
            class_id = detection[1]
            
            class_name = class_name[int(class_id)-1]
            
            color = color(int(class_id))
            
            bboxX = detection[3] * width
            bboxY = detection[4] * height
            
            bboxWidth = detection[5] * width
            bboxHeight = detection[6] * height
            
            cv2.rectangle(img, (int(bboxX), int(bboxY)), (int(bboxWidth), int(bboxHeight)), color, thickness=2)
            cv2.rectangle(img, class_name, (int(bboxX), int(bboxY-5)),cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
    #show FPS
    cv2.putText(img, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255,0), 2)
    
    cv2.imshow("image", img)
    
    
    #cv2.imshow("classification Resized", img_resize)
    cv2.imshow("classification Original", img)
    
    if cv2.waitKey(5) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
cap.release()
    
    
            
            
            
                        
            
    
    
    

