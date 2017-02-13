import serial
import numpy as np

class motor(object):

	def __init__(self):
		self.serial_port = serial.Serial(port='/dev/tty.usbmodem1421', baudrate=115200)
		self.trigger_state = 0
		self.val = 0
		self.ready_to_stop_motor = 90
		self.ready_to_stop_sensor = 180

	def close(self):
		self.serial_port.close()

	def write_serial(self, val_string):
		self.serial_port.write(val_string)

	def tune_up(self, event):
		self.serial_port.write("q")

	def tune_down(self, event):
		self.serial_port.write("z")

	def reset(self, event):
		self.trigger_state = 0
		print(self.trigger_state)

	def tick(self, event):
		self.trigger_state = 1
		print(self.trigger_state)

	def spring(self, event):
		self.trigger_state =2
		self.serial_port.write("g")	
		print(self.trigger_state)

	def get_ready(self):
		self.serial_port.write("g")

	def get_angle(self, val):
		#print(val)
		if self.trigger_state == 2: #spring
			val_interval = val - self.val
			if val_interval >=3 and val <= 180:
				self.serial_port.write("m")  #step down
				print("motor move")
				self.val = val

			if val > 180:
				if self.val != 0:
					self.val = 0






