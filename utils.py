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
    if len(files) < 11:  # 11 tests
        return False
    return True


# returns the data vectors. If fs_method = "", we do not check if the method is correct
def extract_data_from_file(file_name):

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
    return extract_data_from_file("raw_baseline/0_baseline.txt")


def print_data(percent, file_names, specificity, recall, precision, f_measure, g_mean, print_summary=True,
               write_on_file=False):
    f = None

    title = "Percentage of selected features: " + str(percent) + "%\n"
    print title

    if write_on_file:
        if percent == 1:
            f = open("results.txt", "w")
        else:
            f = open("results.txt", "a")

        f.write(title + "\n")

    if print_summary:
        header = ["-"] + file_names

        # extract the average values
        rows = [specificity, recall, precision, f_measure, g_mean]

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

    if write_on_file:
        f.close()

        # print "#" + "\t" + str(files)[2:-2].replace("', '", "\t")
        # print [x[4] for x in specificity]
