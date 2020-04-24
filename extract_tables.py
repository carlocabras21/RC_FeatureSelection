from utils import *

datasets = ["acq", "money", "corn"]
percents = [1, 2, 5]

for dataset in datasets:
    print "Dataset: " + dataset + "\n"
    for percent in percents:

        # first of all, read the baseline
        test_names, specificity, recall, precision, f_measure, g_mean, mcc = \
            extract_data_from_folder("raw_data/raw_" + dataset + "_baseline")

        # then read the test files and append the results
        folder = "raw_data/raw_" + dataset + "_" + str(percent)
        results = extract_data_from_folder(folder)
        test_names  += results[0]
        specificity += results[1]
        recall      += results[2]
        precision   += results[3]
        f_measure   += results[4]
        g_mean      += results[5]
        mcc         += results[6]

        print_data(dataset, percent, test_names, specificity, recall, precision, f_measure, g_mean, mcc,
                   print_summary=True, write_on_file=True)

    # finally, print the tests without Feature Selection
    test_names, specificity, recall, precision, f_measure, g_mean, mcc = \
        extract_data_from_folder("raw_data/raw_" + dataset + "_baseline")

    results = extract_data_from_folder("raw_data/raw_" + dataset + "_no_FS")
    test_names  += results[0]
    specificity += results[1]
    recall      += results[2]
    precision   += results[3]
    f_measure   += results[4]
    g_mean      += results[5]
    mcc         += results[6]

    print_data(dataset, 100, test_names, specificity, recall, precision, f_measure, g_mean, mcc,
               print_summary=True, write_on_file=True)

    print "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * " \
          "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * " \
          "* * * * * * * * * * * * * * * * * * * * * * * * * * *\n\n\n"
