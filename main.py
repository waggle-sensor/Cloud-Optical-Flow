from threading import Thread
from queue import Queue
import numpy as np
import cv2 as cv
import time 
import openpyxl
def create_video_capture_queue(device, queue_size=30, fps=None, quiet=False):
    frames = Queue(queue_size)
    

    def video_capture_worker():
        capture = cv.VideoCapture(device)
        next_cap = time.time()
        current_time = next_cap
        while capture.isOpened():
            current_time = time.time()
            ok, frame = capture.read()
            if not ok and not quiet:
                raise RuntimeError("failed to capture frame")
            elif fps is None: 
                frames.put(frame)
            elif current_time >= next_cap:
                frames.put(frame)
                next_cap = current_time + 1./fps

    Thread(target=video_capture_worker, daemon=True).start()
    return frames
cap = cv.VideoCapture(cv.samples.findFile("movieON20191121.mpg"))
ret, frame1 = cap.read()
prvs = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while(1):
    ret, frame2 = cap.read()
    next = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv.normalize(mag,None,0,255,cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
    cv.imshow('frame2',bgr)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv.imwrite('opticalfb.png',frame2)
        cv.imwrite('opticalhsv.png',bgr)
    pixel_y = 320
    pixel_x = 192
    #print(f'the velocity vector at pixel (y=10,x=15) is {flow[pixel_x,pixel_y]}')
    prvs = next
    magnitude = np.linalg.norm(flow[pixel_x,pixel_y])
    print(magnitude)
quit()
