import math
import os


def avg(lst):  # returns the average of a list
    return sum(lst) / len(lst)


def string_from_lst_name(lst, name):
    s = name + '\t'
    for el in lst:
        s += str('%.3f' % el).replace('.', ',') + '\t'
    return s


def print_vector(lst, name):  # print the list like a tabular row
    print string_from_lst_name(lst, name)


def write_vector_on_file(f, lst, name):  # print the list like a tabular row
    s = string_from_lst_name(lst, name) + "\n"
    f.write(s)


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
    recall      = [0, 0, 0, 0, 0]
    precision   = [0, 0, 0, 0, 0]
    f_measure   = [0, 0, 0, 0, 0]
    g_mean      = [0, 0, 0, 0, 0]

    # index of the 4 test files
    i = 0
    folder = "raw_data_baseline"

    files = os.listdir(folder)

    files.sort()

    for file_name in files:
        specificity[i], recall[i], precision[i], f_measure[i], g_mean[i] = \
            extract_data_from_file(folder + '/' + file_name, "")

        i += 1

    specificity[4] = round(avg(specificity[0:4]), 3)
    recall[4]      = round(avg(recall[0:4])     , 3)
    precision[4]   = round(avg(precision[0:4])  , 3)
    f_measure[4]   = round(avg(f_measure[0:4])  , 3)
    g_mean[4]      = round(avg(g_mean[0:4])     , 3)

    return specificity, recall, precision, f_measure, g_mean


def print_data(fs_method, file_names, specificity, recall, precision, f_measure, g_mean,
               print_summary=True, print_all_tables=True, write_on_file=False):
    f = None

    print fs_method + "\n"

    if write_on_file:
        f = open("results_" + fs_method + ".txt", "w")
        f.write(fs_method + "\n\n")

    if print_summary:
        header = ["-"] + file_names

        # extract the average values
        rows = [[x[4] for x in specificity],
                [x[4] for x in recall],
                [x[4] for x in precision],
                [x[4] for x in f_measure],
                [x[4] for x in g_mean]]

        metrics = ["Specificity", "Recall", "Precision", "F-Measure", "G-Mean"]

        # first print the titles
        for j in range(0, len(header)):
            print("%15s" % header[j]),
        print ""

        # then print the values
        for i in range(0, len(rows)):
            print("%15s" % metrics[i]),

            for j in range(0, len(rows[i])):
                # print every number in the format e.g. 0,350
                print("%15s" % str('%.3f' % float(rows[i][j])).replace('.', ',')),
            print ''

        print "\n\n"

        if write_on_file:
            # first write the titles
            for j in range(0, len(header)):
                f.write("%15s" % header[j]),
            f.write("\n")

            # then write the values
            for i in range(0, len(rows)):
                f.write("%15s" % metrics[i])

                for j in range(0, len(rows[i])):
                    # write every number in the format e.g. 0,350
                    f.write("%15s" % str('%.3f' % float(rows[i][j])).replace('.', ','))
                f.write("\n")

            f.write("\n\n")

    for i_test in range(0, len(file_names)):
        if print_all_tables:
            print file_names[i_test]

            print '\t' + '#' + '\t' + ' 1' + '\t' + ' 2' + '\t' + ' 3' + '\t' + ' 4' + '\t' + 'Average'

            print_vector(specificity[i_test], 'Specificity')
            print_vector(recall[i_test],      'Recall     ')
            print_vector(precision[i_test],   'Precision  ')
            print_vector(f_measure[i_test],   'F-measure  ')
            print_vector(g_mean[i_test],      'G-mean     ')

            print "\n\n"

        if write_on_file and print_all_tables:
            f.write(
                file_names[i_test] + "\n" +
                '\t' + '#' + '\t\t  ' + '1' + '\t\t  ' + '2' + '\t\t  ' + '3' + '\t\t  ' + '4' + '\t\t' + 'Average\n')

            write_vector_on_file(f, specificity[i_test], 'Specificity')
            write_vector_on_file(f, recall[i_test], 'Recall     ')
            write_vector_on_file(f, precision[i_test], 'Precision  ')
            write_vector_on_file(f, f_measure[i_test], 'F-measure  ')
            write_vector_on_file(f, g_mean[i_test], 'G-mean     ')

            f.write("\n\n")

    if write_on_file:
        f.close()

        # print "#" + "\t" + str(files)[2:-2].replace("', '", "\t")
        # print [x[4] for x in specificity]
