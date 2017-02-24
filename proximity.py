import serial
import numpy as np
from threading import Thread
import time

class proximity(Thread):
	def __init__(self):

		Thread.__init__(self)

		self.serial_port = serial.Serial(port='/dev/tty.usbmodem14241', baudrate=115200)

		self.prox_read = 0


	def read_value(self):
		"""
		while True:
			try:
				self.prox_read = int(self.serial_port.readline())
				break
			except ValueError:
				continue
		
		return self.prox_read
		"""

		self.serial_port.write('g')

		return int(self.serial_port.readline())