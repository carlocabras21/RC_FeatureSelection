from utils import *

percents = [1, 2, 5]
for percent in percents:

    # first of all, read the baseline
    test_names, specificity, recall, precision, f_measure, g_mean, mcc = \
        extract_data_from_folder("raw_baseline")

    # then read the test files and append the results
    folder = "raw_" + str(percent)
    results = extract_data_from_folder(folder)
    test_names  += results[0]
    specificity += results[1]
    recall      += results[2]
    precision   += results[3]
    f_measure   += results[4]
    g_mean      += results[5]
    mcc         += results[6]

    print_data(percent, test_names, specificity, recall, precision, f_measure, g_mean, mcc,
               print_summary=True, write_on_file=True)


# finally, print the tests without Feature Selection
test_names, specificity, recall, precision, f_measure, g_mean, mcc = \
    extract_data_from_folder("raw_baseline")

results = extract_data_from_folder("raw_no_FS")
test_names  += results[0]
specificity += results[1]
recall      += results[2]
precision   += results[3]
f_measure   += results[4]
g_mean      += results[5]
mcc         += results[6]

print_data(100, test_names, specificity, recall, precision, f_measure, g_mean, mcc,
           print_summary=True, write_on_file=True)
