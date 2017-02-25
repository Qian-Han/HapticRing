import serial
import numpy as np
from threading import Thread
import time

class motor(Thread):
	
		

	def __init__(self):
		Thread.__init__(self)

		self.serial_port = serial.Serial(port='/dev/tty.usbmodem14211', baudrate=115200)

		self.trigger_state = 0
		self.target_state = 0
		self.val = 0
		self.max_per_rotation = 0
		self.ready_to_stop_motor = 90
		self.ready_to_stop_sensor = 180
		self.tick_step = 0
		self.spring_step = 0
		self.is_ready = 0
		self.step_count = 0
		self.motor_moving = 0

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

		self.pthreshold_up = 290
		self.pthreshold_down = 260

		self.action_start = 20  #5 degree
		self.action_end = 300  #300 degree

		self.time_tag = 0


	def close(self):
		self.serial_port.close()

	def write_serial(self, val_string):
		self.serial_port.write(val_string)

	# def tune_up(self, event):
	# 	self.serial_port.write("q")

	# def tune_down(self, event):
	# 	self.serial_port.write("z")

	def reset(self, target):
		self.trigger_state = 10  #to reset
		self.target_state = target
		self.is_ready = 0
		
	def set_profile(self, prof):
		if prof == 1:  #no force
			self.noforce(1)
		elif prof == 2: #force
			self.force(1)
		elif prof == 3:
			self.stop(1)
		elif prof == 4:
			self.spring(1)
		elif prof == 5:
			self.antispring(1)
		elif prof == 6:
			self.tick_bump(1)

	def noforce(self, event):
		self.trigger_state = 10
		self.target_state = 1
		self.is_ready = 0
		self.spring_step = 0
		#self.serial_port.write("c")	
		#self.serial_port.write("e")	
		#print(self.trigger_state)


	def force(self, event):		
		self.trigger_state = 10
		self.target_state = 2
		self.is_ready = 0
		self.spring_step = 0

		#for i in range(0,5):
		#	self.serial_port.write("c")	
		#print(self.trigger_state)

	def stop(self, event):
		self.trigger_state = 10
		self.target_state = 3
		self.is_ready = 0
		self.spring_step = 0



	def spring(self, event):
		self.trigger_state = 10
		self.target_state = 4


		#self.is_ready = 1
		#self.step_count = 0
		self.spring_step = 0
		#print(self.trigger_state)

	def antispring(self, event):
		self.trigger_state = 10
		self.target_state = 5		
		self.is_ready = 0
		self.spring_step = 0
		#self.step_count = 0
		#self.antispring_step = 0
		#print(self.trigger_state)

	def tick_bump(self, event):
		self.trigger_state = 10
		self.target_state = 6
		self.spring_step = 0
		#self.is_ready = 0
		#self.tick_step = 0
		#self.step_count = 0
		#print(self.trigger_state)


	def tick_fast(self, event):
		self.trigger_state = 7
		for i in range(0,3):
			self.serial_port.write("c")	
		self.is_ready = 1
		self.tick_step = 0
		self.step_count = 0
		print(self.trigger_state)


	# def knob(self, event):
	# 	self.trigger_state = 3
	# 	self.serial_port.write('k')
	# 	self.is_ready = 1
	# 	self.knob_step_on = 1
	# 	self.knob_ind = 0
	# 	print(self.trigger_state)

	# def tuk(self, event):
	# 	self.trigger_state = 4
	# 	self.serial_port.write('l')
	# 	self.is_ready = 1
	# 	self.tuk_step_on = 1
	# 	self.tuk_ind = 0
	# 	print(self.trigger_state)



	# def wall(self, event):
	# 	self.trigger_state = 5
	# 	self.serial_port.write("g")	
	# 	self.wall_step = 0
	# 	print(self.trigger_state)





	def get_angle(self, val, pval):  #pval for proximtiy value
		#print(val)
		#back to the reset position
		if self.trigger_state == 10:
			if pval > self.pthreshold_up and self.motor_moving == 0:
				
				self.serial_port.write(".")   #moving down
				self.motor_moving = 1

			elif pval < self.pthreshold_down and self.motor_moving == 0:
				self.serial_port.write("/")  #moving up
				self.motor_moving = 2

			
			elif (self.motor_moving == 1 and pval < self.pthreshold_up) or (self.motor_moving == 2 and pval > self.pthreshold_down):
				self.trigger_state = self.target_state
				self.target_state = 0
				self.serial_port.write("s")
				print("stop called")
				self.motor_moving = 0

			elif pval > self.pthreshold_down and pval < self.pthreshold_up:
				self.trigger_state = self.target_state
				self.target_state = 0
				self.serial_port.write("s")
				print("stop called")
				self.motor_moving = 0



		#if self.trigger_state == 1: #noforce

			"""

			if val > 5.0 and val < 80.0:
				if self.spring_step == 0:
					self.spring_step = 1

				self.max_per_rotation = val
					

				val_interval = val - self.val

				if val_interval >=20.0:
					step_interval = (int)(val_interval / 20.0)
					#print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("p")  #step up
						self.step_count += 1

					self.val = self.val + step_interval * 20.0

					#print(self.val)

			elif val >= 0 and val < 5:
				if self.spring_step == 1:
					self.spring_step = 0
					print(self.step_count)
					#for x in range(0, self.step_count):
					
					if self.max_per_rotation > 70:
						self.serial_port.write("c")
						# time.sleep(0.5)
						self.serial_port.write("e")

					else:
						for x in range(0, self.step_count):
							self.serial_port.write("m")

					self.max_per_rotation = 0
					self.step_count = 0

				self.val = 5.0#val


			"""



		elif self.trigger_state == 2: #force

			if self.is_ready == 0:
				#for i in range(0,1):
				self.serial_port.write("c")
				self.serial_port.write("x")
				self.serial_port.write("x")
				self.serial_port.write("z")
				self.serial_port.write("z")	
				self.is_ready = 1

			else:
				if val > self.action_start and val < self.action_end:
					if self.spring_step == 0:
						self.spring_step = 1

				elif val >= 0 and val < 2:
					if self.spring_step == 1:
						self.spring_step = 0
						
						self.reset(2)




		if self.trigger_state == 3: #stop

			if val > (self.action_end - 3.0) and val < self.action_end:
				if self.spring_step == 0:
					self.spring_step = 1

					for i in range(0,4):
						self.serial_port.write("c")

					self.time_tag = time.time()	
					
			elif val >= 0 and val < 40:
				if self.spring_step == 1:
					
	
					#hold for 2 seconds
					if time.time() - self.time_tag > 2:
						self.reset(3)
						self.spring_step = 0




		if self.trigger_state == 4: #spring

			if val > self.action_start and val < self.action_end:
				if self.spring_step == 0:
					self.spring_step = 1

				#self.max_per_rotation = val
					

				val_interval = val - self.val

				if val_interval >=4.0:
					step_interval = (int)(val_interval / 4.0)
					print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("m")  #step down
						#self.step_count += 1

					self.val = self.val + step_interval * 4.0

					#print(self.val)

			elif val >= 0 and val < 5:
				if self.spring_step == 1:
					self.spring_step = 0
					self.reset(4)

				self.val = self.action_start - 2

			






		if self.trigger_state == 5: #antipring
			if self.is_ready == 0:
				#for i in range(0,1):
				self.serial_port.write("c")
				self.serial_port.write("x")
				self.serial_port.write("x")
				self.serial_port.write("x")
				self.serial_port.write("z")	
				self.is_ready = 1

			else:

				if val > self.action_start and val < self.action_end:
					if self.spring_step == 0:
						self.spring_step = 1

					#self.max_per_rotation = val
						

					val_interval = val - self.val

					if val_interval >=5.0:
						step_interval = (int)(val_interval / 5.0)
						print(step_interval)
						for x in range(0, step_interval):
							self.serial_port.write("p")  #step down
							#self.step_count += 1

						self.val = self.val + step_interval * 5.0

						#print(self.val)

				elif val >= 0 and val < 5:
					if self.spring_step == 1:
						self.spring_step = 0
						self.reset(5)

					self.val = self.action_start - 2


		"""

			if val > 5.0 and val < 80.0:
				if self.spring_step == 0:
					self.spring_step = 1

				self.max_per_rotation = val
					

				val_interval = val - self.val

				if val_interval >=2.0:
					step_interval = (int)(val_interval / 2.0)
					#print(step_interval)
					for x in range(0, step_interval):
						self.serial_port.write("p")  #step up
						self.step_count += 1

					self.val = self.val + step_interval * 2.0

					#print(self.val)

			elif val >= 0 and val < 5:
				if self.spring_step == 1:
					self.spring_step = 0
					print(self.step_count)
					#for x in range(0, self.step_count):
					
					if self.max_per_rotation > 70:
						self.serial_port.write("-")
						# time.sleep(0.5)
						self.serial_port.write("g")
						# self.serial_port.write("c")
						#self.serial_port.write("r")
					else:
						for x in range(0, self.step_count):
							self.serial_port.write("m")

					self.max_per_rotation = 0
					self.step_count = 0

				self.val = 5.0#val
			"""




		"""

		if self.trigger_state == 6: #bump or Tick
			if val > (self.action_end - 40.0) and val < (self.action_end - 30.0):
				if self.spring_step == 0:
					self.spring_step = 1
					print("going down")
					for i in range(0,4):
						self.serial_port.write("c")

					self.time_tag = time.time()	

			elif val > (self.action_end - 15.0):
				if self.spring_step == 1:
					if time.time() - self.time_tag > 0.5:
						self.spring_step = 2
						print("going up")
						for i in range(0, 4):
							self.serial_port.write("e")

			elif val >= 0 and val < 5:
				if self.spring_step == 2 or self.spring_step == 1:
					print("reset")
					self.spring_step = 0
					self.reset(6)

		"""

		if self.trigger_state == 6:  #bump

			if val > (self.action_end - 3.0) and val < self.action_end:
				if self.spring_step == 0:
					self.spring_step = 1

					for i in range(0,4):
						self.serial_port.write("c")

					self.time_tag = time.time()	
					
			elif val >= 0 and val < 40:
				if self.spring_step == 1:
					
	
					#hold for 2 seconds
					if time.time() - self.time_tag > 0.5:
						self.reset(6)
						self.spring_step = 0


