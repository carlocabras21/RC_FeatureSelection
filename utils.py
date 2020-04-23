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


# returns the data vectors
def extract_data_from_file(file_name):

    with open(file_name) as f:
        # e.g.:  raw_data/raw_acq_1/02_RU(3:1)_FS.txt  --->  RU(3:1) + FS
        test_name = file_name.split("/")[2][3:-4].replace("_", " + ")

        ''' line example:
        === Detailed Accuracy By Class ===

                     TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                     0,997    0,815    0,933      0,997    0,964      0,379    0,932     0,991     Other
                     0,185    0,003    0,852      0,185    0,305      0,379    0,932     0,613     Uterus
        '''

        line = f.readline()
        while '=== Detailed Accuracy By Class ===' not in line:  # find this line
            line = f.readline()

        # go to the first line with numbers
        f.readline()
        f.readline()
        line = f.readline()
        specificity = float(line.split()[3].replace(',', '.'))

        line = f.readline()
        recall      = float(line.split()[3].replace(',', '.'))
        precision   = float(line.split()[2].replace(',', '.'))
        f_measure   = float(line.split()[4].replace(',', '.'))
        g_mean      = round(math.sqrt(specificity * recall), 3)
        mcc         = float(line.split()[5].replace(',', '.'))

    return test_name, specificity, recall, precision, f_measure, g_mean, mcc


def extract_baseline():
    return extract_data_from_file("raw_baseline/0_baseline.txt")


# prints data on screen and write it to results.txt
def print_data(dataset, percent, test_names, specificity, recall, precision, f_measure, g_mean, mcc,
               print_summary=True, write_on_file=False):
    f = None

    if percent == 100:
        title = "No Feature Selection\n"
    else:
        title = "Percentage of selected features: " + str(percent) + "%\n"

    print title

    if write_on_file:
        if dataset == "acq" and percent == 1:  # open in write mode only if it's the first dataset
            f = open("results.txt", "w")
        else:  # otherwise, append the results
            f = open("results.txt", "a")

        if percent == 1:  # write the dataset name only the first time for each dataset
            f.write("Dataset: " + dataset + "\n\n")

        f.write(title + "\n")

    header  = ["-"] + test_names
    rows    = [ specificity,   recall,   precision,   f_measure,   g_mean,   mcc]
    metrics = ["Specificity", "Recall", "Precision", "F-Measure", "G-Mean", "MCC"]

    if print_summary:
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

        if percent == 100:
            f.write("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * " +
                    "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * " +
                    "* * * * * * * * * * * * * * * * * * * * * * * * * * *\n\n\n")

        f.close()


# extract all the metrics data from the tests in the folder
def extract_data_from_folder(folder):
    # read all the files and count them
    files = os.listdir(folder)
    files.sort()

    # initialize the lists
    test_names  = []
    specificity = []
    recall      = []
    precision   = []
    f_measure   = []
    g_mean      = []
    mcc         = []

    # extract data from files
    for file_name in files:
        results = extract_data_from_file(folder + '/' + file_name)
        test_names  += [results[0]]
        specificity += [results[1]]
        recall      += [results[2]]
        precision   += [results[3]]
        f_measure   += [results[4]]
        g_mean      += [results[5]]
        mcc         += [results[6]]

    return test_names, specificity, recall, precision, f_measure, g_mean, mcc
