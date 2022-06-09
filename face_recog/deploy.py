import tensorflow.keras
from tensorflow.keras.models import load_model
import cv2 
import numpy as np
import time
import face_recognition
import imutils


#face recog deploy
#display scientific notation for clarity
np.set_printoptions(suppress=True)

#load prediction model
new_model = tensorflow.keras.models.load_model("./face_recog/models/face_recognition_model.h5")
#with open("face_recog/models/face_spoofing.pkl", "rb") as f:
#clf = joblib.load('face_recog/models/face_spoofing.pkl')



#load the test_labels
with open("./face_recog/models/labels.txt", "r") as f:
    class_names = f.read().split("\n")
    
#load the face detection model
net = cv2.dnn.readNetFromCaffe('./face_recog/models/deploy.prototxt', './face_recog/models/res10_300x300_ssd_iter_140000.caffemodel')

    
#create the array of the shape of the feed into the keras models
data = np.ndarray(shape=(1,224,224,3), dtype=np.float32)

size = (224, 224)

#open the camera 
cap = cv2.VideoCapture(0)

while cap.isOpened():
    
    start = time.time()
    
    ret, img = cap.read()
    
    img = imutils.resize(img, width=400)
    
    W = None
    H = None
    if W is None or H is None:
            (H, W) = img.shape[:2]
            
            
    # construct a blob from the frame, pass it through the network,
    # obtain our output predictions, and initialize the list of
    # bounding box rectangles
    blob = cv2.dnn.blobFromImage(img, 1.0, (W, H),
                                     (104.0, 177.0, 123.0))
    
    net.setInput(blob)
    detections = net.forward()
    rects = []
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # filter out weak detections by ensuring the predicted
        # probability is greater than a minimum threshold
        if detections[0, 0, i, 2] > 0.5:
        # compute the (x, y)-coordinates of the bounding box for
        # the object, then update the bounding box rectangles list
            box = detections[0, 0, i, 3:7] * \
                np.array([W, H, W, H]) 
            rects.append(box.astype("int"))
            
    print(rects)
            
    #no faces -> skip the rest of the steps
    if len(rects) == 0:
        continue
    
   
    for face in rects:
        
        x_up = face[0]
        y_up = face[1]
        x_down = face[2]
        y_down = face[3]
        
        face_width = x_up - x_down
        face_height = y_up - y_down
        
        new_face_width = 3 * face_width
        new_face_height = 2.5 * face_height
        
        x_offset = 1/2 * (new_face_width - face_width)
        y_offset = 1/2 * (new_face_height - face_height)
        
        new_x_up = x_up + x_offset
        new_y_up = y_up + y_offset
        
        new_x_down = x_down - x_offset
        new_y_down = y_down - y_offset
        
        if new_x_up < 0:
            new_x_up = 0
        
        if new_y_up < 0:
            new_y_up = 0
            
        if new_x_down > W - 1:
            new_x_down = W - 1
            
        if new_y_down > H - 1:
            new_y_down = H - 1
            
        face[0] = new_x_up
        face[1] = new_y_up
        face[2] = new_x_down
        face[3] = new_y_down
        
        for i in range(len(face)):
            if face[i] < 0:
                face[i] = 0
            elif face[i] > 0:
                pass
        crop_img = img[face[1]:face[3], face[0]:face[2]]
        
        height, width, channels = crop_img.shape
        
        scale_value = width/height
    
    #normalize the image
        img_resize = cv2.resize(crop_img, size, fx= scale_value, fy=1, interpolation=cv2.INTER_NEAREST)
    
        cv2.imshow("Resized", img_resize)
        cv2.waitKey(1)
    
    #turn image into np array
        img_array = np.asarray(img_resize)
    
    # normalize the image
        normalize_img_array = (img_array.astype(np.float32)/127.0) - 1
   
    
    #load the image into the array
    
        data[0] = normalize_img_array
    #set the shape of the data
   
    
    #run the inference
        prediction = new_model.predict(data)
        
   
        
        
    
    
    #print(prediction)
        index = np.argmax(prediction)
        class_name = class_names[index]
        
        confidence_score = prediction[0][index]
        
        # if confidence_score > 5.0 :
        #     index == 0 and index == 1
            
        # elif confidence_score > 7.0 :
        #     index == 2
            
        
       
            
            
        
    #Draw a box round predictions 
        if index == 0:
            cv2.rectangle(img, (face[0],face[1]),(face[2], face[3]),(0, 255, 0), 2)
        elif index==1:
            cv2.rectangle(img, (face[0],face[1]),(face[2], face[3]),(255, 172, 0), 2)
        elif index==2:
            cv2.rectangle(img, (face[0],face[1]),(face[2], face[3]),(172, 0, 225), 2)
            
        print(class_name)
    
    end = time.time()
    totalTime = end - start
    
    fps = 1/totalTime
    print("FPS: ", fps)
    
    #cv2.putText(img, f'FPS: {int(fps)}', (0,20), cv2.FONT_HERSHEY_TIPLEX, 1.0, (0, 0,255), 1.5)
    #cv2.putText(img, class_name, (20,200), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (0,0,255), 1.5)
    #cv2.putText(img, str(float("{:.2f}".format(confidence_score*100)))+ "%", (75,100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255,0), 2)
    
    
    #cv2.imshow("classification Resized", img_resize)
    
    cv2.imshow("classification Resized", img_resize)
    cv2.imshow("classification Original", img)
    
    if cv2.waitKey(1) == ord("q"):
        break
    
cv2.destroyAllWindows()
cap.release()


    
    
    


