require("survival")
require("timeROC")
require("Bolstad2")
require("ROCR")
require("survivalMPL")
require("plyr")
require("caret")
require("discretization")
require("FSelector")

source("bin.R")
setwd("~/Desktop/Dream Challenge/DATA/Cox version/Q1b")

test_data <- read.csv(file="CoreTable_leaderboard.csv")
data1 <- read.csv(file="A.csv")
data2 <- read.csv(file="B.csv")
data3 <- read.csv(file="C.csv")
data_all <- rbind(data1, data2, data3)


## 先處理training data
LKADT_P <- data_all[,"LKADT_P"]
DEATH <- data_all[,"DEATH"]
for (i in 1:nrow(data_all)) {
  if (data_all[i,"LKADT_P"] < 387) data_all[i,"LKADT_P"] <- 1
  else data_all[i,"LKADT_P"] <- 0
}

class_attr <- data_all[,"LKADT_P"]
data_all["LKADT_P"] <- NULL
train_condata <- con(data_all)
train_dicdata <- dic(data_all)
train_condata <- cbind(train_condata, class_attr)

bin_result <- mdlp(train_condata)
cut_point <- bin_result$cutp
bin_data <- bin_result$Disc.data
bin_data[ncol(bin_data)] <- NULL
data_all <-cbind(bin_data, train_dicdata, class_attr)

gain <- information.gain(class_attr~., data_all)
select_feature <- c(row.names(gain)[gain!=0])
data_all <- data_all[select_feature]
data_all$AGEGRP2 <- as.numeric(data_all$AGEGRP2)
training_data <- cbind(data_all, DEATH, LKADT_P)


## 處理test data
LKADT_P <- test_data[,"LKADT_P"]
DEATH <- test_data[,"DEATH"]

test_condata <- con(test_data)
test_dicdata <- dic(test_data)
cut_point <- All_to_Zero(cut_point)
test_bin_result <- mdlp_test(test_condata, cut_point)

test_bin_data <- test_bin_result$Disc.data
test_data <-cbind(test_bin_data, test_dicdata)
test_data <- test_data[select_feature]
test_data <- cbind(test_data, DEATH, LKADT_P)
test_data$AGEGRP2 <- as.numeric(test_data$AGEGRP2)

write.csv(x = training_data, file = "training_Q1b.csv",row.names = FALSE)
write.csv(x = test_data, file = "test_Q1b.csv",row.names = FALSE)
