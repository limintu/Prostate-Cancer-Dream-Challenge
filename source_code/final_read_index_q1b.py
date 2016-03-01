
import numpy as np
import csv

from tools import save_result_no_text
from adaboost_read_index import Adaboost


####################################################################3333

def run():
    training_data = 'dataset/dream/training_Q1b.csv'
    X_train, y_train, delta_train = _training_data(training_data)

    test_data = 'dataset/dream/test_Q1b.csv'
    X_test = _test_data(test_data)

    n_iter = 10
    r_index = 1
    # Create adaboost object
    #a = Adaboost('linear', r_index, "final_random_q1b.txt")
    a = Adaboost('decision_tree', r_index, "final_random_q1b.txt")
    a.fit(X_train, y_train, delta_train, n_iter)
    result = a.predict(X_test, mode='mean')
    result_file = 'result_q1b'
    save_result_no_text(result, result_file)
    return


def _training_data(input_file):
    """
    Preprocess the data set of dream challenge

    """
    X = []
    y = []
    delta = []
    with open(input_file) as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            y.append(int(row[-1]))
            delta.append(int(row[-2]))
            X.append([float(i)for i in row[:-4]]+[float(row[-4])]+[float(row[-3])])
    return np.array(X), np.array(y), np.array(delta)


def _test_data(input_file):
    """
    Preprocess the data set of dream challenge

    """
    X = []
    with open(input_file) as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            X.append([float(i)for i in row[:-4]]+[float(row[-4])]+[float(row[-3])])
    return np.array(X)


def main():
    run()
    return


if __name__== "__main__":
    main()
