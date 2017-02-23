import csv
import numpy as np
from threading import Thread
import time

class data_sample(object):

	def __init__(self, timestamp, angle, force,   event,    block, trial, profile,    count, duration, profile_result, distractor, distractor_result):
		self.timestamp = timestamp
		self.angle = angle
		self.force = force #motor position, read from ir proximty

		#beginning
		self.event = event #start/complete trial, start/stop motion
		self.block = block
		self.trial = trial
		self.profile = profile
		

		#end
		self.count = count #how many operation times
		self.duration = duration #how long it takes
		self.profile_result = profile_result
		self.distractor = distractor
		self.distractor_result = distractor_result


	def tocvs(self):
		return {'timestamp': self.timestamp, 'angle': self.angle, 'force': self.force, 
			'event': self.event, 'block': self.block, 'trial': self.trial, 'profile': self.profile, 
			'count': self.count, 'duration': self.duration, 'profile_result': self.profile_result, 'distractor': self.distractor, 'distractor_result': self.distractor_result}


class data_storage(object):
	
	def __init__(self):
		self.samples = []

	def add_sample(self, _timestamp, _angle, _force, _event, _block, _trial, _profile, _count, _duration, _profile_result, _distractor, _distractor_result):
		datasample = data_sample(_timestamp, _angle, _force, _event, _block, _trial, _profile, _count, _duration, _profile_result, _distractor, _distractor_result)
		self.samples.append(datasample)

	def save(self, user, temp):
		with open('data_%s_%s.csv'%(user, temp), 'w') as csvfile:
		    fieldnames = ['timestamp', 'angle', 'force', 'event', 'block', 'trial', 'profile', 'count', 'duration', 'profile_result', 'distractor', 'distractor_result']
		    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		    writer.writeheader()

		    for data in self.samples:
		    	writer.writerow(data.tocvs())

		print("data saved")


"""
if __name__ == "__main__":
	data_storage = data_storage()
	data_storage.add_sample(1,2,3,4,5)
	data_storage.add_sample(10,22,33,43,53)

	data_storage.save()

"""