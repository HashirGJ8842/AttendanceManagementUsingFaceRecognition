#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import Tk
from Tkinter import  *
import train_model

import cv2
import numpy as np
from PIL import Image
import os

class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='First number')
        self.lbl1.place(x=100, y=50)
        self.lbl2=Label(win, text='Second number')
        self.lbl2.place(x=100, y=100)
        self.lbl3=Label(win, text='Result')
        self.lbl3.place(x=100, y=200)
        self.t1=Entry(bd=3)
        self.t2=Entry()
        self.t3=Entry()
        self.btn1 = Button(win, text='Add')
        self.btn2=Button(win, text='Subtract')
        self.b1 = Button(win, text='Add', command=self.TrainImages)
        self.t1.place(x=200, y=50)

        self.t2.place(x=200, y=100)
        self.b1=Button(win, text='Add')
        self.b1.place(x=100, y=150)

        self.t3.place(x=200, y=200)


    def TrainImages(self):
        # Path for face image database
        path = 'train_data'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml");
        # # function to get the images and label data
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        imagePaths.remove('train_data/.DS_Store')
        faceSamples = []
        ids = []

        def getImagesAndLabels(path):
            for imagePath in imagePaths:
                images = [os.path.join(imagePath, f) for f in os.listdir(imagePath)]
                for image in images:
                    PIL_img = Image.open(image).convert('L')  # grayscale
                    img_numpy = np.array(PIL_img, 'uint8')
                    id = int(os.path.split(image)[0].split("/")[1])
                    faces = detector.detectMultiScale(img_numpy)
                    for (x, y, w, h) in faces:
                        faceSamples.append(img_numpy[y:y + h, x:x + w])
                        ids.append(id)
            return faceSamples, ids

        def TrainModel():
            print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
            path = 'train_data'
            faces, ids = getImagesAndLabels(path)
            recognizer.train(faces, np.array(ids))
            # Save the model into trainer/trainer.yml
            recognizer.write('trainer/trainer.yml')
            # Print the numer of faces trained and end program
            return "\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids)))



window=Tk()
mywin=MyWindow(window)
window.title('Hello Python')
window.geometry("400x300+10+10")
window.mainloop()