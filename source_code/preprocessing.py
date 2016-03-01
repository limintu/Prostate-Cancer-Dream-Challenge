
import numpy as np
#from mylib.common import file_len


def split_mtlr_dataset(input_set, delimiter, n_features):
    """
    To split dataset into X, y and delta sets.

    Parameters
    ----------
    Input_set : input mtlr dataset

    delimiter : delimiter: the delimiter that separates the elements of a dataline. If delimiter is None, it means runs of consecutive whitespace are regarded as a single separator.

    Returns
    -------
        X : numpy array, shape = [n_samples, n_features]
            Training data

        y : numpy array, shape = [n_samples,]
            Target values

        delta : numpy array, shape = [n_samples,]
            Censor indicator, 1 : censored, 0 : uncensored

    """
    #n_samples = file_len(input_set)
    with open(input_set)as f:
        X = []
        y = []
        delta = []
        for line in f:
            line_parts = line.rstrip('\n').split(delimiter)
            y.append(float(line_parts[0]))
            delta.append(int(line_parts[1]))
            X.append([float(i.split(':')[1]) for i in line_parts[2:]])
    return np.array(X), np.array(y), np.array(delta)
