import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import numpy as np
import csv
import argparse

#put all data together
def create_all_raw():
	data_dir = "cat_user_study"
	all_date = []

	for subdir, dirs, files in os.walk(data_dir):
		for file in files:
			if 'data_' in file:
				print(os.path.join(subdir, file))
				single_file_data = open(os.path.join(subdir, file))
				user_index = subdir
				user_index = user_index[20:]
				csv_f = csv.reader(single_file_data)
				for row in csv_f:
					if row[0] != 'timestamp':
						row.insert(0, user_index)
						all_date.append(row)

	with open('all_data_step_1.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['USER','timestamp','angle','force','event','block','trial','profile','count','duration','profile_result','distractor','distractor_result','CORRECTIONS','PTIMES'])
		for data in all_date:
		    writer.writerow(data)



#detect key events
def create_new_data():
	new_data = []
	temp_data = []
	temp_event = []
	data_is_good = False
	is_first_2 = False  #index of the first event 2 occurance
	last_3_index = 0  #index of last event 3 occurance
	end_temp = 0

	first_try = True

	raw_data = open('all_data_step_1.csv')
	csv_f = csv.reader(raw_data)
	for row in csv_f:
		if row[4] == '1':
			data_is_good = True
			is_first_2 = True
			del temp_data[:]
			del temp_event[:]

		elif row[4] == '7':
			if data_is_good == True:
				data_is_good = False
				end_temp = float(row[1])

				
				#if ''.join(temp_event).rfind('41') != -1:
				#	if first_try:
				#		print(temp_event)
				#		print(''.join(temp_event).rfind('3'))
				#		first_try = False

				#locate the last 3
				#last_3_index = ''.join(temp_event).rfind('3')
				try:
					last_3_index = len(temp_event) - 1 - temp_event[::-1].index('3')
				except ValueError:
					print("no 3 error at user: %s, block: %s, trial: %s, profile: %s" % (row[0], row[5], row[6], row[7]))
					continue

				#if last_3_index == -1:
				#	#there is no 3
				#	print("no 3 error at user: %s, block: %s, trial: %s, profile: %s" % (row[0], row[5], row[6], row[7]))
				#	continue

				itri = 0

				for data_item in temp_data:

					if end_temp >= float(data_item[1]):
						if data_item[4] == '3' and itri == last_3_index:  
							new_data.append(data_item)
						elif data_item[4] != '3':
							new_data.append(data_item)

					else:
						print("7 time error")
						
					itri+=1

				new_data.append(row) #add event 7

		if data_is_good == True:
			if row[4] == '1' or row[4] == '3' or row[4] == '4' or row[4] == '41' or row[4] == '42' or row[4] == '5' or row[4] == '6':
				temp_data.append(row)
				temp_event.append(row[4])

			if row[4] == '2' and (row[7] == '1' or row[7] == '2') and is_first_2 == True:
				temp_data.append(row)
				temp_event.append(row[4])
				is_first_2 = False


	with open('all_data_step_2.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['USER','timestamp','angle','force','event','block','trial','profile','count','duration',
			'profile_result','distractor','distractor_result','CORRECTIONS','COLOR_CORRECTION','RTIMES','PTIMES','PRESPONSE_TIME' ])
		for data in new_data:
		    writer.writerow(data)


