import cv2
import numpy as np
import math
import time
import tkinter as tk
from PIL import Image, ImageTk
from cvzone.HandTrackingModule import HandDetector
import os
from cvzone.ClassificationModule import Classifier
import socket
import threading
import os

root = tk.Tk()
root.title("Hand Detection App")

video_label = tk.Label(root)
video_label.pack(side='left')
video_label.pack(side='top')

processed_label = tk.Label(root)
processed_label.pack(side='left')
processed_label.pack(side='bottom')

cap = cv2.VideoCapture(0)

detection = HandDetector(maxHands=1)
offset = 20
img_size = 500
folder = "Data"
counter = 0
success, img = cap.read()


def process_frame():
    global counter
    success, img = cap.read()
    hands, img = detection.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        img_while = np.ones((img_size, img_size, 3), np.uint8)*255
        img_crop = img[y-offset:y+h+offset, x-offset:x+w+offset]
        img_crop_shape = img_crop.shape
        aspect_ratio = h/w
        if aspect_ratio > 1:
            k = img_size/h
            w_cal = math.ceil(k*w)
            img_resize = cv2.resize(img_crop, (w_cal, img_size))
            w_gap = math.ceil((img_size-w_cal)/2)
            img_resize_shape = img_resize.shape
            img_while[:, w_gap:w_cal+w_gap] = img_resize
        else:
            k = img_size/w
            h_cal = math.ceil(k*h)
            img_resize = cv2.resize(img_crop, (img_size, h_cal))
            h_gap = math.ceil((img_size-h_cal)/2)
            img_resize_shape = img_resize.shape
            img_while[h_gap:h_cal+h_gap,:] = img_resize
        processed_image = Image.fromarray(img_while)
        processed_image = ImageTk.PhotoImage(processed_image)
        processed_label.config(image=processed_image)
        processed_label.image = processed_image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (540, 380))
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    video_label.config(image=img)
    video_label.image = img
    root.after(10, process_frame)

def button_click():
    ret, img = cap.read()
    counter =0
    hands, img = detection.findHands(img)
    hand = hands[0]
    x, y, w, h = hand['bbox']
    img_crop = img[y-offset:y+h+offset, x-offset:x+w+offset]
    
    folder = 'Data/'+entry.get()
    cv2.imwrite(f'{folder}/image_{time.time()}.jpg',img_crop )
    counter += 1
    print(f'{counter} images saved.')

def create_folder():
    os.makedirs('Data/'+entry.get())

def train_model():
    import training as tr
    tr.training_data()
    new_button.config(state='active')

def train_thread():
    new_button.config(state="disabled")
    threading.Thread(target=train_model).start()

def open_window():
    import sign_detector_client as sdc
    sdc.detection()
    sdc.detect()

label = tk.Label(root, text="Enter Folder Name:")
label.pack(padx=10)
entry = tk.Entry(root)
entry.pack(padx=10)
button1 = tk.Button(root, text="Create Folder", command=create_folder) 

button1.pack(padx=10)
button = tk.Button(root, text="collect the images", command=button_click)
button.pack(padx=10)
new_button = tk.Button(root, text="Train the data",command=train_thread )
new_button.pack(padx=10)
button = tk.Button(root, text="Detection", command=open_window)
button.pack()
close_button = tk.Button(root, text="Close", command=root.destroy)
close_button.pack()

process_frame()
root.mainloop()
