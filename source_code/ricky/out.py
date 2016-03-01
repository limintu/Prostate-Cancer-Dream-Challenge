import pandas as pd
import seperate
import select
a=pd.read_csv("CoreTable_training.csv")
#data1 =  seperate.out1(a)
#data1 = pd.concat(a['STUDYID'],a['RPT'])
c = ["DOMAIN","RPT","ENDTRS_C"]
data1 = select.select(a,c)
print data1


