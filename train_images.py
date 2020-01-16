import os
import cv2
os.chdir("train_data")

def checkDirectory(emp_id):
    """
    Check if a directory for that employee id exists. If it exits then change directory and save the new images to it.
    Else create a directory,change to it and store in it.
    :return:
    """
    if str(emp_id) in os.listdir(os.getcwd()):
        os.chdir(str(emp_id))
        return "Changed Directory to "+str(emp_id)
    else :
        os.mkdir(str(emp_id))
        os.chdir(str(emp_id))
        return "Creating a new directory"

def captureImage(emp_id):
    i = 0
    checkDirectory(emp_id)
    camera = cv2.VideoCapture(0)
    while i < 5:
        raw_input('Press Enter to capture')
        return_value, image = camera.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        height, width = image.shape[:2]

        for (x, y, w, h) in faces:
            r = max(w, h) / 2
            centerx = x + w / 2
            centery = y + h / 2
            nx = int(centerx - r)
            ny = int(centery - r)
            nr = int(r * 2)

            faceimg = image[ny:ny + nr, nx:nx + nr]
            lastimg = cv2.resize(faceimg, (512, 512))
            status = cv2.imwrite(str(emp_id) + '_' + str(i) + '.jpg', lastimg)

        print("[INFO] Found {0} Faces!".format(len(faces)))
        i += 1
    del(camera)







