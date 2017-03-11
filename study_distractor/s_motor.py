import serial
import numpy as np
from threading import Thread
import time

class motor(Thread):
	
	def __init__(self):
		Thread.__init__(self)

		self.serial_port = serial.Serial(port='/dev/tty.usbmodem14241', baudrate=115200)

		self.trigger_state = 0
		self.target_state = 0
		self.val = 0
		self.max_per_rotation = 0
		self.ready_to_stop_motor = 90
		self.ready_to_stop_sensor = 180
		self.tick_step = 0
		self.profile_step = 0
		self.is_ready = 0
		self.step_count = 0
		self.motor_moving = 0

		self.pthreshold_up = 670
		self.pthreshold_down = 650

		self.pthreshold_low = 520

		self.action_start = 20 #20 degree
		self.action_end =  180  #300 degree

		self.time_tag = time.time()
		self.first_move = True
		self.action_stop = False

	def close(self):
		self.serial_port.close()

	def write_serial(self, val_string):
		self.serial_port.write(val_string)

	def set_action_stop(self, angle):			
		if self.trigger_state == 6 and (self.profile_step == 1 or self.profile_step == 0):
			self.action_stop = True

		if self.trigger_state == 6 and self.profile_step == 1:
			self.val = angle

	def reset(self, target):
		self.trigger_state = 10  #to reset
		self.target_state = target
		self.is_ready = 0

	def noforce(self):
		self.trigger_state = 11
		self.target_state = 1
		self.is_ready = 0
		self.profile_step = 0
		print("1 - noforce")

	def force(self):		
		self.trigger_state = 11
		self.target_state = 2
		self.is_ready = 0
		self.profile_step = 0
		print("2 - force")

	def stop(self):
		self.trigger_state = 11
		self.target_state = 3
		self.is_ready = 0
		self.profile_step = 0
		print("3 - stop")

	def spring(self):
		self.trigger_state = 11
		self.target_state = 4
		self.profile_step = 0
		print("4 - spring")

	def antispring(self):
		self.trigger_state = 11
		self.target_state = 5		
		self.is_ready = 0
		self.profile_step = 0
		print("5 - antispring")

	def tick_bump(self):
		self.trigger_state = 11
		self.target_state = 6
		self.profile_step = 0
		print("6 - bump")

	def set_profile(self, prof):
		if prof == 1:  #no force
			self.noforce()
		elif prof == 2: #force
			self.force()
		elif prof == 3:
			self.stop()
		elif prof == 4:
			self.spring()
		elif prof == 5:
			self.antispring()
		elif prof == 6:
			self.tick_bump()
		elif prof == 0:
			self.reset(0)  #reset to a higher position


	def get_angle(self, val, pval, storage, is_recording):  #pval for proximtiy value

		if self.first_move == True and (time.time() - self.time_tag > 2):
			#move a little bit down
			if pval > 250:
				self.serial_port.write("x")
			self.first_move = False
		else:
			#back to the reset position
			if self.trigger_state == 10:  #reset to a higher position
				if pval > self.pthreshold_up and self.motor_moving == 0:
					
					self.serial_port.write(".")   #moving down
					self.motor_moving = 1

				elif pval < self.pthreshold_down and self.motor_moving == 0:
					self.serial_port.write("/")  #moving up
					self.motor_moving = 2

				elif (self.motor_moving == 1 and pval < self.pthreshold_up) or (self.motor_moving == 2 and pval > self.pthreshold_down):
					if self.target_state == 0:
						self.trigger_state = 0
					else:
						self.trigger_state = 11
					self.serial_port.write("s")
					# print("reset moving up done")
					self.motor_moving = 0

				elif pval > self.pthreshold_down and pval < self.pthreshold_up:
					if self.target_state == 0:
						self.trigger_state = 0
					else:
						self.trigger_state = 11
					self.serial_port.write("s")
					# print(" reset moving up done")
					self.motor_moving = 0

			elif self.trigger_state == 11:   #reset to a lower position, real get ready
				if pval > self.pthreshold_low and self.motor_moving == 0:
					self.serial_port.write(".")   #moving down
					self.motor_moving = 1

				elif pval < self.pthreshold_low:
					self.trigger_state = self.target_state
					# print("reset moving down done")
					if self.trigger_state == 1:
						# print("dong le")
						self.serial_port.write("e")
						# self.serial_port.write("q")
						#self.serial_port.write("q")


					self.target_state = 0
					self.serial_port.write("s")
					self.motor_moving = 0

			elif self.trigger_state == 1:   #no force
				if val>self.action_start and val < self.action_end:
					if self.profile_step == 0:
						# print("set 1")
						self.profile_step = 1
				elif val >=0 and val < 2:
					if self.profile_step == 1:
						self.profile_step =0
						# print("reset 1")
						self.reset(1)


			elif self.trigger_state == 2: #force
				if self.is_ready == 0:
					for i in range(0,2):
						self.serial_port.write("c")
					# self.serial_port.write("x")
					# self.serial_port.write("x")
					# self.serial_port.write("z")
					# self.serial_port.write("z")	
					self.is_ready = 1

				else:
					if val > self.action_start and val < self.action_end:
						if self.profile_step == 0:
							self.profile_step = 1

							if is_recording:
								storage.add_sample(time.time(), val, pval, 4, 0, 0, 0, 0, 0, 0, 0, 0)

					elif val >= 0 and val < 2:
						if self.profile_step == 1:
							self.profile_step = 0
							
							self.reset(2)

			if self.trigger_state == 3: #stop

				if val > (self.action_start + 25) and val < (self.action_start + 30):
					if self.profile_step == 0:
						self.profile_step = 1
						if is_recording:
							storage.add_sample(time.time(), val, pval, 4, 0, 0, 0, 0, 0, 0, 0, 0)

						for i in range(0,5):
							self.serial_port.write("c")
						# self.serial_port.write("z")

						self.time_tag = time.time()	
						
				elif val >= 0 and val < 40:  #this might not be useful
					if self.profile_step == 1:
						#hold for 2 seconds
						if time.time() - self.time_tag > 2:
							self.reset(3)
							self.profile_step = 0
				
			if self.trigger_state == 4: #spring

				if val > self.action_start and val < self.action_end:
					if self.profile_step == 0:
						self.profile_step = 1
						if  1 :
							storage.add_sample(time.time(), val, pval, 4, 0, 0, 0, 0, 0, 0, 0, 0)

					val_interval = val - self.val

					if val_interval >=3.00:
						step_interval = (int)(val_interval / 3.00)
						#print(step_interval)
						for x in range(0, step_interval):
							self.serial_port.write("m")  #step down

						self.val = self.val + step_interval * 3.00

				elif val >= 0 and val < 5:
					if self.profile_step == 1:
						self.profile_step = 0
						self.reset(4)

					self.val = self.action_start - 2

			if self.trigger_state == 5: #antipring
				if self.is_ready == 0:
					#for i in range(0,1):
					self.serial_port.write("c")
					self.serial_port.write("c")
					# self.serial_port.write("x")
					# self.serial_port.write("x")
					# self.serial_port.write("x")
					# self.serial_port.write("z")	
					# self.serial_port.write("z")	
					self.is_ready = 1

				else:

					if val > self.action_start and val < self.action_end:
						if self.profile_step == 0:
							self.profile_step = 1
							if is_recording:
								storage.add_sample(time.time(), val, pval, 4, 0, 0, 0, 0, 0, 0, 0, 0)

						val_interval = val - self.val

						if val_interval >=3.0:
							step_interval = (int)(val_interval / 3.0)
							#print(step_interval)
							for x in range(0, step_interval):
								self.serial_port.write("p")  #step down

							self.val = self.val + step_interval * 3.0

					elif val >= 0 and val < 5:
						if self.profile_step == 1:
							self.profile_step = 0
							self.reset(5)

						self.val = self.action_start - 2

			if self.trigger_state == 6:  #bump
				if val > self.action_start and val < self.action_end: 
					if self.action_stop:
						if self.profile_step == 0: #or self.profile_step == 1 only the first time
							if val - self.val > 5:  #need to test
								self.profile_step = 2
								if is_recording:
									storage.add_sample(time.time(), val, pval, 41, 0, 0, 0, 0, 0, 0, 0, 0)
								#print("going down")
								for i in range(0,3):
									self.serial_port.write("c")
								self.serial_port.write("z")

								self.time_tag = time.time()	

						if self.profile_step == 2:
							if time.time() - self.time_tag > 0.3:

								#print("going up")
								self.profile_step = 1
								if is_recording:
									storage.add_sample(time.time(), val, pval, 42, 0, 0, 0, 0, 0, 0, 0, 0)
								for i in range(0,3):
									self.serial_port.write("e")
								self.serial_port.write("q")

								self.action_stop = False
						
				elif val >= 0 and val < 5:
					if self.profile_step == 1 or self.profile_step == 2:
						self.reset(6)
						self.profile_step = 0

					self.val = self.action_start


