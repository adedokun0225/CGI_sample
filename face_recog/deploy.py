import tensorflow.keras
from tensorflow.keras.models import load_model
import cv2 
import numpy as np
import time
#face recog deploy
#display scientific notation for clarity
np.set_printoptions(suppress=True)

#load model
#new_model = tensorflow.keras.models.load_model("face_recog/models/face_recognition_model.h5")

#load the test_labels
with open("face_recog/labels.txt", "r") as f:
    class_names = f.read().split("\n")
    
#create the array of the shape of the feed into the keras models

data = np.ndarray(shape=(1,224,224,3), dtype=np.float32)

size = (224, 224)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    
    start = time.time()
    
    ret, img = cap.read()
    
    height, width, channels = img.shape
    
    scale_value = width/height
    
    img_resize = cv2.resize(img, size, fx= scale_value, fy=1, interpolation=cv2.INTER_NEAREST)
    
    #turn image intonp array
    img_array = np.asarray(img_resize)
    
    # normalize the image
    normalize_img_array = (img_array.astype(np.float32)/127.0) - 1
    
    #load the image into the array
    data[0] = normalize_img_array
    
    #run the inference
    #prediction = new_model.predict(data)
    
    #print(prediction)
    #index = np.argmax(prediction)
    #class_name = class_names[index]
    #confidence_score = prediction[0][index]
    
    end = time.time()
    totalTime = end - start
    
    fps = 1/totalTime
    #print("FPS: ", fps)
    cv2.putText(img, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255,0), 2)
    #cv2.putText(img, class_name, (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
    #cv2.putText(img, str(float("{:.2f}".format(confidence_score*100)))+ "%", (75,100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255,0), 2)
    
    
    cv2.imshow("classification Resized", img_resize)
    cv2.imshow("classification Original", img)
    
    if cv2.waitKey(5) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
cap.release()
    
    
    
    
    
    
    
    
    


