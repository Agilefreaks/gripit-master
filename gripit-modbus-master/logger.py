import csv
import time

class Logger:
	FILE_EXTENSION = '.csv'

	def current_milli_time(self):
		return int(round(time.time() * 1000))

	def create_new_file(self):
		file_name = str(self.current_milli_time()) + Logger.FILE_EXTENSION
		with open(file_name + '', 'w', newline='') as csvfile:
			csv.writer(csvfile)
		return file_name

	def write(self, file_name, result, hold_id):
		with open(file_name, 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow([hold_id, self.current_milli_time()] + result)