import csv
import time
import os

class Logger:
	PATH='logs/'
	FILE_EXTENSION = '.csv'

	def current_milli_time(self):
		return int(round(time.time() * 1000))

	def create_directory(self):
		if not os.path.exists(Logger.PATH):
			os.makedirs(Logger.PATH)

	def create_new_file(self):
		self.create_directory()
		file_name = str(self.current_milli_time()) + Logger.FILE_EXTENSION
		with open(Logger.PATH + file_name, 'w', newline='') as csvfile:
			csv.writer(csvfile)
		return file_name

	def write(self, file_name, result, hold_id):
		with open(Logger.PATH + file_name, 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow([hold_id, self.current_milli_time()] + result)
