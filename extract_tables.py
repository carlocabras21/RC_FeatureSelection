from utils import *
import os

# initialize the lists
n_tests = 12
specificity = [[0, 0, 0, 0, 0]] * n_tests
recall      = [[0, 0, 0, 0, 0]] * n_tests
precision   = [[0, 0, 0, 0, 0]] * n_tests
f_measure   = [[0, 0, 0, 0, 0]] * n_tests
g_mean      = [[0, 0, 0, 0, 0]] * n_tests

# first of all, read the baseline
specificity[0], recall[0], precision[0], f_measure[0], g_mean[0] = extract_baseline

# index of the 4 test files  
i = 0

# index of tests, where 0 is baseline, 1 is FS,  ecc.
i_test = 1

fs_method = "ReliefF"
folder = "raw_data_" + fs_method

files = os.listdir(folder)

if not are_files_correct(files):
    exit("Exit: not enough files in folder. There are missing tests.")

files.sort()

for file_name in files:
    print file_name, i_test
    specificity[i_test][i], recall[i_test][i], precision[i_test][i], f_measure[i_test][i], g_mean[i_test][i] = \
        extract_data_from_file(folder + '/' + file_name, fs_method)

    if i == 3:
        # compute the average
        specificity [i_test][4] = round( avg(specificity [i_test][0:4]), 3)
        recall      [i_test][4] = round( avg(recall      [i_test][0:4]), 3)
        precision   [i_test][4] = round( avg(precision   [i_test][0:4]), 3)
        f_measure   [i_test][4] = round( avg(f_measure   [i_test][0:4]), 3)
        g_mean      [i_test][4] = round( avg(g_mean      [i_test][0:4]), 3)

        i_test += 1

    i = (i + 1) % 4

print_all_data(specificity, recall, precision, f_measure, g_mean)
