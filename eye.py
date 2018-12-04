import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

cascade = cv.CascadeClassifier('haarcascade_eye.xml')

while(True):

	ret, frame = cap.read()
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	eyes = cascade.detectMultiScale(gray, 1.3, 6)

	for(x,y,w,h) in eyes:
		cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

	cv.imshow('Frame', frame)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
