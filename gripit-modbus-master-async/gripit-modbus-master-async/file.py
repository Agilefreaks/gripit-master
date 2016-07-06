import csv
import time

def create(file):
	with open(file, 'w', newline='') as csvfile:
		csv.writer(csvfile)


def write(file, result, hold_id):
	current_milli_time = lambda: int(round(time.time() * 1000))
	with open(file, 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow([hold_id, current_milli_time()] + result)