#calculate accuracy, response time, adjusted response time and others
def show_data_result():
	data_result = []

	data_no_result = open('all_data_step_2.csv')
	csv_f = csv.reader(data_no_result)

	response_time = 0
	adjusted_response_time = 0  #response_time - key_press_time
	key_press_time = 0  #from the last 3 to 6
	leave_motion_time = 0 # time of 3
	profile_start_stamp = 0
	profile_end_stamp = 0
	is_profiling = False

	profile_times = 0

	color_correction = ''
	profile_correction = ''

	row_count = 0
	for row in csv_f:
		row_count += 1
		if row[7] == '1' or row[7] == '2':
			if row[4] == '1':
				profile_times = 0
				response_time = 0
				profile_start_stamp = 0
				profile_end_stamp = 0
				is_profiling = True
			elif row[4] == '2':
				profile_start_stamp = float(row[1])
			elif row[4] == '3':
				leave_motion_time = float(row[1])  #this should be the last 3
			elif row[4] == '5':
				profile_times += 1

				if is_profiling == True:
					profile_end_stamp = float(row[1])
					if profile_end_stamp - profile_start_stamp > 0.0:
						response_time += (profile_end_stamp - profile_start_stamp)
					else:
						print(row_count)
						print("2-5 response time error sequencing")

					is_profiling = False

			elif row[4] == '6':
				if is_profiling == True:
					profile_end_stamp = float(row[1])
					if profile_end_stamp - profile_start_stamp > 0.0:
						response_time += (profile_end_stamp - profile_start_stamp)
					else:
						#print("6 %s"%profile_end_stamp)
						print(row_count)
						print("2-6 error sequencing")

					is_profiling = False
				else:
					if float(row[1]) - profile_end_stamp > 0:
						response_time+=(float(row[1]) - profile_end_stamp)
					else:
						print(row_count)
						print("5-6 error sequencing")

				#calculate the key_press_time
				if float(row[1]) - leave_motion_time > 0:
					key_press_time = float(row[1]) - leave_motion_time
					adjusted_response_time = response_time - key_press_time
					if adjusted_response_time < 0:
						#print(row_count)
						#print("adjusted time error")
						print("3 error at user: %s, block: %s, trial: %s, profile: %s" % (row[0], row[5], row[6], row[7]))
						continue
				else:
					print(row_count)
					print("3-6 serror")


			elif row[4] == '7':
				#profile correct
				if row[7] == row[10]:
					profile_correction = '1'
				else:
					profile_correction = '0'

				row.append(profile_correction)

				#color correct, only valid on block 2 and 4 
				if row[5] == '2' or row[5] == '4': 
					if row[11] == row[12]:
						color_correction = '1'
					else:
						color_correction = '0'
				else:
					color_correction = ''

				row.append(color_correction)

				#profile times
				if profile_times == 0:
					profile_times = 1
				row.append(profile_times)

				#response time
				row.append(response_time)

				#adjusted response time
				row.append(adjusted_response_time)

				if response_time > 1000:
					#print(row_count)
					print("no 2 error at user: %s, block: %s, trial: %s, profile: %s" % (row[0], row[5], row[6], row[7]))
				else:
					data_result.append(row)

		else:
			if row[4] == '1':
				profile_times = 0
				response_time = 0
				profile_start_stamp = 0
				profile_end_stamp = 0
				is_profiling = False

			elif row[4] == '3':
				leave_motion_time = float(row[1])  #this should be the last 3

			elif row[4] == '4' or row[4] == '41':
				profile_start_stamp = float(row[1])
				is_profiling = True

				#if row[4] == '41':
				#	print("41  %s"%profile_start_stamp)
			elif row[4] == '5' or row[4] == '42':
				if is_profiling == True:
					profile_end_stamp = float(row[1])

					if profile_end_stamp - profile_start_stamp > 0.0:
						response_time += (profile_end_stamp - profile_start_stamp)
					else:
						print(row_count)
						print("4-5, 41-42 response time error sequencing")

					profile_times += 1
					is_profiling = False
			elif row[4] == '6':
				#response time
				if is_profiling == True:
					profile_end_stamp = float(row[1])
					if profile_end_stamp - profile_start_stamp > 0.0:
						response_time += (profile_end_stamp - profile_start_stamp)
					else:
						#print("6 %s"%profile_end_stamp)
						print(row_count)
						print("4-6 error sequencing")

					is_profiling = False
				else:
					if float(row[1]) - profile_end_stamp > 0:
						response_time+=(float(row[1]) - profile_end_stamp)
					else:
						print(row_count)
						print("5-6 error sequencing")

				#calculate the key_press_time
				if float(row[1]) - leave_motion_time > 0:
					key_press_time = float(row[1]) - leave_motion_time
					adjusted_response_time = response_time - key_press_time
					if adjusted_response_time < 0:
						#print(row_count)
						#print("adjusted time error")
						print("3 error at user: %s, block: %s, trial: %s, profile: %s" % (row[0], row[5], row[6], row[7]))
						continue
				else:
					print(row_count)
					print("3-6 serror")


			elif row[4] == '7':
				#profile correct
				if row[7] == row[10]:
					profile_correction = '1'
				else:
					profile_correction = '0'
				
				row.append(profile_correction)

				#color correct, only valid on block 2 and 4 
				if row[5] == '2' or row[5] == '4': 
					if row[11] == row[12]:
						color_correction = '1'
					else:
						color_correction = '0'
				else:
					color_correction = ''

				row.append(color_correction)

				#profile times
				if profile_times == 0:
					profile_times = 1
				row.append(profile_times)

				#response time
				row.append(response_time)

				#adjusted response time
				row.append(adjusted_response_time)

				if response_time > 1000:
					#print(row_count)
					print("no 4 error at user: %s, block: %s, trial: %s, profile: %s" % (row[0], row[5], row[6], row[7]))
				else:
					data_result.append(row)

	with open('all_data_step_3.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['USER','timestamp','angle','force','event','block','trial','profile','count','DURATION',
			'profile_result','distractor','distractor_result','PROFILE_CORRECTIONS','COLOR_CORRECTION','PROFILE_TIMES','PRESPONSE_TIME','ADJUSTED_RESPONSE_TIME'])
		for data in data_result:
		    writer.writerow(data)

