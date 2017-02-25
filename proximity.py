import serial
import numpy as np
from threading import Thread
import threading
import time

class proximity(Thread):
	def __init__(self):

		Thread.__init__(self)

		self.serial_port = serial.Serial(port='/dev/tty.usbmodem14241', baudrate=115200)

		self.prox_read = 0
		self.read_val = 0
        	


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


		while True:
			try:
				self.prox_read = int(self.serial_port.readline())
				break
			except ValueError:
				continue

		#return self.prox_read  #int(self.serial_port.readline())

	def close(self):
		while self.serial_port.inWaiting():
			self.read_val = self.serial_port.read(self.serial_port.inWaiting())
			print("IR Read:%s" % (binascii.hexlify(self.read_val)))


	def read_value_thread(self):
		t1 = Thread(target = self.read_value)

		t1.start()
		t1.join()

		return self.prox_read 