from utils import *
import os

percents = [1, 2, 5]
for percent in percents:
    folder = "raw_" + str(percent)

    files = os.listdir(folder)

    if not are_files_correct(files):
        exit("Exit: not enough files in folder. There are missing tests.")

    files.sort()

    # initialize the lists
    specificity = []
    recall      = []
    precision   = []
    f_measure   = []
    g_mean      = []
    for _ in range (0, 12):
        specificity .append(0)
        recall      .append(0)
        precision   .append(0)
        f_measure   .append(0)
        g_mean      .append(0)

    # first of all, read the baseline
    specificity[0], recall[0], precision[0], f_measure[0], g_mean[0] = extract_baseline()

    # index of tests, where 0 is baseline, 1 is FS,  ecc.
    i_test = 1

    for file_name in files:
        specificity[i_test], recall[i_test], precision[i_test], f_measure[i_test], g_mean[i_test] = \
            extract_data_from_file(folder + '/' + file_name)
        i_test += 1

    formatted_file_names = ["Baseline"]
    # noinspection PyRedeclaration
    i = 0
    for f in files:
        formatted_file_name = f[3:-4].replace("_", " + ")
        formatted_file_names.append(formatted_file_name)
        i += 1

    print_data(percent, formatted_file_names, specificity, recall, precision, f_measure, g_mean, print_summary=True,
               write_on_file=True)






















