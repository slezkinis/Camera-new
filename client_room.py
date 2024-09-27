# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64
import websocket
import json
import RPi.GPIO as GPIO


BUFF_SIZE = 65536
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
BUFF_SIZE = 65536
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:8000/closed_room/1")
fps,st,frames_to_count,cnt = (0,0,20,0)
vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam
while True:
    while(vid.isOpened()):
        WIDTH=400
        _,frame = vid.read()
        frame = imutils.resize(frame,width=WIDTH)
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buffer)
        ws.send_binary(message)
        # ws.send({"id": 1, "data": message.decode()})
        answ = json.loads(ws.recv_data()[1])
        if answ["is_open"]:
            GPIO.output(14, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(14, GPIO.LOW)
        frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        # cv2.imshow('TRANSMITTING VIDEO',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            ws.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st=time.time()
                cnt=0
            except:
                pass
        cnt+=1
        time.sleep(0.3)

