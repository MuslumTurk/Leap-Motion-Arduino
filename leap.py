import sys
sys.path.append("/usr/lib/Leap/lib")
sys.path.append("/usr/lib/Leap/lib/x64")
sys.path.append("/usr/lib/Leap/lib")
import thread,time, Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Tkinter import *
import Tkinter
from PIL import Image,ImageTk
import cv2, math, ctypes
import numpy as np
import serial

class LeapMotion(Leap.Listener):
	finger_names = ['Thumb','Index','Middle','Ring','Pinky']
	bone_names = ['Metacarpal','Proximal','Indermediate','Distal']
	state_names = ['STATE_INVALID','STATE_START','STATE_UPDATE','STATE_END']
	yukari_asagi = []
	saga_sola = []
	ileri_geri = []
	durum  = []
	yon = 0
	yukariasagi = 0
	ser = serial.Serial("/dev/ttyUSB0", 9600)

	def on_init(self,controller):
		print "Motion Started"

	def on_connect(self,controller):
		print "Motion Connected"
# ---------------------- enabled to gestures
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self,controller):
		print "Motion Baglantisi Kesildi"
		self.ser.close()

	def on_exit(self,controller):
		print "Motion Existed"
	
	def on_frame(self,controller):
		frame = controller.frame()
		interactionBox = frame.interaction_box
		self.scale = 1.0 
		self.kaydirma_miktari = 20
		
		for hand in frame.hands:
			handType = "Left Hand -> " if hand.is_left else "Right Hand ->"
			print handType + "\t Hand ID:"+str(hand.id)+"\t x:"+str(hand.palm_position[0])+"\t y:"+str(hand.palm_position[1]) +"\t z:"+str(hand.palm_position[2])

			self.yukari_asagi.append(hand.palm_position[1])
			self.saga_sola.append(hand.palm_position[0])

			self.pinch = hand.pinch_strength
			print ">>>>>>>>>>>>>>>>>>>>><<PINCH :"+ str(self.pinch) +">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#------------------------------ left right control -------------------------------
			if len(self.saga_sola) > 1:
				if self.saga_sola[0]+1 < self.saga_sola[1]:
					
					self.yon = self.yon+self.kaydirma_miktari
					self.updateCircle(self.pinch,self.yon,self.yukariasagi)
					print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<pedal saga"
					self.ser.write("Muslum Turk6")
				elif self.saga_sola[0] > self.saga_sola[1]+1:
					self.yon = self.yon-self.kaydirma_miktari
					self.updateCircle(self.pinch,self.yon,self.yukariasagi)
					print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<pedal sola"
					self.ser.write("Muslum Turk4")

				else:
					self.updateCircle(self.pinch,self.yon,self.yukariasagi)
					self.ser.write("Muslum Turk0")
				
				self.saga_sola[:] = []
#------------------------------ up down control -------------------------------------

			if len(self.yukari_asagi) > 1:
				if self.yukari_asagi[0]+1 < self.yukari_asagi[1]:
					self.yukariasagi = self.yukariasagi-self.kaydirma_miktari
					self.updateCircle(self.pinch,self.yon,self.yukariasagi)
					print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<pedal yukari"
					self.ser.write("Muslum Turk8")

				elif self.yukari_asagi[0] > self.yukari_asagi[1]+1:
					self.yukariasagi = self.yukariasagi+self.kaydirma_miktari
					self.updateCircle(self.pinch,self.yon,self.yukariasagi)
					print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<pedal asagi"
					self.ser.write("Muslum Turk2")
				else:
					self.updateCircle(self.pinch,self.yon,self.yukariasagi)
					self.ser.write("Muslum Turk0")

				self.yukari_asagi[:] = []	
		
#--------------------------- gesture contoll -----------------------------

		for gesture in frame.gestures():
		# ------------------ Circle Detected
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)
				print "Circle ID :"+str(circle.id) + "\tProgress :"+str(circle.progress) +"\tRadius :"+str(circle.radius)
				if circle.id > 3:
					self.ser.write("cirleq")
		# -------------- Swipe Detected	
			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture)
				print "Swipe ID :"+str(swipe.id)+"\t State :"+self.state_names[gesture.state]+"\tPosition :"+str(swipe.position)+"\t Speed (mm/s):"+str(swipe.speed)
		# --------------- ScreenTap Detected	
			if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
				screentap = ScreenTapGesture(gesture)
				print "ScreenTap ID :"+str(gesture.id) + "\t 	State :"+self.state_names[gesture.state] + "\t Position :"+str(screentap.position)
		# --------------  KeyTap Detected
			if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
				keytap = KeyTapGesture(gesture)
				print "KeyTap ID :"+str(keytap.id)
				if keytap.id > 3:
					self.ser.write("keytapw")
	
	def set_canvas(self, canvas):
		self.paintCanvas = canvas

#------------------------------- create image and control --------------------------------- 
	def updateCircle( self, gelenpinch , sagsol, yukariasagi):
		hassasiyet = 2

		if gelenpinch == 0:
			gelenpinch =0.1
		end =  int(gelenpinch  * 700)
		self.durum.append(end)
		
		if len(self.durum) > 1:
			self.original = Image.open('penguen.jpg')

			if gelenpinch > 0.4:
				self.original = self.original.resize((end, end), Image.ANTIALIAS)	
	# ------------------------  created image
			self.image = ImageTk.PhotoImage(self.original)
			self.paintCanvas.create_image(sagsol, yukariasagi, image=self.image, anchor=NW, tags="IMG")
			self.original = self.original.resize((end, end), Image.ANTIALIAS)
			self.paintCanvas.pack(expand=YES , fill = BOTH)

	#----------------------- image movement rigth
			if int(self.durum[0])+hassasiyet < int(self.durum[1]) :
				if gelenpinch > 0.4:
					self.original = self.original.resize((end, end), Image.ANTIALIAS)
				self.image = ImageTk.PhotoImage(self.original)
				self.paintCanvas.create_image(sagsol, yukariasagi, image=self.image, anchor=NW, tags="IMG")
				self.paintCanvas.pack(expand=YES , fill = BOTH)

	#----------------------- image movement left 
			if int(self.durum[0])-hassasiyet > int(self.durum[1]):
				if gelenpinch > 0.4:
					self.original = self.original.resize((end, end), Image.ANTIALIAS)
				self.image = ImageTk.PhotoImage(self.original)
				self.paintCanvas.create_image(sagsol, yukariasagi, image=self.image, anchor=NW, tags="IMG")
				self.paintCanvas.pack(expand=YES , fill = BOTH)
			self.durum[:] = []

#------------------------- leap motion and PaintCanvas ----------------------------
class PaintBox(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.leap = Leap.Controller()
		self.painter = LeapMotion()
		self.leap.add_listener(self.painter)
		self.pack( expand = YES, fill = BOTH )
		self.master.title( "...Leap Motion..." )

		self.paintCanvas = Canvas(self,width = "900" , height="800" )
		self.paintCanvas.pack(expand=YES , fill = BOTH)
		self.painter.set_canvas(self.paintCanvas)
		mainloop()

#--------------------------- started leap motion -----------------------------------
def main():
	PaintBox()
	listener  = LeapMotion()
	controller = Leap.Controller()
	controller.add_listener(listener)
	print "Press Enter Key with Exit "
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		#leap motion remove listener
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()