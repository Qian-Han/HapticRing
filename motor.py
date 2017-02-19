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

		self.knob_step_on = 0
		# self.knob_lift_ang = [35.0, 95.0, 155.0, 215.0, 275.0, 335.0]
		# self.knob_down_ang = [55.0, 115.0, 175.0, 235.0, 295.0, 355.0]
		self.knob_lift_ang = [45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0, 0.0]
		self.knob_down_ang = [65.0, 110.0, 155.0, 200.0, 245.0, 290.0, 335.0, 20.0]
		self.knob_ind = 0


		self.tuk_step_on = 0
		# self.tuk_lift_ang = [35.0, 95.0, 155.0, 215.0, 275.0, 335.0]
		# self.tuk_down_ang = [55.0, 115.0, 175.0, 235.0, 295.0, 355.0]
		self.tuk_lift_ang = [45.0, 105.0, 165.0, 225.0, 285.0, 345.0]
		self.tuk_down_ang = [55.0, 115.0, 175.0, 235.0, 295.0, 355.0]
		self.tuk_ind = 0

		self.wall_step_on = 0
		self.wall_ang = [270.0, 90.0]



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
		self.knob_ind = 0
		print(self.trigger_state)

	def tuk(self, event):
		self.trigger_state = 4
		self.serial_port.write('l')
		self.is_ready = 1
		self.tuk_step_on = 1
		self.tuk_ind = 0
		print(self.trigger_state)



	def wall(self, event):
		self.trigger_state = 5
		self.serial_port.write("g")	
		self.wall_step = 0
		print(self.trigger_state)


	def noforce(self, event):
		self.trigger_state = 6
		self.serial_port.write("c")	
		self.serial_port.write("e")	
		print(self.trigger_state)


	def force(self, event):		
		self.trigger_state = 7
		for i in range(0,3):
			self.serial_port.write("c")	
		self.serial_port.write("z")
		self.serial_port.write("z")
		print(self.trigger_state)



	def stop(self, event):
		self.trigger_state = 8
		for i in range(0,8):
			self.serial_port.write("c")	
		print(self.trigger_state)


	def antispring(self, event):
		self.trigger_state = 9
		self.serial_port.write("c")	
		self.serial_port.write("e")		
		self.is_ready = 1
		self.step_count = 0
		self.antispring_step = 0
		print(self.trigger_state)




	def get_ready(self):
		self.serial_port.write("g")

	def get_angle(self, val):
		#print(val)
		if self.trigger_state == 2: #spring
			if val >=2.0 and val < 20.0 and self.is_ready == 0:
				self.serial_port.write("g")
				self.is_ready = 1


			if val >= 20.0 and val <= 300.0:
				if self.spring_step == 0:
					self.spring_step = 1

				#if val < 2.0:
				#	self.val = 2.0

				val_interval = val - self.val

				if val_interval >=4.0:
					step_interval = (int)(val_interval / 4.0)
					#print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("m")  #step down
						self.step_count += 1

					self.val = self.val + step_interval * 4.0

					#print(self.val)

			else:
				if self.spring_step == 1:
					self.spring_step = 0
					#print(self.step_count)
					#for x in range(0, self.step_count):
					self.serial_port.write("r")
					#self.serial_port.write("r")
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
					#print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("m")  #step down
						self.step_count += 1

					self.val = self.val + step_interval * 0.75

					#print(self.val)

			elif (val > 46 and val < 360) or (val < 14.7 and val > 0):
				if self.spring_step == 1:
					self.spring_step = 0
					#print(self.step_count)
					#for x in range(0, self.step_count):
					self.serial_port.write("y")
					self.is_ready = 0
						#time.sleep(0.015)

					self.step_count = 0

				self.val = 15.0#val




		elif self.trigger_state == 3: #knob
			if self.knob_step_on == 1 and val > self.knob_lift_ang[self.knob_ind] and val < self.knob_lift_ang[self.knob_ind] + 2.0:
				self.serial_port.write("n") #lift up
				self.knob_step_on = 0
			elif self.knob_step_on == 0 and val > self.knob_down_ang[self.knob_ind] and self.knob_down_ang[self.knob_ind] + 2.0:
				self.serial_port.write("b") #put down
				self.knob_step_on = 1
				self.knob_ind += 1
				if self.knob_ind == len(self.knob_lift_ang):
					self.knob_ind = 0 



		elif self.trigger_state == 4: #tuk
			if self.tuk_step_on == 1 and val > self.tuk_lift_ang[self.tuk_ind] and val < self.tuk_lift_ang[self.tuk_ind] + 2.0:
				self.serial_port.write(",") #lift down
				self.tuk_step_on = 0
			elif self.tuk_step_on == 0 and val > self.tuk_down_ang[self.tuk_ind] and self.tuk_down_ang[self.tuk_ind] + 2.0:
				self.serial_port.write("v") #put up
				self.tuk_step_on = 1
				self.tuk_ind += 1
				if self.tuk_ind == len(self.tuk_lift_ang):
					self.tuk_ind = 0 

		

		elif self.trigger_state == 5: #wall
			# if (val >= self.wall_ang[1] and val <= self.wall_ang[1] + 2) or (val >= self.wall_ang[0] - 2 and val <= self.wall_ang[0])
			if self.wall_step_on == 0 and val > self.wall_ang[1] and val <= self.wall_ang[1] + 10:
				self.serial_port.write(".") #lift down
				self.wall_step_on = 1
			elif self.wall_step_on == 0 and val >= self.wall_ang[0] - 10  and val <= self.wall_ang[0]:
				self.serial_port.write(".") #lift down
				self.wall_step_on = 1



			elif self.wall_step_on == 1 and val < self.wall_ang[1] and val >= self.wall_ang[1] - 10:
				self.serial_port.write("/") #rise up
				self.wall_step_on = 0

			elif self.wall_step_on == 1 and val > self.wall_ang[0] and val <= self.wall_ang[0] + 10:
				self.serial_port.write("/") #rise up
				self.wall_step_on = 0





		elif self.trigger_state == 9: #antispring
			if val >=2.0 and val < 20.0 and self.is_ready == 0:
				for x in range(0, 2):
					self.serial_port.write("g")
				# self.serial_port.write("c")
				self.serial_port.write("z")
				self.is_ready = 1


			if val >= 20.0 and val <= 300.0:
				if self.antispring_step == 0:
					self.antispring_step = 1

				#if val < 2.0:
				#	self.val = 2.0

				val_interval = val - self.val

				if val_interval >=4.0:
					step_interval = (int)(val_interval / 4.0)
					#print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("p")  #step on
						self.step_count += 1

					self.val = self.val + step_interval * 4.0

					#print(self.val)

			else:
				if self.antispring_step == 1:
					self.antispring_step = 0
					#print(self.step_count)
					#for x in range(0, self.step_count):
					for x in range(0, 1):
						self.serial_port.write("e")
					
					#self.serial_port.write("r")
					self.is_ready = 0
						#time.sleep(0.015)

					self.step_count = 0

				self.val = 20.0#val

