def tolist(list,label,data):
	list[label] = data
	return list
def ensemble(list,method):
	if method == "average":
		return list.mean(axis=1)
	elif method == "minimum":
		return list.min(axis=1)
	elif method == "maximum":
		return list.max(axis=1)
	elif method == "median":
		return list.median(axis=1)
	elif method == "trimmed mean":
		sum = list.sum(axis=1)
		max = list.max(axis=1)
		min = list.min(axis=1)
		final = (sum-max-min)/(len(list.columns)-2)
		return final
	elif method == "product":
		return list.product(axis=1)