import sklearn
def predict_with_regressor(X_train,y_train,X_test,case):
	if case == 1 :
		model1 = sklearn.ensemble.RandomForestRegressor()
		model1.fit(X_train,y_train)
		return model1.predict(X_test)

	elif case == 2 :
		model2 = sklearn.tree.DecisionTreeRegressor()
		model2.fit(X_train,y_train)
		return model2.predict(X_test)
