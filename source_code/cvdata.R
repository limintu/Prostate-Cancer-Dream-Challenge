library(caret)
library(plyr)
cvtest<-function(data,x){
	test_data <- data[1,]
	for (i in 1:nrow(data)){
		if (data[i,"fold"]==x) {
			test_data <- rbind(test_data, data[i,]) 
		}
	}
	test_data <- test_data[-1,]
	test_data[,"fold"]<- NULL
	rownames(test_data)<- NULL
	return(test_data)
}
cvtrain<-function(data,x){
	training_data <- data[1,]
	for (i in 1:nrow(data)){
		if (data[i,"fold"]!=x) {
			training_data <- rbind(training_data, data[i,])
		}
	}
	training_data <- training_data[-1,]
	training_data[,"fold"]<- NULL
	rownames(training_data)<- NULL
	return(training_data)
}