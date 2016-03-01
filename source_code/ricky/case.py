from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
def case(label,data,case):
	if case == 1:
		rf = RandomForestClassifier(n_estimators = 100)
		#rf= RandomForestClassifier(n_estimators = 100, max_depth=6, min_samples_leaf=20, max_features=7)
                rf.fit(data,label)
		return rf
	elif case ==2:
		#print 'label = {0}'.format(label)
                input =  label['ENDTRS_C'].str.contains("AE")*1
		#print 'input = {0}'.format(input)
                #print 'type(input) = {0}'.format(type(input))
                rf = RandomForestClassifier(n_estimators = 100)
		#rf= RandomForestClassifier(n_estimators = 100, max_depth=6, min_samples_leaf=20, max_features=7)
                rf.fit(data,input)
		return rf
        elif case ==3:
                input =  label['ENDTRS_C'].str.contains("AE")*1
                rf = GradientBoostingClassifier()
                rf.fit(data,input)
		return rf