#prepare the data for statistic analysis
#user / motion, visual, profile / accuracy, response time, new response time / 
def show_condition_data_accuracy_and_time():
	accuracy_data = []
	temp_data = []
	new_row = []
	condition_trials = [0, 0, 0, 0, 0, 0]  #should be 6 * 9 for each condition
	
	#profile correction
	condition_corrects = [0, 0, 0, 0, 0, 0]  #should be 6 items
	
	#profile response time
	condition_retime = [0, 0, 0, 0, 0, 0]   #should be 6 items

	#adjusted profile response time
	condition_adjusted_retime = [0, 0, 0, 0, 0, 0]

	#profile times
	condition_ptimes = [0, 0, 0, 0, 0, 0] 

	#rotation times
	condition_rtimes = [0, 0, 0, 0, 0, 0]

	#duration
	condition_duration = [0, 0, 0, 0, 0, 0]

	#color accuracy
	condition_color = [0, 0, 0, 0, 0, 0]

	last_row = []

	raw_data = open('all_data_step_3.csv')
	csv_f = csv.reader(raw_data)
	for orow in csv_f:
		temp_data.append(orow)

	temp_data.append(temp_data[1])  #to get the orginal last row

	for row in temp_data:
		if len(last_row) != 0:
			if row[5] == last_row[5] and row[0] == last_row[0]: #user and block is the same
				profile_index = int(row[7]) - 1
				condition_trials[profile_index] += 1
				if row[13] == '1':
					condition_corrects[profile_index] += 1
				condition_retime[profile_index] += float(row[16])
				condition_adjusted_retime[profile_index] += float(row[17])

				condition_ptimes[profile_index] += int(row[15])
				condition_rtimes[profile_index] += int(row[8])
				condition_duration[profile_index] += float(row[9])
				if (last_row[5] == '2' or last_row[5] == '4') and row[14] == '1': 
					condition_color[profile_index] += 1
			else:
				for itrp in range(6):
					new_row = []
					#record the piece
					new_row.append(last_row[0])
					#motion
					if last_row[5] == '1' or last_row[5] == '2':
						new_row.append('1')
					elif last_row[5] == '3' or last_row[5] == '4':
						new_row.append('2')

					#visual
					if last_row[5] == '1' or last_row[5] == '3':
						new_row.append('1')
					elif last_row[5] == '2' or last_row[5] == '4':  #with color
						new_row.append('2')

					new_row.append('%s'%(itrp+1))

					if condition_trials[itrp] == 9:  #has to be 9
						new_row.append('%s'%(1.0 * condition_corrects[itrp] / 9))
						new_row.append('%s'%(1.0 * condition_retime[itrp] / 9))
						new_row.append('%s'%(1.0 * condition_adjusted_retime[itrp] / 9))

						new_row.append('%s'%(1.0 * condition_ptimes[itrp] / 9))
						new_row.append('%s'%(1.0 * condition_rtimes[itrp] / 9))
						new_row.append('%s'%(1.0 * condition_duration[itrp] / 9))
						if last_row[5] == '2' or last_row[5] == '4':
							new_row.append('%s'%(1.0 * condition_color[itrp] / 9))
						#print(new_row)


						accuracy_data.append(new_row)
					else:
						print("error: user %s, profile %s" % (new_row[0], (itrp + 1)))

				#reset values
				profile_index = int(row[7]) - 1
				condition_trials = [0, 0, 0, 0, 0, 0]  #should be 6 * 9 for each condition
				condition_corrects = [0, 0, 0, 0, 0, 0]  #should be 6 items
				condition_retime = [0, 0, 0, 0, 0, 0]   #should be 6 items
				condition_adjusted_retime = [0, 0, 0, 0, 0, 0]
				condition_ptimes = [0, 0, 0, 0, 0, 0] 
				condition_rtimes = [0, 0, 0, 0, 0, 0]
				condition_duration = [0, 0, 0, 0, 0, 0]
				condition_color = [0, 0, 0, 0, 0, 0]

				condition_trials[profile_index] += 1
				if row[13] == '1':
					condition_corrects[profile_index] += 1
				condition_retime[profile_index] += float(row[16])
				condition_adjusted_retime[profile_index] += float(row[17])
				condition_ptimes[profile_index] += int(row[15])
				condition_rtimes[profile_index] += int(row[8])
				condition_duration[profile_index] += float(row[9])
				if (last_row[5] == '2' or last_row[5] == '4') and row[14] == '1': 
					condition_color[profile_index] += 1

		last_row = row


	#print(accuracy_data)

	with open('all_data_step_4.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['USER','MOTION', 'VISUAL', 'PROFILE', 'PACCURACY', 'RTIME', 'ARTIME', 'PTIMES', 'RTIMES', 'DURATION', 'CACCURACY'])
		for data in accuracy_data:
		    writer.writerow(data)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='data_dealer --step string')
	parser.add_argument('--step', action='store', dest='step', default='0' ,help='step to execute')

	args = parser.parse_args()

	if args.step == '0':
		print("expecting > 0")
	elif args.step == '1':
		create_all_raw()
	elif args.step == '2':
		create_new_data()
	elif args.step == '3':
		show_data_result()
	elif args.step == '4':
		show_condition_data_accuracy_and_time()
