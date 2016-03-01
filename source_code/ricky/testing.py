def test(testdata,rf):
	out = rf.predict(testdata)
	temp = out.argsort()
	rank = temp.argsort()
	return rank