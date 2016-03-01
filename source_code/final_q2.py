import numpy as np
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingClassifier
#from math import log

from tools import save_result_no_text
from preprocessing_q2 import X_processor
from ricky.case import case
from ricky.ensemble import tolist, ensemble
from adaboost_seed_q2 import Adaboost_q2
from monsss.merge import merge
from monsss.readcsv import readcsv


def adaboost_data_index_list(X, y, delta, z):
    xp = X_processor()
    X, y, delta, z, data_index_list = xp.select_ENDTRS_C_data(X, y, delta, z)
    return data_index_list


def selected_train_adaboost(train_index, data_index_list):
    """

    Parameters
    ----------
    data_index_list : list
        The list of data index in which the value of the "ENDTRS_C" feature is "AE" or "possible_AE"
    """
    return [i for i in train_index if i in data_index_list]


###########################################################################3

def predict_with_adaboost(X_train, y_train, delta_train, X_test):
    print 'predict_with_adaboost'

    n_iter = 10

    # Create adaboost object
    #a = Adaboost_q2('linear')
    #a = Adaboost_q2('random_forest')
    a = Adaboost_q2('decision_tree', "randomq2.txt", 100)
    a.fit(X_train, y_train, delta_train, n_iter)
    return a.predict(X_test, mode='mean')


def predict_with_classifier1(X_train, delta_train, X_test):
    rf = case(delta_train, X_train, 1)
    return rf.predict_proba(X_test)[:,1]


def predict_with_classifier2(X_train, delta_train, z_train, X_test):
    delta_train = merge(np.array(["ENDTRS_C"]), z_train)
    rf = case(delta_train, X_train, 2)
    return rf.predict_proba(X_test)[:,1]


def predict_with_gradientboostingclassifier(X_train, delta_train, z_train, X_test):
    #rf = GradientBoostingClassifier()
    #rf.fit(X_train,delta_train)
    delta_train = merge(np.array(["ENDTRS_C"]), z_train)
    rf = case(delta_train, X_train, 3)

    return rf.predict_proba(X_test)[:,1]


def _training_data(training_file):
    X = readcsv(training_file)
    origin_file = 'dataset/dream/CoreTable_training.csv'
    xp = X_processor()
    y, delta, z = xp.extractDependent(origin_file)
    delta = xp.tackle_DISCONT_missing(y, delta, z)
    X, y, delta, z = xp.tackle_ENTRT_PC_missing(X, y, delta, z)
    y = y.astype(np.int)
    delta = delta.astype(np.int)
    return X, y, delta, z


def _test_data(test_file):
    X = readcsv(test_file)
    return X


def run():
    training_file = 'dataset/dream/Train_afterAll.csv' ### only feature data
    X_train, y_train, delta_train, z_train = _training_data(training_file)
    test_file = 'dataset/dream/Test_afterAll.csv' ### only feature data
    X_test = _test_data(test_file)

    ### rank of test data by classifier1
    rank_c1 = predict_with_classifier1(X_train, delta_train, X_test)

    ### rank of test data by classifier2
    rank_c2 = predict_with_classifier2(X_train, delta_train, z_train, X_test)

    ### rank of test data by gradient boosting classifier
    rank_gc = predict_with_gradientboostingclassifier(X_train, delta_train, z_train, X_test)

    #train_index = selected_train_adaboost(train_index, data_index_list)
    #X_train_ad = X[train_index]
    #y_train_ad = y[train_index]
    #delta_train_ad = delta[train_index]
    #z_train_ad = z[train_index]

    ### rank of test data by adaboost
    #rank_ad = predict_with_adaboost(X_train_ad, y_train_ad, delta_train_ad, X_test)
    #rank_ad = [1/float(j) for j in rank_ad]

    ### rank of test data by regressor
    #rank_rg = predict_with_regressor(X_train_ad, y_train_ad, X_test, 1) ### 1:random forest regressor, 2: decision tree regressor
    #rank_rg = [1/float(j) for j in rank_rg]

    all_rank = DataFrame()
    all_rank = tolist(all_rank, "classifier1", rank_c1)
    all_rank = tolist(all_rank, "classifier2", rank_c2)
    all_rank = tolist(all_rank, "gradient boosting classifier", rank_gc)
    #all_rank = tolist(all_rank, "adaboost", rank_ad)
    #all_rank = tolist(all_rank, "regressor", rank_rg)

    ### "average", "minimum", "maximum", "median", "trimmed mean"
    result = ensemble(all_rank, "average")
    predicted_class = []
    for i in result:
        if i > 0.5:
            predicted_class.append(1)
        else:
            predicted_class.append(0)
    final_result = [(result[i], predicted_class[i]) for i in xrange(len(result))]
    result_file = 'result_q2'
    save_result_no_text(final_result, result_file)
    return


def main():
    run()
    return


if __name__== "__main__":
    main()
