
import numpy as np
import csv

from adaboost_seed import Adaboost


########################################################################

def run():
    training_data = 'dataset/dream/training_Q1b.csv'
    X_train, y_train, delta_train = _data(training_data)

    #test_data = 'dataset/dream/test_Q1b.csv'
    #X_test, y_test, delta_test = _data(test_data)

    n_iter = 10
    # Create adaboost object
    a = Adaboost('decision_tree', "final_random_q1b.txt")
    #a = Adaboost('random_forest', "final_random_q1b.txt")
    a.fit(X_train, y_train, delta_train, n_iter)
    #result = a.predict(X_test, mode='mean')
    #result_file = 'final_q1b'
    #save_result_no_text(result, result_file)
    return


def _data(input_file):
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
            X.append([int(i)for i in row[:-4]]+[float(row[-4])]+[int(row[-3])])
    return np.array(X), np.array(y), np.array(delta)



def main():
    ### For adaboost_seed.py
    file = open("final_random_q1b.txt", "w+")
    file.close()
    ###

    run()
    return


if __name__== "__main__":
    main()
