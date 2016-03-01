
setwd("C:/Users/Ricky/Desktop")
source("ensemble.R")
source("model.R")
library(survival)

train1 <- read.csv(file="Train_after1.csv")
train2 <- read.csv(file="Train_after2.csv")
train3 <- read.csv(file="Train_after3.csv")
test1 <- read.csv(file="Test_after1.csv")
test2 <- read.csv(file="Test_after2.csv")
test3 <- read.csv(file="Test_after3.csv")

fit_coxph1 <- coxph(Surv(train1$LKADT_P, train1$DEATH) ~ ., train1)
fit_coxph2 <- coxph(Surv(train2$LKADT_P, train2$DEATH) ~ ., train2)
fit_coxph3 <- coxph(Surv(train3$LKADT_P, train3$DEATH) ~ ., train3)

train1 = train1[(summary(fit_coxph1)$coefficients[,5])<0.2]
train2 = train2[(summary(fit_coxph2)$coefficients[,5])<0.2]
train3 = train3[(summary(fit_coxph3)$coefficients[,5])<0.2]
test1 = test1[(summary(fit_coxph1)$coefficients[,5])<0.2]
test2 = test2[(summary(fit_coxph2)$coefficients[,5])<0.2]
test3 = test3[(summary(fit_coxph3)$coefficients[,5])<0.2]

in1 = model(train1,test1)
in2 = model(train2,test2)
in3 = model(train3,test3)
in1 = rank(in1)
in2 = rank(in2)
in3 = rank(in3)
data = cbind(in1,in2,in3)

RPT <- read.csv(file = "CoreTable_validation.csv")
RPT <- RPT["RPT"]
RISK <- ens("average",data)
ensresult <- cbind(RPT, RISK)
write.csv(ensresult, file = "Q1A.csv",row.names=FALSE)
