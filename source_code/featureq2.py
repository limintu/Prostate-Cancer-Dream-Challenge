
# coding: utf-8

# In[17]:

import pandas as pd
import Orange

dataoriAll = pd.read_csv("TrainAll.csv")
datatestAll = pd.read_csv("TestAll.csv")

dfAll = pd.DataFrame(dataoriAll)

for column in dataoriAll.columns:
    dfAll.rename(columns={column: 'D#'+column}, inplace=True)

dfAll.rename(columns={"D#DISCONT": 'c#D#DISCONT'}, inplace=True)

dfAll.to_csv("Train_afterAll.csv",index=False)


dataAll = Orange.data.Table("Train_afterAll.csv")


# In[21]:

listnameAll=[]
listgainAll=[]

gain = Orange.feature.scoring.InfoGain()

for feature in dataAll.domain.features:
    listnameAll.append(feature.name)
    listgainAll.append(gain(feature, dataAll))
    
mAll = dict(zip(listnameAll, listgainAll))
#del mAll["LKADT_P"]
#del mAll["DISCONT"]
from collections import OrderedDict
from operator import itemgetter

mAll = OrderedDict(sorted(mAll.items(), key=itemgetter(1) , reverse = True))

listAll = []

i = 1
for label in mAll.keys():
    if i <= 16 :
        listAll.append(label)
        i+=1
    else :
        break
dataoriAll.to_csv("Train_afterAll.csv",columns=listAll,index=False)
datatestAll.to_csv("Test_afterAll.csv",columns=listAll,index=False)

