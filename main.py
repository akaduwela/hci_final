from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader
from kivy.core.window import Window



import cv2
import numpy as np
import random


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')


src_path = 'memes/'

meme_dict = {0: "drake.jpg", 1:"jesus.png", 2:"kermit.jpg", 3:"pikachu.png", 4:"you-can-do-it-meme-3-1.jpeg"}


counter = 0
meme_counter = 0

meme = False
alarm = False

lookaway = False
memescreen = False

lookaway_threshold = 100
meme_threshold = 100

alarm_sound = SoundLoader.load('sounds/alarm.mp3')
notif_sound = SoundLoader.load('sounds/notif.mp3')


def on_text1(instance, value):
	global lookaway_threshold
	lookaway_threshold = int(value)*33
	
def on_text2(instance, value):
	global meme_threshold
	meme_threshold = int(value)*33


settingslayout = BoxLayout(padding=10, orientation='vertical')
set_subbox1 = BoxLayout(padding=10, size_hint=(1,0.4), orientation='vertical')
set_subbox2 = BoxLayout(padding=10, size_hint=(1,0.4), orientation='vertical')
set_subbox3 = BoxLayout(padding=10, size_hint=(1,0.2), orientation='horizontal')

alarm_input = TextInput(text="Enter wait time (s)", multiline=False)
alarm_label = Label(text="Enter time to wait for lookaway:")
meme_input = TextInput(text="Enter wait time (s)", multiline=False)
meme_label = Label(text="Enter time to wait for memescreen:")


alarm_input.bind(text=on_text1)
meme_input.bind(text=on_text2)

set_btn = Button(text="Save")


set_subbox1.add_widget(alarm_label)
set_subbox1.add_widget(alarm_input)
set_subbox2.add_widget(meme_label)
set_subbox2.add_widget(meme_input)


set_subbox3.add_widget(set_btn)


settingslayout.add_widget(set_subbox1)
settingslayout.add_widget(set_subbox2)
settingslayout.add_widget(set_subbox3)

settings = Popup(title="Settings",
				content=settingslayout, size=(400,400))
set_btn.bind(on_press=settings.dismiss)


def on_save(instance):
	settings.dismiss()

def lookaway(instance):
	global lookaway, counter, alarm_sound
	if (lookaway):
		print("Lookaway deactivated!")
		lookaway = False
		alarm_sound.stop()
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
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

		self.img1 = Image(source='images/1.jpg')
		layout = BoxLayout(padding=10, orientation="vertical")
		sublayout1 = BoxLayout(padding=10, orientation="horizontal", size_hint = (1,0.8))
		sublayout2 = BoxLayout(padding=10, orientation="horizontal", size_hint = (1,0.2))

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


	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None

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
		global counter, meme_counter, meme, alarm, lookaway, memescreen, alarm_sound, notif_sound, meme_threshold, lookaway_threshold
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


		if (meme):
			## load meme here
			idx = random.randint(0,4)
			meme_src = src_path + meme_dict[idx]
			box = BoxLayout(padding=10, orientation='vertical')
			subbox1 = BoxLayout(padding=10, size_hint=(1, 0.8))
			subbox2 = BoxLayout(padding=10, size_hint=(1, 0.2))

			subbox1.add_widget(Image(source=meme_src))
			dismiss_btn = Button(text='Back to work!')
			
			subbox2.add_widget(dismiss_btn)

			box.add_widget(subbox1)
			box.add_widget(subbox2)
			popup = Popup(title = 'MEME', 
				content=box, size=(400,400))

			dismiss_btn.bind(on_press=popup.dismiss)
			popup.open()
			

			if(notif_sound):
				notif_sound.play()
			print("meme loaded!")
			meme = False
			meme_counter = meme_counter/2

		if (alarm):
			print("WAKE UP!")
			if(alarm_sound):
				alarm_sound.play()
			alarm = False
			counter = counter/2

		if (lookaway):
			counter += 1
			
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
					if (memescreen):
						print(meme_counter)
						meme_counter += 1
					#print(meme_counter)        

		if (lookaway):
			if (counter > lookaway_threshold):
				alarm = True

		if (memescreen):
			if (meme_counter > meme_threshold):
				print("Loading meme... ")
				meme = True

	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		global alarm_sound, counter, meme_counter, settings
		if keycode[1] == 'm':
			if (alarm_sound):
				alarm_sound.stop()
		if keycode[1] == 's':
			settings.open()
		if keycode[1] == 'q':
			if (settings):
				settings.dismiss()
		return True


if __name__ == '__main__':
	CamApp().run()