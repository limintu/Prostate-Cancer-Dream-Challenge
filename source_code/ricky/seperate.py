#import pandas as pd
def out1(data):
	data1 =  data[data['RPT'].str.contains("ASC-")]
	return data1

def out2(data):
	data1 =  data[data['RPT'].str.contains("CELG-")]
	return data1
	
def out3(data):
	data1 =  data[data['RPT'].str.contains("VEN-")]
	return data1