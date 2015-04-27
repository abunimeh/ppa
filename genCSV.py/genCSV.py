#!/usr/bin/env python3
# MAIN
import csv
import json
import sys
import os
from FindFiles import findFiles
from GetCadenceMetrics import GetCadenceMetrics
from GetSynopsysMetrics import GetSynopsysMetrics


with open(r'C:\dev\intel\ppa\genCSV.py\config.json', 'r') as f:
    json_data = json.load(f)
    # finds the default value for the order number to search files in the json file
    dir_structure = json_data['Search_Key']["Order"]["default"]
print(dir_structure)
print("number of arguments received:", (len(sys.argv)-1))
print(sys.argv)
test_cases_list = []
arg_list = []
if dir_structure == "1":
    for argument in sys.argv:
        if argument is not sys.argv[0]:
            first_level = [os.path.join(argument, name) for name in os.listdir(argument)if os.path.isdir(os.path.join(argument, name))]
            for dir_names in first_level:
                files_to_search = [os.path.join(dir_names, name) for name in os.listdir(dir_names)if os.path.isdir(os.path.join(dir_names, name))]
                for files in files_to_search:
                    test_cases_list.append(files)
elif dir_structure == "2":
    for argument in sys.argv:
        if argument is not sys.argv[0]:
            files_to_search = [os.path.join(argument, name) for name in os.listdir(argument)if os.path.isdir(os.path.join(argument, name))]
            for files in files_to_search:
                test_cases_list.append(files)
elif dir_structure == "3":
    for argument in sys.argv:
        if argument is not sys.argv[0]:
            print("ARGS", argument)
            test_cases_list.append(argument)



csv_file_exist = 0
# default tool is synopsys
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
        temp = GetCadenceMetrics.get_cadence_metrics(list_of_files, test_case, tool)
    elif tool == "synopsys":
        temp = GetSynopsysMetrics.get_synopsys_metrics(list_of_files, test_case, tool)

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
        my_file.close()
        print('Regr_Suite_Runs_Comparison_Data.csv created with %s' % test_case)
    else:
        # Appends the csv with the following testcases
        with open(r'Regr_Suite_Runs_Comparison_Data.csv', 'a') as my_file:
            writer = csv.writer(my_file, lineterminator='\n')
            writer.writerow(values)
        my_file.close()
        print('Regr_Suite_Runs_Comparison_Data.csv appended with %s' % test_case)
