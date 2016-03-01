
# coding: utf-8

# In[18]:

import pandas as pd
import Orange

dataori1 = pd.read_csv("Train1.csv")
dataori2 = pd.read_csv("Train2.csv")
dataori3 = pd.read_csv("Train3.csv")


datatest1 = pd.read_csv("Test1.csv")
datatest2 = pd.read_csv("Test2.csv")
datatest3 = pd.read_csv("Test3.csv")



df1 = pd.DataFrame(dataori1)
df2 = pd.DataFrame(dataori2)
df3 = pd.DataFrame(dataori3)

for column in dataori1.columns:
    df1.rename(columns={column: 'D#'+column}, inplace=True)
for column in dataori2.columns:
    df2.rename(columns={column: 'D#'+column}, inplace=True)
for column in dataori3.columns:
    df3.rename(columns={column: 'D#'+column}, inplace=True)

df1.rename(columns={"D#DEATH": 'c#DEATH'}, inplace=True)
df2.rename(columns={"D#DEATH": 'c#DEATH'}, inplace=True)
df3.rename(columns={"D#DEATH": 'c#DEATH'}, inplace=True)

df1.to_csv("Train_after1.csv",index=False)
df2.to_csv("Train_after2.csv",index=False)
df3.to_csv("Train_after3.csv",index=False)

data1 = Orange.data.Table("Train_after1.csv")
data2 = Orange.data.Table("Train_after2.csv")
data3 = Orange.data.Table("Train_after3.csv")

listname1=[]
listgain1=[]
listname2=[]
listgain2=[]
listname3=[]
listgain3=[]

gain = Orange.feature.scoring.InfoGain()

for feature in data1.domain.features:
    listname1.append(feature.name)
    listgain1.append(gain(feature, data1))

for feature in data2.domain.features:
    listname2.append(feature.name)
    listgain2.append(gain(feature, data2))

for feature in data3.domain.features:
    listname3.append(feature.name)
    listgain3.append(gain(feature, data3))
    
#print feature.name, gain(feature, data1)

m1 = dict(zip(listname1, listgain1))
m2 = dict(zip(listname2, listgain2))
m3 = dict(zip(listname3, listgain3))


del m1["LKADT_P"]
del m2["LKADT_P"] 
del m3["LKADT_P"] 


from collections import OrderedDict
from operator import itemgetter

m1 = OrderedDict(sorted(m1.items(), key=itemgetter(1) , reverse = True))
m2 = OrderedDict(sorted(m2.items(), key=itemgetter(1) , reverse = True))
m3 = OrderedDict(sorted(m3.items(), key=itemgetter(1) , reverse = True))
#print m

list1 = []
list2 = []
list3 = []


i = 1
for label in m1.keys():
    if i <= 15 :
        list1.append(label)
        i+=1
    else :
        break
i = 1
for label in m2.keys():
    if i <= 15 :
        list2.append(label)
        i+=1
    else :
        break
i = 1
for label in m3.keys():
    if i <= 15 :
        list3.append(label)
        i+=1
    else :
        break

datatest1.to_csv("Test_after1.csv",columns=list1,index=False)
datatest2.to_csv("Test_after2.csv",columns=list2,index=False)
datatest3.to_csv("Test_after3.csv",columns=list3,index=False)

list1.append('LKADT_P')
list1.append('DEATH')
list2.append('LKADT_P')
list2.append('DEATH')
list3.append('LKADT_P')
list3.append('DEATH')
        
dataori1.to_csv("Train_after1.csv",columns=list1,index=False)
dataori2.to_csv("Train_after2.csv",columns=list2,index=False)
dataori3.to_csv("Train_after3.csv",columns=list3,index=False)


# In[19]:


print list1

print list2

print list3


# In[ ]:



