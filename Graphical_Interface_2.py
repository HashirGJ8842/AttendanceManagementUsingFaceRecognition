from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import cv2
import time
import Employee
import os


class MarkingAttendance:
    def function_MA(self):
        self.thread = threading.Thread(target=self.MA_videoLoop, args=())
        self.thread.start()

    def function_TI(self):
        self.thread = threading.Thread(target=self.TI_videoLoop, args=())
        self.thread.start()

    def TI_videoLoop(self):
        os.chdir("train_data")

        def checkDirectory(emp_id):
            """
            Check if a directory for that employee id exists. If it exits then change directory and save the new images to it.
            Else create a directory,change to it and store in it.
            :return:
            """
            if str(emp_id) in os.listdir(os.getcwd()):
                os.chdir(str(emp_id))
                return "Changed Directory to " + str(emp_id)
            else:
                os.mkdir(str(emp_id))
                os.chdir(str(emp_id))
                return "Creating a new directory"

        def captureImage(emp_id):
            i = 0
            checkDirectory(emp_id)
            while i < 30:
                # raw_input('Press Enter to capture')
                return_value, self.frame = self.vs.read()
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=3,
                    minSize=(30, 30)
                )
                for (x, y, w, h) in faces:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                height, width = self.frame.shape[:2]

                for (x, y, w, h) in faces:
                    r = max(w, h) / 2
                    centerx = x + w / 2
                    centery = y + h / 2
                    nx = int(centerx - r)
                    ny = int(centery - r)
                    nr = int(r * 2)

                    faceimg = self.frame[ny:ny + nr, nx:nx + nr]
                    lastimg = cv2.resize(faceimg, (512, 512))
                    status = cv2.imwrite(str(emp_id) + '_' + str(i) + '.jpg', lastimg)
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)


                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

                print("[INFO] Found {0} Faces!".format(len(faces)))
                i += 1
                self.welcomeLabel.config(text=f'Took {i} images, found {len(faces)} faces', bg='lightgreen')
                self.btn1.config(text="Close", command=self.onClose)

        captureImage(self.name)

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
                self.label1.config(text=result + ' ' + name, bg="lightgreen")
                break

            if self.panel is None:
                self.panel = tki.Label(image=image)
                self.panel.image = image
                self.panel.pack(side="left", padx=10, pady=10)


            else:
                self.panel.configure(image=image)
                self.panel.image = image
            cv2.waitKey(1)

    def enter_bar(self):
        self.entry.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
        self.btn1.config(text="Proceed", command=self.function_TI)

    def onClose(self):
        print("[INFO] closing...")
        self.stopEvent.set()
        self.root.quit()
        self.vs.release()

    def next_function(self):
        self.name = self.enter_id.get()
        self.enter_id.pack_forget()
        self.enterLabel.pack_forget()
        self.welcomeLabel = tki.Label(text=f'Welcome {self.name}', bg="lightgreen")
        self.welcomeLabel.pack(side="bottom", fill="both", expand="yes", padx=10,
                         pady=10)
        self.btn1.config(text="Train", command=self.function_TI)
    def initial(self):
        self.enterLabel = tki.Label(text=f'Enter ID', bg="lightblue")
        self.enterLabel.pack(fill="both", expand="yes", padx=10,
                               pady=10)
        self.enter_id = tki.Entry(self.root)
        self.enter_id.pack(fill="both", expand="yes", padx=10,
                        pady=10)
        self.btn1 = tki.Button(self.root, text='Proceed', command=self.next_function)
        self.btn1.pack(side="bottom", fill="both", expand="yes", padx=10,
                       pady=10)
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

        self.initial()

        self.root.wm_title("Face Recognition")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


print("[INFO] warming up camera...")
vs = cv2.VideoCapture(0)
time.sleep(2.0)

pba = MarkingAttendance(vs)
pba.root.mainloop()