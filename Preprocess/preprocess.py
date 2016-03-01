
# coding: utf-8

# In[73]:

import pandas as pd


# In[74]:

# read the file according to the path
# Please change it depend on your need

train=pd.read_csv("CoreTable_training.csv")
test=pd.read_csv("CoreTable_leaderboard.csv")


# In[75]:

#Data preprocessing  #
train=train.convert_objects(convert_numeric=True)
test=test.convert_objects(convert_numeric=True)
train['DEATH']=train['DEATH'].fillna("No")
train['DEATH']=train['DEATH'].replace("YES", "Yes")
test['DEATH']=test['DEATH'].fillna("No")
test['DEATH']=test['DEATH'].replace(".", "No")
print train["AGEGRP2"]


train["AGEGRP2"]=train["AGEGRP2"].replace("18-64",1)
train["AGEGRP2"]=train["AGEGRP2"].replace("65-74",2)
train["AGEGRP2"]=train["AGEGRP2"].replace(">=75",3)


# In[76]:

x = ['NON_TARGET',
 'TARGET',
 'BONE',
 'RECTAL',
 'LYMPH_NODES',
 'KIDNEYS',
 'LUNGS',
 'LIVER',
 'PLEURA',
 'OTHER',
 'PROSTATE',
 'ADRENAL',
 'BLADDER',
 'PERITONEUM',
 'COLON',
 'HEAD_AND_NECK',
 'SOFT_TISSUE',
 'STOMACH',
 'PANCREAS',
 'THYROID',
 'ABDOMINAL',
 'ORCHIDECTOMY',
 'PROSTATECTOMY',
 'TURP',
 'LYMPHADENECTOMY',
 'SPINAL_CORD_SURGERY',
 'BILATERAL_ORCHIDECTOMY',
 'PRIOR_RADIOTHERAPY',
 'ANALGESICS',
 'ANTI_ANDROGENS',
 'GLUCOCORTICOID',
 'GONADOTROPIN',
 'BISPHOSPHONATE',
 'CORTICOSTEROID',
 'IMIDAZOLE',
 'ACE_INHIBITORS',
 'BETA_BLOCKING',
 'HMG_COA_REDUCT',
 'ESTROGENS',
 'ANTI_ESTROGENS',
 'ARTTHROM',
 'CEREBACC',
 'CHF',
 'DVT',
 'DIAB',
 'GASTREFL',
 'GIBLEED',
 'MI',
 'PUD',
 'PULMEMB',
 'PATHFRAC',
 'SPINCOMP',
 'COPD',
 'MHBLOOD',
 'MHCARD',
 'MHCONGEN',
 'MHEAR',
 'MHENDO',
 'MHEYE',
 'MHGASTRO',
 'MHGEN',
 'MHHEPATO',
 'MHIMMUNE',
 'MHINFECT',
 'MHINJURY',
 'MHINVEST',
 'MHMETAB',
 'MHMUSCLE',
 'MHNEOPLA',
 'MHNERV',
 'MHPSYCH',
 'MHRENAL',
 'MHRESP',
 'MHSKIN',
 'MHSOCIAL',
 'MHSURG',
 'MHVASC']


# In[77]:

train[x]=train[x].fillna(0)
test[x]=test[x].fillna(0)


# In[78]:

train[x]= train[x].replace(".", 0)
test[x]= test[x].replace(".", 0)


# In[79]:

train[x]= train[x].replace("Y", 1)
train[x]= train[x].replace("YES", 1)
test[x]= test[x].replace("Y", 1)
test[x]= test[x].replace("YES", 1)
train=train.replace("NA.","NA")
test=test.replace("NA.","NA")


# In[80]:

#Imputation
train['BMI']=train['BMI'].fillna(28.6)
train['ALP']=train['ALP'].fillna(69)
train['ALT']=train['ALT'].fillna(16)
train['AST']=train['AST'].fillna(19)
train['CA']=train['CA'].fillna(2.4)
train['CREAT']=train['CREAT'].fillna(80)
train['HB']=train['HB'].fillna(12.9)
train['LDH']=train['LDH'].fillna(200)
train['NEU']=train['NEU'].fillna(5)
train['PLT']=train['PLT'].fillna(300)
train['PSA']=train['PSA'].fillna(4)
train['TBILI']=train['TBILI'].fillna(5)
train['TESTO']=train['TESTO'].fillna(20)
train['WBC']=train['WBC'].fillna(7)
train['CREACL']=train['CREACL'].fillna(110)
train['NA.']=train['NA.'].fillna(142)
train['MG']=train['MG'].fillna(0.75)
train['PHOS']=train['PHOS'].fillna(1.1)
train['ALB']=train['ALB'].fillna(40)
train['TPRO']=train['TPRO'].fillna(70)
train['RBC']=train['RBC'].fillna(5)
train['LYM']=train['LYM'].fillna(2.5)
    
test['BMI']=test['BMI'].fillna(28.6)
test['ALP']=test['ALP'].fillna(69)
test['ALT']=test['ALT'].fillna(16)
test['AST']=test['AST'].fillna(19)
test['CA']=test['CA'].fillna(2.4)
test['CREAT']=test['CREAT'].fillna(80)
test['HB']=test['HB'].fillna(12.9)
test['LDH']=test['LDH'].fillna(200)
test['NEU']=test['NEU'].fillna(5)
test['PLT']=test['PLT'].fillna(300)
test['PSA']=test['PSA'].fillna(4)
test['TBILI']=test['TBILI'].fillna(5)
test['TESTO']=test['TESTO'].fillna(20)
test['WBC']=test['WBC'].fillna(7)
test['CREACL']=test['CREACL'].fillna(110)
test['NA.']=test['NA.'].fillna(142)
test['MG']=test['MG'].fillna(0.75)
test['PHOS']=test['PHOS'].fillna(1.1)
test['ALB']=test['ALB'].fillna(40)
test['TPRO']=test['TPRO'].fillna(70)
test['RBC']=test['RBC'].fillna(5)
test['LYM']=test['LYM'].fillna(2.5)


# In[81]:

# Save the files


def out1(train):
    data1 =  train[train['RPT'].str.contains("ASC-")]
    return data1

def out2(train):
    data1 =  train[train['RPT'].str.contains("CELG-")]
    return data1

def out3(train):
    data1 =  train[train['RPT'].str.contains("VEN-")]
    return data1

acs = out1(train) 
gelg = out2(train) 
ven = out3(train) 


# Change the 4 paths if need
acs.to_csv("acs.csv",index= False)
gelg.to_csv("gelg.csv",index= False)
ven.to_csv("ven.csv",index= False)

test.to_csv("CoreTable_leaderboard_new.csv",index= False)





