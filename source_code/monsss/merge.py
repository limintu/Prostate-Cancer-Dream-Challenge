import pandas as pd
def merge(label,data):
        data=pd.DataFrame(data)
	data.columns = label
	return data
