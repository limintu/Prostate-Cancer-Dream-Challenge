
import numpy as np
from numpy.random import choice
from math import log
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
import linecache


class Adaboost:
    """
    A adaboost like regressor for 1b subchallenge.

    Parameters
    ----------
    regressor : object

    Returns
    -------
    self : returns an instance of self.

    """

    def __init__(self, regr_name, r_index, random_fname):
        self.regr_name = regr_name
        self.regr_list = [] ### each element is a tuple (regressor, regressor weight)
        self.r_index = r_index
        self.random_fname = random_fname

    def fit(self, X, y, delta, n_iter, sample_weight=None):
        """
        Fit the adaboost model.

        Parameters
        ----------
        X : numpy array, shape = [n_samples, n_features]
            Training data

        y : numpy array, shape = [n_samples,]
            Target values

        delta : numpy array, shape = [n_samples,]
            Censor indicator, 1 : censored, 0 : uncensored

        n_iter : number
            number of iteration

        sample_weight : array-like of shape = [n_samples]
            The current sample weights.

        Returns
        -------
        self: returns an instance of self.
        """

        if sample_weight is None:
            # Initialize weights to 1 / n_samples
            sample_weight = self._initial_sample_weight(X)
        else:
            # Normalize existing weights
            sample_weight = sample_weight / sample_weight.sum(dtype=np.float64)

            # Check that the sample weights sum is positive
            if sample_weight.sum() <= 0:
                raise ValueError(
                    "Attempting to fit with a non-positive "
                    "weighted number of samples.")

        for i in xrange(n_iter):
            regr, sample_weight, regr_weight = self.train_model(X, y, delta, sample_weight)
            count = 0
            while regr is None or sample_weight is None or regr_weight is None:
                print 'regr is None or sample_weight is None or weight is None'
                print 'count of error_M > 0.5 = {0}'.format(count)
                sample_weight = self._initial_sample_weight(X)
                regr, sample_weight, regr_weight = self.train_model(X, y, delta, sample_weight)
                count = count + 1
            self.regr_list.append((regr, regr_weight))
        return self


    def _initial_sample_weight(self, X):
        """
        Initialize the sample weight

        Parameters
        ----------
        X : numpy array, shape = [n_samples, n_features]
            Training data

        Returns
        -------
        sample_weight : array-like of shape = [n_samples]
            The sample weight, each element is 1 / n_samples

        """

        sample_weight = np.empty(X.shape[0], dtype=np.float)
        sample_weight[:] = 1. / X.shape[0]
        return sample_weight


    def predict(self, X, mode="max"):
        """
        Predict using the model.

        Parameters
        ----------
            X : numpy array, shape = (n_samples, n_features)
                Training data

            mode : string, default="max", mode set = {"max", "mean"}
                the prediction mode

        Returns
        -------
            C : array, shape = [n_samples,]

                Returns predicted values.
        """
        if len(self.regr_list) == 0:
            raise Exception('Not fit regressor from data.')

        if mode == 'max':
            weight_list = [w for (r, w) in self.regr_list]
            m = max(weight_list)
            max_i_list = [i for i, j in enumerate(weight_list) if j == m]

            final_results = np.zeros((X.shape[0],))
            for i in range(X.shape[0]): # for each data instance
                results_max_model = np.zeros((len(max_i_list),))
                for k in xrange(len(max_i_list)):
                    results_max_model[k] = self.regr_list[max_i_list[k]][0].predict(X[i])
                final_results[i] = np.mean(results_max_model, axis=0)

        elif mode == 'mean':
            final_results = np.zeros((X.shape[0],))
            for i in range(X.shape[0]): # for each data instance
                result_instance_all_regressors = []
                for (r, w) in self.regr_list:
                    result_instance_all_regressors.append(r.predict(X[i]))
                final_results[i] = np.mean(np.array(result_instance_all_regressors), axis=0)
        return final_results



    def train_model(self, X, y, delta, sample_weight):
        """
        To train the regression model.

        Parameters
        ----------
            X : numpy array, shape = (n_samples, n_features)
                Training data

            y : numpy array, shape = (n_samples,)
                Target values

            delta : numpy array, shape = [n_samples,]
                Censor indicator, 1 : censored, 0 : uncensored

            sample_weight : numpy array, shape=(n_samples,)
                Weight of samples.

        Returns
        -------
            model : a Model instance, its attribute coef: array, shape = [n_features,], intercept: array

            sample_weight : numpy array, shape=(n_samples,)
                Weight of resampled data.
        """

        X, y, delta, sample_weight = self._sample(X, y, delta, sample_weight)
        #X_uc, y_uc, delta_uc, sample_weight_uc = self._uncensored_sample(X, y, delta, sample_weight)

        regr = self._regressor(self.regr_name)
        regr.fit(X, y)

        error_M, error_mean = self._error_model(X, y, delta, sample_weight, regr)
        #error_M_uc, error_mean_uc = self._error_model(X_uc, y_uc, delta_uc, sample_weight_uc, regr)

        #if error_M > error_M_uc:
        #    return None, None, None

        if error_M > 0.5:
            return None, None, None


	#This part is changed by Yofu
	predict_result = [regr.predict(X[i]) for i in xrange(X.shape[0])]


	for i in xrange(X.shape[0]):
            if (delta[i] == 0 and abs(predict_result[i] - y[i]) < error_mean) or (delta[i] == 1 and predict_result[i] > y[i]):
                sample_weight[i] = (error_M/float(1-error_M)) * sample_weight[i]

	#This part is changed by Yofu

        sample_weight = self._normalizing_weight(sample_weight)
        regr_weight = log((1-error_M)/float(error_M))
        return regr, sample_weight, regr_weight


    def _regressor(self, regr_name):
        if regr_name == 'linear':
            return linear_model.LinearRegression()
        elif regr_name == 'random_forest':
            return RandomForestRegressor(n_estimators=10, min_samples_split=2, n_jobs=-1)
        elif regr_name == 'decision_tree':
            return DecisionTreeRegressor()


    def _normalizing_weight(self, arr):
        """
        To normalizing the input array.

        Parameters
        ----------
            arr: array, shape = [n_samples,]

        Returns
        -------
            arr: array, shape = [n_samples,]

        """
        arr /= arr.sum()
        return np.array(arr)


    def _error_model(self, X, y, delta, sample_weight, regressor):
        """
        To compute the error of the regressor model.

        Parameters
        ----------
            X: numpy array, shape=(n_samples, n_features)
                Samples.

            y : numpy array, shape = (n_samples,)
                Target values

            delta : numpy array, shape = [n_samples,]
                Censor indicator, 1 : censored, 0 : uncensored

            sample_weight: numpy array, shape=(n_samples,)
                Weight of samples.

            regressor: function
                Regressor.
        Returns
        -------
            error: float
        """

        error = 0
	error_mean = self._error_mean(X, y, delta, regressor)

	for i in xrange(X.shape[0]):
            # For uncensored data or censored data with its predicted value less than its true value
            if delta[i] == 0: ### uncensored data
                error = error + sample_weight[i]*self._error_uncensored(X[i], y[i], error_mean, regressor)
            elif delta[i] == 1 and regressor.predict(X[i]) < y[i]: ### censored data
                error = error + sample_weight[i]
        return  error, error_mean


    def _error_mean(self, X, y, delta, regressor):
	"""
        Return the mean of all error.

	Parameters
	----------
            X: numpy array, shape=(n_samples, n_features)
                Samples.

            y : numpy array, shape = (n_samples,)
                Target values

            delta : numpy array, shape = [n_samples,]
                Censor indicator, 1 : censored, 0 : uncensored

        Returns
	-------
            error_mean : number
                The mean of all error
	"""
	error_sum = 0

	#This part is changed by Yofu
	predict_result = [regressor.predict(X[i]) for i in xrange(X.shape[0])]

	for i in xrange(X.shape[0]):
            # For uncensored data or censored data with its predicted value less than its true value
            if delta[i] == 0 or (delta[i] == 1 and predict_result[i] < y[i]):
                error_sum = error_sum + abs(predict_result[i] - y[i])
	return	error_sum/float(X.shape[0])

	#This part is changed by Yofu



    def _error_uncensored(self, X_i, y_i, error_mean, regressor):
	"""
        Return indicator values of uncensored data.

	Parameters
	----------
            X_i : numpy array, shape = [n_features,]
                The i-th element

            y_i : number
                The dependent value of the i-th element

            error_mean : number
                The mean of all error

	Returns
	-------
            error: number
                The error value

	"""
        if abs(regressor.predict(X_i) - y_i) > error_mean:
            return  1
        else:
            return 0


    def _normalized_RMSE():
	"""

	Parameters
	----------

	Returns
	-------

	"""

	return


    def _uncensored_sample(self, X, y, delta, sample_weight):
        """
        Get uncensored samples from training data.

        Parameters
        ----------

            X : numpy array, shape = (n_samples, n_features)
                Training data

            y : numpy array, shape = (n_samples,)
                Target values

            delta : numpy array, shape = [n_samples,]
                Censor indicator, 1 : censored, 0 : uncensored

            sample_weight : numpy array, shape=(n_samples,)
                Weight of resampled samples

        Returns
        -------
            X : numpy array, shape = (n_samples, n_features)
                Resampled training data

            y : numpy array, shape = (n_samples,)
                Target values of the resampled training data

            delta : numpy array, shape = [n_samples,]
                Censor indicator of the resampled training data, 1 : censored, 0 : uncensored

            sample_weight : numpy array, shape=(n_samples,)
                Weight of resampled samples
	"""
        i_list = [i for i, v in enumerate(delta) if v == 0]
        X = np.array([X[i] for i in i_list])
        y = np.array([y[i] for i in i_list])
        delta = np.array([delta[i] for i in i_list])
        sample_weight = np.array([sample_weight[i] for i in i_list])
        sample_weight = self._normalizing_weight(sample_weight)
        return X, y, delta, sample_weight


    def _sample(self, X, y, delta, sample_weight):
        """
        Get samples from training data according to the sample weight.

        Parameters
        ----------

            X : numpy array, shape = (n_samples, n_features)
                Training data

            y : numpy array, shape = (n_samples,)
                Target values

            delta : numpy array, shape = [n_samples,]
                Censor indicator, 1 : censored, 0 : uncensored

            sample_weight : numpy array, shape=(n_samples,)
                Weight of samples.

        Returns
        -------
            X : numpy array, shape = (n_samples, n_features)
                Resampled training data

            y : numpy array, shape = (n_samples,)
                Target values of the resampled training data

            delta : numpy array, shape = [n_samples,]
                Censor indicator of the resampled training data, 1 : censored, 0 : uncensored

            sample_weight : numpy array, shape=(n_samples,)
                Weight of resampled samples
	"""
	#print 'sample_weight = {0}'.format(sample_weight)
        #print 'np.sum(sample_weight) = {0}'.format(np.sum(sample_weight))

        #i_array = choice([x for x in xrange(X.shape[0])], X.shape[0], p=sample_weight)
        #print 'type(r_index) = {0}'.format(type(r_index))
	print 'self.random_fname = {0}'.format(self.random_fname)
        i_array = linecache.getline(self.random_fname, self.r_index)
	i_array = [int(i) for i in i_array.split()]
	#print type(r_index)
        self.r_index = self.r_index + 1

        #print 'i_array = {0}'.format(i_array)
        X = np.array([X[i] for i in i_array])
        y = np.array([y[i] for i in i_array])
        
        
        #write the index
        #with open('random.txt', 'a+') as f:
    		#f.write(" ".join(map(str, i_array)))
    		#f.write("\n")
    	#
        delta = np.array([delta[i] for i in i_array])
        sample_weight = np.array([sample_weight[i] for i in i_array])
        sample_weight = self._normalizing_weight(sample_weight)
        return X, y, delta, sample_weight
