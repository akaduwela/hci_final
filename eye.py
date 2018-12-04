import cv2 as cv
import numpy as np
import time


cap = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv.CascadeClassifier('haarcascade_smile.xml')

counter = 0
meme_counter = 0
while(True):

	ret, frame = cap.read()
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)


	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]

		eyes = eye_cascade.detectMultiScale(roi_gray)
		eyes = list(eyes)
	
		smile = smile_cascade.detectMultiScale(roi_gray, 1.8, 8)
		smile = list(smile)

		if (len(eyes) == 2):
			for(ex,ey,ew,eh) in eyes:
				cv.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
			counter = 0
		else:
			counter += 1
			#print(counter)

		if (len(smile) >= 1):
			for(sx,sy,sw,sh) in smile:
				cv.rectangle(roi_color, (sx,sy), (sx+sw, sy+sh), (0,0,255), 2)
			meme_counter = 0

		else:
			if (len(eyes) > 1):
				meme_counter += 1
				#print(meme_counter)
	
	if (counter > 100):
		print("WAKE UP!")

	if (meme_counter > 100):
		print("Loading meme... ")
	cv.imshow('Frame', frame)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
