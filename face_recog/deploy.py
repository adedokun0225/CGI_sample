import tensorflow.keras
import cv2
import numpy as np
import time

#display scientific notation for clarity
np.set_printoptios(suppress=True)

#load model
model = tensorflow.keras.models.load_model("face_recognition_model.h5")

#load the test_labels
with open("labels.txt", "r") as f:
    class_names = f.read().split("\n")
    
#create the array of the shape of the feed into the keras models

data = np.ndarray(shape=(1,224,224,3), dtype=np.float32)

size = (224, 224)
ClosedResourceError
cap = cv2.VideoCapture(0)

while cap.isopened():
    
    ret, img = cap.read()
    
    height, width, channels = img.Shape
    
    scale_value = width/height
    
    img_resize = cv2.resize(img, size, fx= scale_value, fy=1, interpolation=cv2.INTER_NEAREST)
    
    #turn image intonp array
    img_array = np.asarray(img_resize)
    
    # normalize the image
    normalize_img_array = (img_array.astype(np.float32)/127.0) - 1
    
    #load the image into the array
    data[0] = normalize_img_array
    
    #run the inference
    prediction = model.predict(data)
    
    #print(prediction)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    
    end = time.time()
    totalTime = end - start
    
    fps = 1/totalTime
    
    
    cv2.imshow("classification Resized", img_resize)
    cv2.imshow("classification Original", img)
    
    if cv2.waitkey(5) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
cap.release()
    
    
    
    
    


