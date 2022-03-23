from click import NoSuchOption
from cv2 import CAP_REALSENSE
from django.shortcuts import render
from django.http import StreamingHttpResponse,HttpResponse,HttpResponseServerError
import cv2
import time
from matplotlib.pyplot import gray
import numpy as np

# Create your views here.
# def index(request):
#     return render(request, 'index.html')
    
def about(request):
    return HttpResponse("this is aboutpage")

def services(request):
    return HttpResponse("this is servicepage")


def contact(request):
    return HttpResponse("this is contactpage")

def gen(camera):
    while True:
        frame  = camera.get_frame()
        # frame =  cv2.cvtColor(apple, cv2.COLOR_BGR2GRAY)
        # filter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' +frame + b'\r\n\r\n')

class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(1)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,image = self.video.read()
        ret,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()
 
def stream(request):
    # response = HttpResponse(gen(VideoCamera())
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")
    
    
def home(request):
    return HttpResponse("WELCOME BUDDY")

def camera(self):
    cap = cv2.VideoCapture(1)

    while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # np.outer.write(frame)

            # cv2.imshow('frame', frame)
            cv2.imshow('gray', gray) 
            cv2.waitKey(5) 
            # return HttpResponse(cv2.imshow("Result", gray))

            # yield(b'--frame\r\n'
            #     b'Content-Type: image/jpeg\r\n\r\n' +frame + b'\r\n\r\n')



def trial(s):
    try:
        return StreamingHttpResponse(camera(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")
    