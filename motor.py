import serial
import numpy as np
from threading import Thread
import time

class motor(Thread):
	
		

	def __init__(self):
		Thread.__init__(self)

		self.serial_port = serial.Serial(port='/dev/tty.usbmodem1421', baudrate=115200)

		self.trigger_state = 0
		self.val = 0
		self.ready_to_stop_motor = 90
		self.ready_to_stop_sensor = 180
		self.tick_step = 0
		self.spring_step = 0
		self.is_ready = 0
		self.step_count = 0

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
		self.serial_port.write("g")	
		self.tick_step = 0
		self.step_count = 0
		print(self.trigger_state)


	def spring(self, event):
		self.trigger_state =2
		self.serial_port.write("g")	
		self.is_ready = 1
		self.step_count = 0
		self.spring_step = 0
		print(self.trigger_state)

	def knob(self, event):
		self.trigger_state = 3
		self.serial_port.write('k')
		self.is_ready = 1
		self.knob_step_on = 1
		print(self.trigger_state)

	def get_ready(self):
		self.serial_port.write("g")

	def get_angle(self, val):
		#print(val)
		if self.trigger_state == 2: #spring
			if val >=2.0 and val < 20.0 and self.is_ready == 0:
				self.serial_port.write("g")
				self.is_ready = 1


			if val >= 20.0 and val <= 200.0:
				if self.spring_step == 0:
					self.spring_step = 1

				#if val < 2.0:
				#	self.val = 2.0

				val_interval = val - self.val

				if val_interval >=4.0:
					step_interval = (int)(val_interval / 4.0)
					print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("m")  #step down
						self.step_count += 1

					self.val = self.val + step_interval * 4.0

					#print(self.val)

			else:
				if self.spring_step == 1:
					self.spring_step = 0
					print(self.step_count)
					#for x in range(0, self.step_count):
					self.serial_port.write("r")
					self.is_ready = 0
						#time.sleep(0.015)

					self.step_count = 0

				self.val = 20.0#val
	

		elif self.trigger_state == 1: #tick
			if val >=2.0 and val < 15.0 and self.is_ready == 0:
				self.serial_port.write("g")
				self.is_ready = 1


			if val >= 15.0 and val <= 45.0:
				if self.spring_step == 0:
					self.spring_step = 1

				#if val < 2.0:
				#	self.val = 2.0

				val_interval = val - self.val

				if val_interval >=0.75:
					step_interval = (int)(val_interval / 0.75)
					print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("m")  #step down
						self.step_count += 1

					self.val = self.val + step_interval * 0.75

					#print(self.val)

			elif (val > 46 and val < 360) or (val < 14.7 and val > 0):
				if self.spring_step == 1:
					self.spring_step = 0
					print(self.step_count)
					#for x in range(0, self.step_count):
					self.serial_port.write("y")
					self.is_ready = 0
						#time.sleep(0.015)

					self.step_count = 0

				self.val = 15.0#val
			

		





		elif self.trigger_state == 3: #knob
			if self.knob_step_on == 





