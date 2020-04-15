from utils import *
import os

# fs_method = "InfoG"
fs_method = "ReliefF"
folder = "raw_data_" + fs_method

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
    specificity .append([0, 0, 0, 0, 0])
    recall      .append([0, 0, 0, 0, 0])
    precision   .append([0, 0, 0, 0, 0])
    f_measure   .append([0, 0, 0, 0, 0])
    g_mean      .append([0, 0, 0, 0, 0])


# first of all, read the baseline
specificity[0], recall[0], precision[0], f_measure[0], g_mean[0] = extract_baseline()

# index of tests, where 0 is baseline, 1 is FS,  ecc.
i_test = 1

# index of the 4 test files
# noinspection PyRedeclaration
i = 0
for file_name in files:

    specificity[i_test][i], recall[i_test][i], precision[i_test][i], f_measure[i_test][i], g_mean[i_test][i] = \
        extract_data_from_file(folder + '/' + file_name)

    if i == 3:
        # compute the average
        specificity [i_test][4] = round( avg(specificity [i_test][0:4]), 3)
        recall      [i_test][4] = round( avg(recall      [i_test][0:4]), 3)
        precision   [i_test][4] = round( avg(precision   [i_test][0:4]), 3)
        f_measure   [i_test][4] = round( avg(f_measure   [i_test][0:4]), 3)
        g_mean      [i_test][4] = round( avg(g_mean      [i_test][0:4]), 3)

        i_test += 1

    i = (i + 1) % 4

formatted_file_names = ["Baseline"]
# noinspection PyRedeclaration
i = 0
for f in files:
    if i % 4 == 0:
        formatted_file_name = f[3:-6].replace("_", " + ")
        formatted_file_names.append(formatted_file_name)
    i = (i + 1) % 4

print_data(fs_method, formatted_file_names, specificity, recall, precision, f_measure, g_mean, print_summary=True,
           write_on_file=True)
