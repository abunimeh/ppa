#!/usr/bin/env python3
# MAIN
import csv
import sys
from FindFiles import findFiles
from GetCadenceMetrics import GetCadenceMetrics
from GetSynopsysMetrics import GetSynopsysMetrics

#from OtherMetricClass import OtherMetricClass

print("number of arguments received:", (len(sys.argv)-1))
test_cases_list = []
for argument in sys.argv:
    if argument is not sys.argv[0]:
        print(argument)
        test_cases_list.append(argument)

csv_file_exist = 0
tool = "synopsys"
for test_case in test_cases_list:
    print("### Searching:", test_case)
    if "cadence" in test_case:
        tool = "cadence"
    elif "synopsys" in test_case:
        tool = "synopsys"
    temp = []
    list_of_files = findFiles.search_dir(test_case, tool)
    found_tool_version = 0
    if tool == "cadence":
        temp = GetCadenceMetrics.get_cadence_metrics(list_of_files, test_case)
    elif tool == "synopsys":
        temp = GetSynopsysMetrics.get_synopsys_metrics(list_of_files, test_case)
    # else:
    #     other_metrics = other_metric_class.search_file(file)
    #     metricNames.append(other_metrics)

    names, values = [], []

    print("metrics found: ")
    for metrics in temp:
        metric = tuple(metrics)
        for name in range(len(metric)):
            print(metric[name])
            # Names and values are concatenated into a string in order to have horizontal column
            names += [metric[name][0]]
            values += [metric[name][1]]

    if csv_file_exist == 0:
        csv_file_exist = 1
        # Creates a csv with the first testcase
        with open(r'Regr_Suite_Runs_Comparison_Data.csv', 'wt') as my_file:
            writer = csv.writer(my_file, lineterminator='\n')
            writer.writerow(names)
            writer.writerow(values)
            #writer.writerow(' ')
        my_file.close()
        print('Regr_Suite_Runs_Comparison_Data.csv created with %s' % test_case)
    else:
        # Appends the csv with the following testcases
        with open(r'Regr_Suite_Runs_Comparison_Data.csv', 'a') as my_file:
            writer = csv.writer(my_file, lineterminator='\n')
            #writer.writerow(names)
            writer.writerow(values)
            #writer.writerow(' ')
        my_file.close()
        print('Regr_Suite_Runs_Comparison_Data.csv appended with %s' % test_case)
