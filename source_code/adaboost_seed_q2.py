
from math import log

from adaboost_seed import Adaboost


class Adaboost_q2(Adaboost):
    """
    A adaboost like regressor for subchallenge 2.

    Parameters
    ----------
    regressor : object

    Returns
    -------
    self : returns an instance of self.

    """

    def __init__(self, regr_name, random_fname, threshold):
        Adaboost.__init__(self, regr_name, random_fname)
        self.threshold = threshold


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
        print 'train_model'
        #print 'sample_weight = {0}'.format(sample_weight)
        X, y, delta, sample_weight = self._sample(X, y, delta, sample_weight)
        #print 'After sampling, sample_weight = {0}'.format(sample_weight)

        regr = self._regressor(self.regr_name)
        regr.fit(X, y)

        error_M, error_mean = self._error_model(X, y, delta, sample_weight, regr)
        if error_M > 0.5:
            print 'error_M > 0.5'
            return None, None, None

        for i in xrange(X.shape[0]):
            #print 'Calculating {0}-th instance sample_weight.'.format(i)
            #if abs(regr.predict(X[i]) - y[i]) < error_mean: ### error less than the mean
            if abs(regr.predict(X[i]) - y[i]) < self.threshold: ### error less than the mean
                if error_M == 0:
                    continue
                else:
                    sample_weight[i] = (error_M/float(1-error_M)) * sample_weight[i]

        #print 'After weighting, sample_weight = {0}'.format(sample_weight)
        sample_weight = self._normalizing_weight(sample_weight)
        if error_M == 0:
            regr_weight = 100
        else:
            regr_weight = log((1-error_M)/float(error_M))
        #print 'In end of train_model, sample_weight = {0}'.format(sample_weight)
        return regr, sample_weight, regr_weight


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
        print '_error_model'
        error = 0
	error_mean = self._error_mean(X, y, delta, regressor)

	for i in xrange(X.shape[0]):
            # For uncensored data or censored data with its predicted value less than its true value
            #print 'Calculating {0}-th instance for its error.'.format(i)
            #if abs(regressor.predict(X[i]) - y[i]) > error_mean:
            pred = regressor.predict(X[i])
            #print 'pred vs y = {0} vs {1}'.format(pred, y[i])
            diff = abs(pred - y[i])
            #print 'diff vs threshold = {0} vs {1}'.format(diff, self.threshold)
            if diff > self.threshold:
                error = error + sample_weight[i]
        return  error, error_mean


    def _error(self, X, y, error_mean, sample_weight, regressor):
        subtract_array = np.absolute(np.subtract(regressor.predict(X), y)) - error_mean
        count = np.count_nonzero(np.sort(subtract_array)[::-1])
        return np.sum(sample_weight[np.argsort(subtract_array)[::-1][:count]])


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
	print '_error_mean'
        error_sum = 0
	for i in xrange(X.shape[0]):
            #print 'Summing {0}-th instance for error_sum.'.format(i)
            error_sum = error_sum + abs(regressor.predict(X[i]) - y[i])
	return	error_sum/float(X.shape[0])

