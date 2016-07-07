import csv
import time

FILE_EXTENSION = '.csv'

def current_milli_time():
	int(round(time.time() * 1000))

def create_new_file():
	file_name = str(current_milli_time()) + FILE_EXTENSION
	with open(file_name + '', 'w', newline='') as csvfile:
		csv.writer(csvfile)
	return file_name

def write(file_name, result, hold_id):
	with open(file_name, 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow([hold_id, current_milli_time()] + result)