import math


def avg(lst):  # returns the average of a list
    return sum(lst) / len(lst)


def print_vector(lst, name):  # print the list like a tabular row
    print name + '\t' + \
            str(lst[0]).replace('.', ',') + '\t' + \
            str(lst[1]).replace('.', ',') + '\t' + \
            str(lst[2]).replace('.', ',') + '\t' + \
            str(lst[3]).replace('.', ',') + '\t' + \
            str(round(avg(lst), 3)).replace('.', ',')


# check if there are all the test files
def are_files_correct(files):
    if len(files) < 44:  # 4 runs for each of the 11 test
        return False
    return True


# returns the data vectors. If fs_method = "", we do not check if the method is correct
def extract_data_from_file(file_name, fs_method):
    # with this assignment, if fs_method = "" then the variable is always True.
    is_fs_method_right = fs_method == ""

    with open(file_name) as f:

        ''' line example:
        === Detailed Accuracy By Class ===

                     TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                     0,997    0,815    0,933      0,997    0,964      0,379    0,932     0,991     Other
                     0,185    0,003    0,852      0,185    0,305      0,379    0,932     0,613     Uterus
        '''

        line = f.readline()
        while '=== Detailed Accuracy By Class ===' not in line:  # find this line
            line = f.readline()
            if fs_method in line:
                is_fs_method_right = True

        # exit if we have different tests from the ones in the folder
        if not is_fs_method_right:
            exit("File " + file_name + " refers to a different test then " + fs_method)

        # go to the first line with numbers
        f.readline()
        f.readline()
        line = f.readline()
        specificity = float(line.split()[3].replace(',', '.'))

        line = f.readline()
        recall = float(line.split()[3].replace(',', '.'))
        precision = float(line.split()[2].replace(',', '.'))
        f_measure = float(line.split()[4].replace(',', '.'))
        g_mean = round(math.sqrt(specificity * recall), 3)

    return specificity, recall, precision, f_measure, g_mean


def extract_baseline():
    # initialize the lists
    specificity = [0, 0, 0, 0, 0]
    recall = [0, 0, 0, 0, 0]
    precision = [0, 0, 0, 0, 0]
    f_measure = [0, 0, 0, 0, 0]
    g_mean = [0, 0, 0, 0, 0]

    # index of the 4 test files
    i = 0
    folder = "raw_data_baseline"

    files = os.listdir(folder)

    files.sort()

    for file_name in files:
        specificity[i], recall[i], precision[i], f_measure[i], g_mean[i] = \
            extract_data_from_file(folder + '/' + file_name, "")

        i += 1

    specificity[4] = avg(specificity[0:4])
    recall[4] = avg(recall[0:4])
    precision[4] = avg(precision[0:4])
    f_measure[4] = avg(f_measure[0:4])
    g_mean[4] = avg(g_mean[0:4])

    return specificity, recall, precision, f_measure, g_mean
    #
    # print '\t' + '#' + '\t' + ' 1' + '\t' + ' 2' + '\t' + ' 3' + '\t' + ' 4' + '\t' + 'Average'
    # print_vector(specificity, 'Specificity')
    # print_vector(recall, 'Recall     ')
    # print_vector(precision, 'Precision  ')
    # print_vector(f_measure, 'F-measure  ')
    # print_vector(g_mean, 'G-mean     ')


def print_all_data(specificity, recall, precision, f_measure, g_mean):
    pass


























