import csv

def create(file):
	with open(file, 'w', newline='') as csvfile:
		csv.writer(csvfile)

def write(file, result):
	with open(file, 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',',
								quotechar=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(result)