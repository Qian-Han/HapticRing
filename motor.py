import serial
import numpy as np

class motor(object):

	def __init__(self):
		self.serial_port = serial.Serial(port='/dev/tty.usbmodem1421', baudrate=115200)
		self.trigger_state = 0

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
		print(self.trigger_state)

	def get_angle(self, val):
		print(val)



