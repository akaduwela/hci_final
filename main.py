from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import numpy as np


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

counter = 0
meme_counter = 0
meme = False

lookaway = False
memescreen = False

def lookaway(instance):
	global lookaway, counter
	if (lookaway):
		print("Lookaway deactivated!")
		lookaway = False
	else:
		print("Lookaway activated!")
		lookaway = True
	counter = 0

def memescreen(instance):
	global memescreen, meme_counter
	if (memescreen):
		print("memescreen deactivated!")
		memescreen = False
	else:
		print("memescreen activated!")
		memescreen = True
	meme_counter = 0

class CamApp(App):

	def build(self):
		self.img1 = Image(source='images/1.jpg')
		layout = BoxLayout(padding=10, orientation="vertical")
		sublayout1 = BoxLayout(padding=10, orientation="horizontal")
		sublayout2 = BoxLayout(padding=10, orientation="horizontal")

		button1 = Button(text="Lookaway!")       	
		button2 = Button(text="Memes") 
		button1.bind(on_press=lookaway)
		button2.bind(on_press=memescreen)


		sublayout1.add_widget(self.img1)

		sublayout2.add_widget(button1)
		sublayout2.add_widget(button2)

		layout.add_widget(sublayout1)
		layout.add_widget(sublayout2)

		#opencv2 stuffs
		self.capture = cv2.VideoCapture(0)
		ret, frame = self.capture.read()
		cv2.namedWindow("CV2 Image")
		cv2.imshow("CV2 Image", frame)
		Clock.schedule_interval(self.update, 1.0/33.0)
		return layout

	def CreateImage(self, height, width, bits=np.uint8, channels=3, color=(0, 0, 0)): # (cv.GetSize(frame), 8, 3)
		"""Create new image(numpy array) filled with certain color in RGB"""
		# Create black blank image
		if bits == 8:
			bits = np.uint8
		elif bits == 32:
			bits = np.float32
		elif bits == 64:
			bits = np.float64
		image = np.zeros((height, width, channels), bits)
		if color != (0, 0, 0):
		    # Fill image with color
		    image[:] = color
		return image

	def update(self, dt):
		# display image from cam in opencv window
		global counter, meme_counter, meme
		ret, frame = self.capture.read()
		cv2.imshow("CV2 Image", frame)
		# convert it to texture
		buf1 = cv2.flip(frame, 0)
		buf = buf1.tostring()
		texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
		texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
		# display image from the texture
		self.img1.texture = texture1

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		if (lookaway):
			counter += 1
		
		if (memescreen):
			meme_counter += 1
		
		for (x,y,w,h) in faces:
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]

			eyes = eye_cascade.detectMultiScale(roi_gray)
			eyes = list(eyes)

			smile = smile_cascade.detectMultiScale(roi_gray, 1.8, 8)
			smile = list(smile)


			
			if (len(eyes) == 2):
				for(ex,ey,ew,eh) in eyes:
					#print("eyes")
					cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
				counter = 0
			

			if (len(smile) >= 1):
				for(sx,sy,sw,sh) in smile:
					cv2.rectangle(roi_color, (sx,sy), (sx+sw, sy+sh), (0,0,255), 2)
				meme_counter = 0
				meme = False

			else:
				if (len(eyes) > 1):
					meme_counter += 1
					#print(meme_counter)        


		if (counter > 100):
			print("WAKE UP!")

		if (meme_counter > 100):
			print("Loading meme... ")
			meme = True




if __name__ == '__main__':
	CamApp().run()