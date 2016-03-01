from numpy import genfromtxt
def readcsv(path):
	data = genfromtxt(path, dtype=int, delimiter=',', skip_header=1)
	return data
