library(discretization)
con<-function(temp){	
	headerc = c("BMI","ALP","ALT","AST","CA","CREAT","HB","LDH","NEU","PLT","PSA","TBILI","TESTO","WBC","CREACL","NA.","MG","PHOS","ALB","TPRO","RBC","LYM")
	condata = temp[headerc]
	return(condata)
}
dic<-function(temp){
	headerd = c("AGEGRP2","ECOG_C","NON_TARGET","TARGET","BONE","RECTAL","LYMPH_NODES","KIDNEYS","LUNGS","LIVER","PLEURA","OTHER","PROSTATE","ADRENAL","BLADDER","PERITONEUM","COLON","HEAD_AND_NECK","SOFT_TISSUE","STOMACH","PANCREAS","THYROID","ABDOMINAL","ORCHIDECTOMY","PROSTATECTOMY","TURP","LYMPHADENECTOMY","SPINAL_CORD_SURGERY","BILATERAL_ORCHIDECTOMY","PRIOR_RADIOTHERAPY","ANALGESICS","ANTI_ANDROGENS","GLUCOCORTICOID","GONADOTROPIN","BISPHOSPHONATE","CORTICOSTEROID","IMIDAZOLE","ACE_INHIBITORS","BETA_BLOCKING","HMG_COA_REDUCT","ESTROGENS","ANTI_ESTROGENS","ARTTHROM","CEREBACC","CHF","DVT","DIAB","GASTREFL","GIBLEED","MI","PUD","PULMEMB","PATHFRAC","SPINCOMP","COPD","MHBLOOD","MHCARD","MHCONGEN","MHEAR","MHENDO","MHEYE","MHGASTRO","MHGEN","MHHEPATO","MHIMMUNE","MHINFECT","MHINJURY","MHINVEST","MHMETAB","MHMUSCLE","MHNEOPLA","MHNERV","MHPSYCH","MHRENAL","MHRESP","MHSKIN","MHSOCIAL","MHSURG","MHVASC")
	disdata = temp[headerd]
	return(disdata)
}
lab<-function(temp,lab){
	label = temp[lab]
	return (label)
}
All_to_Zero <- function(x){
    for (i in 1: length(x)) {
        if (x[[i]][1] == "All" ) x[[i]] <- numeric(0)
    }
    return(x)
}
mdlp_train <- function(data){
    p <- length(data[1,])-2
    y <- data[,(p+2)]
    xd <- data
    cutp <- list()
    for (i in 1:p){
        x <- data[,i]
        cuts1 <- cutPoints(x,y)
        cuts <- c(min(x),cuts1,max(x))
        cutp[[i]] <- cuts1
        if(length(cutp[[i]])==0) cutp[[i]] <- "All"
        xd[,i] <- as.integer(cut(x,cuts,include.lowest = TRUE))
    }
    return (list(cutp=cutp,Disc.data=xd))
}
mdlp_test <- function(data, cut_point){
    p <- length(data[1,])
    xd <- data
    cutp <- list()
    for (i in 1:p){
        x <- data[,i]
        cuts1 <- cut_point[[i]]
        cuts <- c(min(x),cuts1,max(x))
        cutp[[i]] <- cuts1
        if(length(cutp[[i]])==0) cutp[[i]] <- "All"
        xd[,i] <- as.integer(cut(x,cuts,include.lowest = TRUE))
    }
    return (list(cutp=cutp,Disc.data=xd))
}
HowToBin<-function(condata1,condata2,condata3,label1,label2,label3,test1,test2,test3){
	header = c("BMI","ALP","ALT","AST","CA","CREAT","HB","LDH","NEU","PLT","PSA","TBILI","TESTO","WBC","CREACL","NA.","MG","PHOS","ALB","TPRO","RBC","LYM")
	num = c(28.6,69,16,19,2.4,80,12.9,200,5,200,4,5,20,7,110,142,0.75,1.1,40,70,5,2.5)	
	condata1$center = 1
	condata2$center = 2
	condata3$center = 3
	condata1 = cbind(condata1,label1)
	condata2 = cbind(condata2,label2)
	condata3 = cbind(condata3,label3)
	alldata = rbind(condata1,condata2,condata3)
	dataini = alldata
	t1 = alldata[alldata$center==1,][,1]
	t2 = alldata[alldata$center==2,][,1]
	t3 = alldata[alldata$center==3,][,1]
	count =0
	c1 = 0
	c2 = 0
	c3 = 0
	for (i in 1:(length(alldata)-2)){
		#if ( (sum(alldata[i]==num[i])) > (length(rownames(alldata)) * 0.8 )){
			name = header[i]
			temp <- dataini[1,][i]
			temp$center <- 1
			temp$DEATH <- label1[1,1]
			if((sum(condata1[i]==num[i]))<(length(rownames(condata1))*0.8)){
				temp1 = condata1[i] 
				temp1$center = 1
				temp1[3] = label1
				temp<-rbind(temp,temp1) 
				count =c(count ,1)
				alldata[header[i]] = NULL
			}
			else{
				test1[header[i]] = NULL
			}
			if((sum(condata2[i]==num[i]))<(length(rownames(condata2))*0.8)){
				temp1 = condata2[i]
				temp1$center = 2
				temp1[3] = label2
				temp<-rbind(temp,temp1)
				count =c(count ,2)
				alldata[header[i]] = NULL
			}
			else{
				test2[header[i]] = NULL
			}
			if((sum(condata3[i]==num[i]))<(length(rownames(condata3))*0.8)){
				temp1 = condata3[i]
				temp1$center = 3
				temp1[3] = label3
				temp<-rbind(temp,temp1)
				count =c(count ,3)
				alldata[header[i]] = NULL
			}
			else{
				test3[header[i]] = NULL
			}
			temp <- temp[-1,]
			if((length(rownames(temp)))!=0){
				result <- mdlp_train(temp)
				if(length(result$Disc.data[result$Disc.data[2]==1,][,1])!=0){
					t1 = cbind(t1,result$Disc.data[result$Disc.data[2]==1,][,1])			
					colnames(t1)[ncol(t1)] <- name
				}
				if(length(result$Disc.data[result$Disc.data[2]==2,][,1])!=0){
					t2 = cbind(t2,result$Disc.data[result$Disc.data[2]==2,][,1])
					colnames(t2)[ncol(t2)] <- name
				}
				if(length(result$Disc.data[result$Disc.data[2]==3,][,1])!=0){
					t3 = cbind(t3,result$Disc.data[result$Disc.data[2]==3,][,1])
					colnames(t3)[ncol(t3)] <- name
				}
				if(sum(count==1)==1){
					c1 = c(c1,result$cutp)
				}
				if(sum(count==2)==1){
					c2 = c(c2,result$cutp)
				}
				if(sum(count==3)==1){
					c3 = c(c3,result$cutp)
				}
				count = 0
			}
			
		#}			
	}	
	c1 = c1[-1]
	c2 = c2[-1]
	c3 = c3[-1]
	t1 = t1[,-1]
	t2 = t2[,-1]
	t3 = t3[,-1]
	return(list(t1,t2,t3,c1,c2,c3,test1,test2,test3))
}
