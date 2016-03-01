

def save_result_no_text(data_list, result_file):
    """
    To save result in the result_file.
    Input:
        data_list: the result data to be saved
        result_file: the file that result is saved.
    """
    with open(result_file, 'a+') as f:
        for i in xrange(len(data_list)):
            f.write(str(data_list[i])+'\n')
    return


def save_result(text_list, data_list, result_file):
    """
    To save result in the result_file.
    Input:
        text_list: the line shows the text of the result, without the symbol ':'
        data_list: the result data to be saved
        result_file: the file that result is saved.
    """
    with open(result_file, 'a+') as f:
        l = len(text_list)
        if l == len(data_list):
            for i in xrange(l):
                if (text_list[i] is not None) and (data_list[i] is not None):
                    f.write(text_list[i]+':'+'\n')
                    f.write(str(data_list[i])+'\n')
                else:
                    raise Exception('Lost some text or data!')
    return

