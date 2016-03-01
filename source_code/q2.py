
#import rpy2.robjects as ro

def score_q2():
    r_source = ro.r['source']
    r_source("score.R")
    ro.r('result <- hello()')
    ccc = ro.r('result')
    #r_hello = ro.globalenv['hello']
    #r('hello')
    print type(ccc)
    return


