def detection():
    import cv2
    from cvzone.HandTrackingModule import HandDetector
    from cvzone.ClassificationModule import Classifier
    import numpy as np
    import math
    import os
    import socket

    cap= cv2.VideoCapture(0)
    detection = HandDetector(maxHands=1)

    classifier = Classifier("my_model.h5","label.txt")
    path = "Data"
    names = os.listdir(path)
    val=names
    labels =val
    print(labels)

    offset= 20
    imgSize=400
    path = "Data"

    def new(message):
        HOST = '192.168.187.177'  
        PORT = 12346          

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT)) 
            s.sendall(message.encode())
            data = s.recv(2024)

    while True:
        count = 0
        success,img =cap.read()
        imgOutput =img.copy()
        hands,img = detection.findHands(img)
        
        if hands:
            hand=hands[0]
            x,y,w,h=hand['bbox']
            imgwhile = np.ones((imgSize,imgSize,3), np.uint8)*255
            imgCrop=img[ y - offset : y + h +offset , x -offset : x + w+offset ] 
            imgCropShape = imgCrop.shape
            aspectRatio=h/w
            
            if aspectRatio>1:
                k=imgSize/h
                wCal=math.ceil(k*w)
                imgResize =cv2.resize(imgCrop,(wCal,imgSize))
                wGap=math.ceil((imgSize-wCal)/2)
                imgResizeShape = imgResize.shape
                imgwhile[:, wGap:wCal+wGap] = imgResize
                prediction,index = classifier.getPrediction(imgwhile,draw=False)
                print(prediction,index)   
            else:
                k=imgSize/w
                hCal=math.ceil(k*h)
                imgResize =cv2.resize(imgCrop,(imgSize,hCal))
                hGap=math.ceil((imgSize-hCal)/2)
                imgResizeShape = imgResize.shape
                imgwhile[hGap:hCal+hGap,:] = imgResize
                prediction,index = classifier.getPrediction(imgwhile,draw=False)
            a=labels[index] 
            print(a)
            cv2.rectangle(imgOutput,(49,49),(581,151),(255,0,25),10)
            cv2.rectangle(imgOutput,(50,50),(580,150),(255,0,156),cv2.FILLED)
            cv2.putText(imgOutput,"Text : "+a, (100,100), cv2.FONT_HERSHEY_COMPLEX , 1, (0,0,0),2)  

            cv2.putText(imgOutput,labels[index],(x,y-25),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)

            cv2.imshow("Imagewhile",imgOutput)
            new(a)        
        cv2.waitKey(1)