from operator import sub
from math import pow, sqrt
import numpy as np


def score_q2(predTime, LKADT_P, DEATH):
    """
    Compute the q1b subchallenge score.

    Parameters
    ----------
    predTime: list, length = n_elements

    LKADT_P: list, length = n_elements

    DEATH: list, length = n_elements

    Returns
    -------
    score: number

    """
    x = data_death(LKADT_P, DEATH)
    y = data_death(predTime, DEATH)
    return (sqrt(sum([pow(i,2) for i in map(sub, x, y)])))/float(len(x))
    #return (sqrt(sum([pow(i,2) for i in [x1-x2 for (x1, x2) in zip(x,y)]])))/float(len(x))
    #return (sqrt(sum([pow(i,2) for i in list(np.array(x) - np.array(y))])))/float(len(x))


def data_death(data_list, death_list):
    """
    Return elements that is uncensored.

    Parameters
    ----------
    data_list: list, length = n_elements

    death_list: list, length = n_elements

    Returns
    output: list, length = n_death_elements

    -------

    """
    return [data_list[i] for i, v in enumerate(death_list) if v == 1]

