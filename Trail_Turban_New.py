import cv2
import numpy as np


#adding image
img_turban = cv2.imread('turban.png',1)

#grayscale conversion
musgray = cv2.cvtColor(img_turban,cv2.COLOR_BGR2GRAY) 

#masking
ret, orig_mask = cv2.threshold(musgray, 225 , 255, cv2.THRESH_BINARY)
orig_mask_inv = cv2.bitwise_not(orig_mask)

#og turban height and width
ogturbanheight, ogturbanwidth = img_turban.shape[:2]

#inserting haar-cascade
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#capturing video
cap=cv2.VideoCapture(0)
ret,img=cap.read()

#video capture height and width
img_h, img_w = img.shape[:2]

#TRACKBAR
def nothing(x):
    pass
cv2.namedWindow('Turban')
cv2.createTrackbar('Color','Turban', 0, 200, nothing)

while True:
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hsvfeed=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #TRACKBAR
    b = cv2.getTrackbarPos('Color', 'Turban')

    #converting turban to hsv to use it later
    turbanhsv = cv2.cvtColor(img_turban,cv2.COLOR_BGR2HSV)

    # detecting face
    faces=face_cascade.detectMultiScale(gray,1.3,5)

    #TURBAN COLOR CHANGE
    h , s , v = cv2.split(turbanhsv)
    turbannew = cv2.merge([h+b,s-40,v])

    turbanfinal = cv2.cvtColor(turbannew,cv2.COLOR_HSV2BGR)

    for (x,y,w,h) in faces:

        #making a rectangle arround face height=h and width=w
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        #redefining face dimensions
        face_w = w
        face_h = h
        face_x1 = x
        face_x2 = face_x1 + face_h
        face_y1 = y
        face_y2 = face_y1 + face_h

        # setting the turban size in relation to tracked face
        turbanwidth = int(1.2 * face_w)
        turbanheight = int(1.7 * face_h)

        #setting turban centered wrt recognized face
        turban_x1 = face_x2 - int(face_w/2) - int(turbanwidth/2) + 5
        turban_x2= turban_x1 + turbanwidth

        # some padding between face and upper turban. Depends on the turban img
        turban_y1 = face_y1 - int(h/2.1)
        turban_y2 = turban_y1 + int(turbanheight/1.5)

        #checking for clipping
        if turban_x1 < 0:
            turban_x1 = 0
        if turban_y1 < 0:
            turban_y1 = 0
        if turban_x2> img_w:
            turban_x2= img_w
        if turban_y2 > img_h:
            turban_y2 = img_h

        #setting turban height and width
        turbanwidth = turban_x2- turban_x1
        turbanheight = turban_y2 - turban_y1
        if turbanwidth < 0 or turbanheight < 0:
            continue

        #re-sizing the original image and the masks to the turban sizes
        #resize all,the masks you made,the originla image,everything
        turban = cv2.resize(turbanfinal, (turbanwidth,turbanheight), interpolation = cv2.INTER_AREA) 
        mask = cv2.resize(orig_mask, (turbanwidth,turbanheight), interpolation = cv2.INTER_AREA)
        mask_inv = cv2.resize(orig_mask_inv, (turbanwidth,turbanheight), interpolation = cv2.INTER_AREA)

        #take ROI for turban from background equal to size of turban image
        roi = img[turban_y1:turban_y2, turban_x1:turban_x2]


        # roi_bg contains the original image only where the turban is not in the region that is the size of the turban.
        roi_bg = cv2.bitwise_and(roi,roi,mask = mask)
        roi_fg = cv2.bitwise_and(turban,turban,mask = mask_inv)
        dst = cv2.add(roi_bg,roi_fg)
        img[turban_y1:turban_y2, turban_x1:turban_x2] = dst

        break

    # Showing Image
    cv2.imshow('Turban',img)
    if cv2.waitKey(1) == ord('q'):
        break;

cap.release()
cv2.destroyAllWindows()