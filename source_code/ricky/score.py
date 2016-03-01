import pandas as pd
def score(pre,label):
        print 'score...'
        rank = pd.DataFrame()
	rank["pre"] = pre
	rank["label"] = label
	Tp = Fp = Tn = Fn = 0
	Tp1 = []
	Fp1 = []
	Tn1 = []
	Fn1 = []
	Recal = []
	Precision = []
	for index, row in rank.iterrows():
		Tp = Fp = Tn = Fn = 0
		for index, row1 in rank.iterrows():
			if row1["pre"]>=row["pre"] and row1["label"] ==1:
				Tp = Tp+1
			elif row1["pre"]>=row["pre"] and row1["label"] ==0:
				Fp = Fp+1
			elif row1["pre"]<row["pre"] and row1["label"] ==1:
				Fn = Fn+1
			elif row1["pre"]<row["pre"] and row1["label"] ==0:
				Tn = Tn+1
		Tp1.append(Tp)
		Fp1.append(Fp)
		Fn1.append(Fn)
		Tn1.append(Tn)
		Recal.append(float(Tp)/(Tp+Fn))
		Precision.append(float(Tp)/(Tp+Fp))
	rank["Tp"] = Tp1
	rank["Fp"] = Fp1
	rank["Fn"] = Fn1
	rank["Tn"] = Tn1
	rank["Recal"] = Recal
	rank["Precision"] = Precision
	rank = rank.sort(['Recal'],ascending=True)
	temp1 = rank["Recal"][1:]
	temp2 = rank["Recal"][:len(Recal)-1]
	temp3 = (temp1.values-temp2.values)*rank["Precision"][1:]
	return temp3.sum()
