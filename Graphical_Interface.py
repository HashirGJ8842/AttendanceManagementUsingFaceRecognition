from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import cv2
import time
import Employee


class MarkingAttendance:
    def func(self):
        self.thread = threading.Thread(target=self.MA_videoLoop, args=())
        self.thread.start()

    def MA_videoLoop(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX
        id = 0
        minW = 0.1 * self.vs.get(3)
        minH = 0.1 * self.vs.get(4)
        confidence = 0

        while True:

            ret, self.frame = self.vs.read()
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )
            print(faces)

            for (x, y, w, h) in faces:
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # If confidence is less them 100 ==> "0" : perfect match
                if (confidence < 100):
                    confidence_percent = "  {0}%".format(round(100 - confidence))
                    confidence = round(100 - confidence)
                    print(confidence)
                    print(id)
                else:
                    id = "unknown"
                    confidence_percent = "  {0}%".format(round(100 - confidence))
                    confidence = round(100 - confidence)

                cv2.putText(
                    self.frame,
                    str(id),
                    (x + 5, y - 5),
                    font,
                    1,
                    (255, 255, 255),
                    2
                )

            if confidence > 65:
                # print("Match Found, Marking Attendance!")
                result = Employee.Employee(id).addAttendance(method="Face")
                name = Employee.Employee(id).fullName()
                print(result)
                self.label1.config(text=result+' '+name, bg="lightgreen")
                break

            if self.panel is None:
                self.panel = tki.Label(image=image)
                self.panel.image = image
                self.panel.pack(side="left", padx=10, pady=10)


            else:
                self.panel.configure(image=image)
                self.panel.image = image
            cv2.waitKey(1)

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.root.quit()
        self.vs.release()

    def __init__(self, vs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tki.Tk()
        self.panel = None

        self.vs.set(3, 480)
        self.vs.set(4, 480)
        self.stopEvent = threading.Event()

        self.label1 = tki.Label(self.root)
        self.label1.pack(side="bottom", fill="both", expand="yes", padx=10,
                         pady=10)
        btn1 = tki.Button(self.root, text="Train")
        btn1.pack(side="bottom", fill="both", expand="yes", padx=10,
                  pady=10)
        btn2 = tki.Button(self.root, text="Mark Attendance", command=self.func)
        btn2.pack(side="bottom", fill="both", expand="yes", padx=10,
                  pady=10)
        btn3 = tki.Button(self.root, text="Display")
        btn3.pack(side="bottom", fill="both", expand="yes", padx=10,
                  pady=10)

        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


print("[INFO] warming up camera...")
vs = cv2.VideoCapture(0)
time.sleep(2.0)

pba = MarkingAttendance(vs)
pba.root.mainloop()
