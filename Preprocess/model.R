suppressMessages(library("survival"))
suppressMessages(library("ROCR"))
suppressMessages(library("survivalMPL"))
suppressMessages(library("plyr"))
suppressMessages(library("caret"))
suppressMessages(library("penalized"))

model<-function(training_data,test_data){	
	fit_MPL <- coxph_mpl(Surv(training_data$LKADT_P, training_data$DEATH) ~ ., training_data)  
	#Beta??
	coefficient <- fit_MPL$coef$Beta
	Beta <- coefficient  
	#cumulated baseline hazard estimate (survival function)
	predict_MPL <- predict(fit_MPL, type = "survival")
	S0 <- predict_MPL$survival[229]  
	### computation ###  
	#b1*x1+b2*x2+....+bn*xn
	value <- vector("numeric", length(test_data[,1]))	
	for (j in 1:nrow(test_data)){
		for (i in 1:(ncol(test_data))){
			value[j] <- value[j] + test_data[j,i]*Beta[i]
		}
	}  
	#exponential
	power <- value
	for (i in 1:length(power)){
		power[i] <- exp(value[i])
	}  
	#base hazard??????
	result <- power
	for (i in 1:length(power)){
		result[i] <- S0^power[i]
	}
	return(1-result)
}