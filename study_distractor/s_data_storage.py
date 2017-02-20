import csv
import numpy as np
from threading import Thread
import time

class data_sample(object):

	def __init__(self, timestamp, event, angle, force, profile):
		self.timestamp = timestamp
		self.event = event
		self.angle = angle
		self.force = force
		self.profile = profile

	def tocvs(self):
		return {'timestamp': self.timestamp, 'event': self.event, 'angle': self.angle, 'force': self.force, 'profile': self.profile}


class data_storage(object):
	
	def __init__(self):
		self.samples = []

	def add_sample(self, _timestamp, _event, _angle, _force, _profile):
		datasample = data_sample(_timestamp, _event, _angle, _force, _profile)
		self.samples.append(datasample)

	def save(self):
		with open('data.csv', 'w') as csvfile:
		    fieldnames = ['timestamp', 'event', 'angle', 'force', 'profile']
		    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		    writer.writeheader()

		    for data in self.samples:
		    	writer.writerow(data.tocvs())


if __name__ == "__main__":
	data_storage = data_storage()
	data_storage.add_sample(1,2,3,4,5)
	data_storage.add_sample(10,22,33,43,53)

	data_storage.save()