"""
			if val > 38.0 and val < 40.0:
				if self.spring_step == 0:
					self.spring_step = 1

					for i in range(0,3):
						self.serial_port.write("c")
					self.serial_port.write("x")		
					print(self.trigger_state)

			elif val >= 0 and val < 2:
				if self.spring_step == 1:
					self.spring_step = 0
	
					#for x in range(0, self.step_count):

					for i in range(0,2):
						self.serial_port.write("e")
						self.serial_port.write("w")		
"""




		# if self.trigger_state == 7: # Tick: Fast

		# 	if val > 5.0 and val < 80.0:
		# 		if self.spring_step == 0:
		# 			self.spring_step = 1

		# 		self.max_per_rotation = val
					

		# 		val_interval = val - self.val

		# 		if val_interval >=2.0:
		# 			step_interval = (int)(val_interval / 2.0)
		# 			#print(step_interval)
		# 			for x in range(0, step_interval):
		# 				self.serial_port.write("m")  #step down
		# 				self.step_count += 1

		# 			self.val = self.val + step_interval * 2.0

		# 			#print(self.val)

		# 	elif val >= 0 and val < 5:
		# 		if self.spring_step == 1:
		# 			self.spring_step = 0
		# 			print(self.step_count)
		# 			#for x in range(0, self.step_count):
					
		# 			if self.max_per_rotation > 70:
		# 				for i in range(0,3):
		# 					self.serial_port.write("e")
		# 					self.serial_port.write("w")		

		# 				for i in range(0,2):
		# 					self.serial_port.write("c")
		# 					self.serial_port.write("x")		


		# 			else:
		# 				for x in range(0, self.step_count):
		# 					self.serial_port.write("p")

		# 			self.max_per_rotation = 0
		# 			self.step_count = 0

		# 		self.val = 5.0#val



			# elif val >= 0 and val < 5:
			# 	if self.spring_step == 1:
			# 		self.spring_step = 0
	
			# 		#for x in range(0, self.step_count):

			# 		self.serial_port.write("r")
			# 		# time.sleep(0.5)
			# 		self.serial_port.write("g")



		##  spring profile 2

		# if self.trigger_state == 2: #spring
		# 	if val >1.0 and val < 3.0 and self.is_ready == 0:
		# 		self.serial_port.write("|")
		# 		self.is_ready = 1


		# 	if val > 3.0 and val < 60.0:
		# 		if self.spring_step == 0:
		# 			self.spring_step = 1

		# 		#if val < 2.0:
		# 		#	self.val = 2.0

		# 		val_interval = val - self.val

		# 		if val_interval >=2.0:
		# 			step_interval = (int)(val_interval / 2.0)
		# 			#print(step_interval)
		# 			for x in range(0, step_interval):
		# 				self.serial_port.write("m")  #step down
		# 				self.step_count += 1

		# 			self.val = self.val + step_interval * 2.0

		# 			#print(self.val)

		# 	else:
		# 		if self.spring_step == 1:
		# 			self.spring_step = 0
		# 			print(self.step_count)
		# 			#for x in range(0, self.step_count):
		# 			self.serial_port.write("r")
		# 			#self.serial_port.write("r")
		# 			self.is_ready = 0
		# 				#time.sleep(0.015)

		# 			self.step_count = 0

		# 		self.val = 0.0#val



		# if self.trigger_state == 2: #spring
		# 	if val >1.0 and val < 3.0 and self.is_ready == 0:
		# 		self.serial_port.write("|")
		# 		self.is_ready = 1


		# 	if val > 3.0 and val < 60.0:
		# 		if self.spring_step == 0:
		# 			self.spring_step = 1

		# 		#if val < 2.0:
		# 		#	self.val = 2.0

		# 		val_interval = val - self.val

		# 		if val_interval >=2.0:
		# 			step_interval = (int)(val_interval / 2.0)
		# 			#print(step_interval)
		# 			for x in range(0, step_interval):
		# 				self.serial_port.write("m")  #step down
		# 				self.step_count += 1

		# 			self.val = self.val + step_interval * 2.0

		# 			#print(self.val)

		# 	else:
		# 		if self.spring_step == 1:
		# 			self.spring_step = 0
		# 			print(self.step_count)
		# 			#for x in range(0, self.step_count):
		# 			self.serial_port.write("r")
		# 			#self.serial_port.write("r")
		# 			self.is_ready = 0
		# 				#time.sleep(0.015)

		# 			self.step_count = 0

		# 		self.val = 0.0#val
	

		# elif self.trigger_state == 1: #tick
		# 	if val >=2.0 and val < 15.0 and self.is_ready == 0:
		# 		self.serial_port.write("g")
		# 		self.is_ready = 1


		# 	if val >= 15.0 and val <= 45.0:
		# 		if self.spring_step == 0:
		# 			self.spring_step = 1

		# 		#if val < 2.0:
		# 		#	self.val = 2.0

		# 		val_interval = val - self.val

		# 		if val_interval >=0.75:
		# 			step_interval = (int)(val_interval / 0.75)
		# 			#print(step_interval)
		# 			for x in range(0, step_interval):
		# 				self.serial_port.write("m")  #step down
		# 				self.step_count += 1

		# 			self.val = self.val + step_interval * 0.75

		# 			#print(self.val)

		# 	elif (val > 46 and val < 360) or (val < 14.7 and val > 0):
		# 		if self.spring_step == 1:
		# 			self.spring_step = 0
		# 			#print(self.step_count)
		# 			#for x in range(0, self.step_count):
		# 			self.serial_port.write("y")
		# 			self.is_ready = 0
		# 				#time.sleep(0.015)

		# 			self.step_count = 0

		# 		self.val = 15.0#val




		# elif self.trigger_state == 3: #knob
		# 	if self.knob_step_on == 1 and val > self.knob_lift_ang[self.knob_ind] and val < self.knob_lift_ang[self.knob_ind] + 2.0:
		# 		self.serial_port.write("n") #lift up
		# 		self.knob_step_on = 0
		# 	elif self.knob_step_on == 0 and val > self.knob_down_ang[self.knob_ind] and self.knob_down_ang[self.knob_ind] + 2.0:
		# 		self.serial_port.write("b") #put down
		# 		self.knob_step_on = 1
		# 		self.knob_ind += 1
		# 		if self.knob_ind == len(self.knob_lift_ang):
		# 			self.knob_ind = 0 



		# elif self.trigger_state == 4: #tuk
		# 	if self.tuk_step_on == 1 and val > self.tuk_lift_ang[self.tuk_ind] and val < self.tuk_lift_ang[self.tuk_ind] + 2.0:
		# 		self.serial_port.write(",") #lift down
		# 		self.tuk_step_on = 0
		# 	elif self.tuk_step_on == 0 and val > self.tuk_down_ang[self.tuk_ind] and self.tuk_down_ang[self.tuk_ind] + 2.0:
		# 		self.serial_port.write("v") #put up
		# 		self.tuk_step_on = 1
		# 		self.tuk_ind += 1
		# 		if self.tuk_ind == len(self.tuk_lift_ang):
		# 			self.tuk_ind = 0 

		

		# elif self.trigger_state == 5: #wall
		# 	# if (val >= self.wall_ang[1] and val <= self.wall_ang[1] + 2) or (val >= self.wall_ang[0] - 2 and val <= self.wall_ang[0])
		# 	if self.wall_step_on == 0 and val > self.wall_ang[1] and val <= self.wall_ang[1] + 10:
		# 		self.serial_port.write(".") #lift down
		# 		self.wall_step_on = 1
		# 	elif self.wall_step_on == 0 and val >= self.wall_ang[0] - 10  and val <= self.wall_ang[0]:
		# 		self.serial_port.write(".") #lift down
		# 		self.wall_step_on = 1



		# 	elif self.wall_step_on == 1 and val < self.wall_ang[1] and val >= self.wall_ang[1] - 10:
		# 		self.serial_port.write("/") #rise up
		# 		self.wall_step_on = 0

		# 	elif self.wall_step_on == 1 and val > self.wall_ang[0] and val <= self.wall_ang[0] + 10:
		# 		self.serial_port.write("/") #rise up
		# 		self.wall_step_on = 0





		# elif self.trigger_state == 9: #antispring
		# 	if val >=2.0 and val < 20.0 and self.is_ready == 0:
		# 		for x in range(0, 2):
		# 			self.serial_port.write("g")
		# 		# self.serial_port.write("c")
		# 		self.serial_port.write("z")
		# 		self.is_ready = 1


		# 	if val >= 20.0 and val <= 300.0:
		# 		if self.antispring_step == 0:
		# 			self.antispring_step = 1

		# 		#if val < 2.0:
		# 		#	self.val = 2.0

		# 		val_interval = val - self.val

		# 		if val_interval >=4.0:
		# 			step_interval = (int)(val_interval / 4.0)
		# 			#print(step_interval)
		# 			for x in range(0, step_interval):
		# 				self.serial_port.write("p")  #step on
		# 				self.step_count += 1

		# 			self.val = self.val + step_interval * 4.0

		# 			#print(self.val)

		# 	else:
		# 		if self.antispring_step == 1:
		# 			self.antispring_step = 0
		# 			#print(self.step_count)
		# 			#for x in range(0, self.step_count):
		# 			for x in range(0, 1):
		# 				self.serial_port.write("e")
					
		# 			#self.serial_port.write("r")
		# 			self.is_ready = 0
		# 				#time.sleep(0.015)

		# 			self.step_count = 0

		# 		self.val = 20.0#val

