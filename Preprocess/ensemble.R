ens<-function(method,datalist){
  len = dim(datalist)	
  ans = 0
  for(i in 1:len[1]){
    if(method == 'average'){
      ans = rowMeans(datalist)
    }
    else if(method == 'minimum'){
      ans[i] = min(datalist[i,])
    }
    else if(method == 'maximum'){
      ans[i] = max(datalist[i,])
    }
    else if(method == 'median'){
      ans[i] = median(as.numeric(datalist[i,]))
    }
    else if(method == 'trimmed mean'){
      ans[i] = (sum(datalist[i,])-min(datalist[i,])-max(datalist[i,]))/(len[2]-2)
    }
    else if(method == 'product'){
      ans[i] = 1
      for(j in 1:len[2]){
        ans[i] = ans[i] * datalist[i,j]
      }
    }
  }
  return(ans)
}

