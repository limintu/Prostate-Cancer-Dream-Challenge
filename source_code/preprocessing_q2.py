import numpy as np
from q2 import score_q2
import csv



class X_processor:
    def __init__(self):
        pass


    def extractDependent(self, input_file):
        y = []
        delta = []
        z = []
        with open(input_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                ### save y
                y.append(row["ENTRT_PC"])
                ### save delta
                delta.append(row["DISCONT"])
                ### save z
                z.append(row["ENDTRS_C"])
        return np.array(y), np.array(delta), np.array(z)


    def tackle_missing(self, feature_headers, input_file):
        """
        Preprocess the data set of dream challenge

        Parameters
        ----------

        Return
        ------

            X : numpy array, shape = [n_samples, n_features]
                The feature array

            y : numpy array, shape = [n_samples,]
                The depedent variable array, that is, "ENTRT_PC" infomation

            delta : numpy array, shape = [n_samples,]
                The depedent variable  array, that is, "DISCONT" infomation

            z : numpy array, shape = [n_samples,]
                The depedent variable  array, that is, "ENDTRS_C" infomation

        """
        X = []
        y = []
        delta = []
        z = []
        with open(input_file) as csvfile:
            reader = csv.DictReader(csvfile)
            missing_indexs = []
            for i, row in enumerate(reader):
                value_ECOG_C = self._tackle_ECOG_C_missing(row)
                if value_ECOG_C is not None:
                    value_ENTRT_PC = self._tackle_ENTRT_PC_missing(row)
                    if value_ENTRT_PC is not None:
                        value_DISCONT = self._tackle_DISCONT_missing(row)
                        if value_DISCONT is not None:
                            y.append(value_ENTRT_PC)
                            delta.append(value_DISCONT)

                            ### save X
                            feature_list = []
                            for feature in feature_headers:
                                feature_list.append(row[feature])
                            X.append(feature_list)

                            ### save z
                            z.append(row["ENDTRS_C"])
                        else:
                            missing_indexs.append(i)
                            continue
                    else:
                        missing_indexs.append(i)
                        continue
                else:
                    missing_indexs.append(i)
                    continue
        return np.array(X), np.array(y), np.array(delta), np.array(z)


    def tackle_dot_missing(self, X, feature_headers):
        for i, h in enumerate(feature_headers):
            for j in xrange(X.shape[0]):
                content = self._checkMissingSymbol(X[j, i], i)
                if content is not None:
                    continue
                else:
                   raw_input(feature_headers[i])
        return X


    def _checkMissingSymbol(self, content, header_index):
        if content == '.':
            return None
        else:
            return content


    def _tackle_ECOG_C_missing(self, row):
        if row["ECOG_C"] == '.':
            return None
        else:
            return int(row["ECOG_C"])


    def _tackle_ENTRT_PC_missing(self, row):
        if row["ENTRT_PC"] == '.':
            return None
        else:
            return int(row["ENTRT_PC"])


    def tackle_ENTRT_PC_missing(self, X, y, delta, z):
        index_list = [i for i in xrange(len(y.tolist()))]
        for i, v in enumerate(y):
            if v == '.':
                index_list = [j for j in index_list if j != i]
        return X[index_list, :], y[index_list], delta[index_list], z[index_list]


    def _tackle_DISCONT_missing(self, row):
        if row["DISCONT"] == '.':
            if row["ENDTRS_C"] == "AE" or row["ENDTRS_C"] == "possible_AE":
                if int(row["ENTRT_PC"]) <= 90:
                    return 1
                else:
                    return 0
            else:
                return None
        else:
            return int(row["DISCONT"])


    def tackle_DISCONT_missing(self, y, delta, z):
        for i, v in enumerate(delta):
            if v == '.':
                if z[i] == "AE" or z[i] == "possible_AE":
                    if int(y[i]) <= 90:
                        delta[i] = 1
                    else:
                        delta[i] = 0
                else:
                    delta[i] = 0
        return delta


    def select_ENDTRS_C_data(self, X, y, delta, z):
        data_index_list = [i for i, v in enumerate(z) if v == 'AE' or v == 'possible_AE']
        return X[data_index_list, :], np.array([y.tolist()[i] for i in data_index_list]), np.array([delta.tolist()[i] for i in data_index_list]), np.array([z.tolist()[i] for i in data_index_list]), data_index_list


    def _select_data(self, row, feature_list):
        """
        To select data according to feature values.

        Parameters
        ----------

        feature_list : numpy array, [(feature_name1, feature_value1),...(feature_name_m, feature_value_m)]

        Return
        ------
            1 : match (feature_name, feature_value)
            None : none is matched
        """

        for f, v in feature_list:
            if row[f] == v:
                return 1
        return None


    def delete_feature(self, X, desired_feature, feature_headers):
        """
        To delete a specific feature from the feature array.

        Parameters
        ----------
            X : numpy array, shape = [n_samples, n_features]
                The feature array

            desired_feature : string
                The feature we want to delete.

            feature_headers : numpy array, shape = [n_features,]
                The feature headers array
        Return
        ------
            new_X: numpy array, shape = [n_samples, n_features]
                The processed feature array

            feature_headers : numpy array, shape = [n_features,]
                The new feature headers array
        """
        desired_index = self.feature_index(desired_feature, feature_headers)
        final_index_list = [x for x in range(len(feature_headers)) if x is not desired_index]
        feature_headers = np.delete(feature_headers, [desired_index])
        return X[:, final_index_list], feature_headers


    def add_dummy_features(self, X, dummy_features, dummy_features_headers, feature_headers):
        """
        To add dummy features to the feature array.

        Parameters
        ----------
            X : numpy array, shape = [n_samples, n_features]
                The feature array

            dummy_features : numpy array, shape = [n_samples, m_features]
                The features we want to add.

            dummy_features_headers : numpy array, shape = [n_features,]
                The dummy feature headers array

            feature_headers : numpy array, shape = [n_features,]
                The feature headers array

        Return
        ------
            new_X: numpy array, shape = [n_samples, n_features]
                The processed feature array

            feature_headers : numpy array, shape = [n_features,]
                The new feature headers array

        """
        feature_headers = np.append(feature_headers, dummy_features_headers, axis=0)
        return np.append(X, dummy_features, axis=1), feature_headers


    def feature_index(self, desired_feature, features):
        for i,f in enumerate(features):
            if f == desired_feature:
                return i
        return None


    def binning(self, X, value_range):
        """
        To bin a specific feature value.

        Parameters
        ----------
            X : numpy array, X.shape = [n_samples, n_features]
                The feature array. For example: X = np.array(["65-74", ">=75", "65-74", "65-74", "18-64", "65-74", "65-74", ">=75"]])
            value_range: numpy array
                The feature value range we want to bin. For example: value_range = np.array(["18-64", "65-74", ">=75"])
        Return
        ------
            new_X : numpy array
                The binned feature array containing dummy variables.
        """

        new_X = []
        for j in xrange(X.shape[0]):
            binned_value = [0]*len(value_range)
            for i, v in enumerate(value_range):
                if X[j, 0] == v:
                    binned_value[i] = 1
                    new_X.append(binned_value)
        return np.array(new_X)


    def _convertYesToInt(self, content):
        if content == "Y" or content == "YES" or content == "Yes":
            return 1
        elif content == "":
            return 0
        else:
            return content


    def convertYes(self, X, feature_headers, headers_for_convert_YES):
        for i, h in enumerate(feature_headers):
            if h in headers_for_convert_YES:
                for j in xrange(X.shape[0]):
                    X[j, i] = self._convertYesToInt(X[j, i])
        return X


    def convertStringToFloat(self, X, feature_headers):
        for i, h in enumerate(feature_headers):
            for j in xrange(X.shape[0]):
                X[j, i] = self._num(X[j, i])
        return X


    def _num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)


if __name__== "__main__":
    main()
