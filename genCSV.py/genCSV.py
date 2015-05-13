#!/usr/bin/env python3
# MAIN

class GenerateMetrics:
    @staticmethod
    def determine_testcases(command_line_args):
        import json
        import os
        config_file = os.path.dirname(command_line_args[0]) + 'config.json'
        # With open is a secure way to open and close a file. Using with we don't have to implicitly close the file as it does it on its own
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # finds the default value for the order number to search files in the json file
            dir_structure = json_data['Search_Key']["Order"]["default"]

        print("number of arguments received:", (len(command_line_args)-1))
        print(command_line_args)
        test_cases_list = []
        print("### Finding the required testcases ###")
        # The following 4 statements/loops is how the script searches for testcases in the given arguments
        # 1 is designed for the current megatest with the duplicate directory
        if dir_structure == "1":
            for argument in command_line_args:
                # command_line_args[0] is always the name of the script so we exclude it from the search
                if argument is not command_line_args[0]:
                    first_level = [os.path.join(argument, name) for name in os.listdir(argument) if os.path.isdir(os.path.join(argument, name))]
                    for dir_names in first_level:
                        files_to_search = [os.path.join(dir_names, name) for name in os.listdir(dir_names)if os.path.isdir(os.path.join(dir_names, name))]
                        for files in files_to_search:
                            test_cases_list.append(files, config_file)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)
        # 2 is designed for megatest when the duplicate testcase folder is removed
        elif dir_structure == "2":
            for argument in command_line_args:
                if argument is not command_line_args[0]:
                    files_to_search = [os.path.join(argument, name) for name in os.listdir(argument)if os.path.isdir(os.path.join(argument, name))]
                    for files in files_to_search:
                        test_cases_list.append(files)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)
        # 3 is for searching by the testcase itself
        elif dir_structure == "3":
            for argument in command_line_args:
                if argument is not command_line_args[0]:
                    test_cases_list.append(argument)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)
        # 4 is for searching by the date folder and three levels into that
        elif dir_structure == "4":
            for argument in command_line_args:
                if argument is not command_line_args[0]:
                    first_level = [os.path.join(argument, name) for name in os.listdir(argument)if os.path.isdir(os.path.join(argument, name)) if os.path.join(argument, name).endswith("runs")]
                    for dir_names in first_level:
                        second_level = [os.path.join(dir_names, name) for name in os.listdir(dir_names)if os.path.isdir(os.path.join(dir_names, name))]
                        for second_lvl_files in second_level:
                            third_level = [os.path.join(second_lvl_files, name) for name in os.listdir(second_lvl_files)if os.path.isdir(os.path.join(second_lvl_files, name))]
                            for third_lvl_files in third_level:
                                test_cases_list.append(third_lvl_files)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)
        GenerateMetrics.get_metrics(test_cases_list)

    @staticmethod
    def get_metrics(test_cases_list):
        from FindFiles import findFiles
        from GetCadenceMetrics import GetCadenceMetrics
        from GetSynopsysMetrics import GetSynopsysMetrics
        # print("### Found testcases ###")
        csv_written = False
        for test_case in test_cases_list:
            print("### Searching:", test_case)
            # default tool is synopsys
            tool = "synopsys"
            if "cadence" in test_case:
                tool = "cadence"
            elif "synopsys" in test_case:
                tool = "synopsys"
            temp_metric_collections = []
            list_of_files = findFiles.search_dir(test_case, tool)
            if tool is "cadence":
                temp_metric_collections = GetCadenceMetrics.get_cadence_metrics(list_of_files, test_case, tool)
            else:
                temp_metric_collections = GetSynopsysMetrics.get_synopsys_metrics(list_of_files, test_case, tool)

            csv_written = GenerateMetrics.generate_csv(temp_metric_collections, test_case, csv_written)

    @staticmethod
    def generate_csv(temp_metric_collections, test_case, csv_written):
        import csv
        names, values = [], []
        name = 0
        value = 1

        print("temp_metric_collection found: ")
        for temp_metric_collection in temp_metric_collections:
            temp_metric_list = tuple(temp_metric_collection)
            for metric in range(len(temp_metric_list)):
                print(temp_metric_list[metric])
                # Names and values are concatenated into a string in order to have horizontal column
                names += [temp_metric_list[metric][name]]
                values += [temp_metric_list[metric][value]]

        if csv_written is False:
            csv_written = True
            # Creates a csv with the first testcase only
            # The 'wt' argument in the following "with open" statement means that if the file doesnt exist then it will be
            # and if one does exist it will be completely overwritten
            with open(r'Regr_Suite_Runs_Comparison_Data.csv', 'wt') as my_file:
                writer = csv.writer(my_file, lineterminator='\n')
                writer.writerow(names)
                writer.writerow(values)
            my_file.close()
            print('Regr_Suite_Runs_Comparison_Data.csv created with %s' % test_case)
        else:
            # The 'a' argument in the following "with open" statement means that if the file does exist then it will be appended to
            with open(r'Regr_Suite_Runs_Comparison_Data.csv', 'a') as my_file:
                writer = csv.writer(my_file, lineterminator='\n')
                writer.writerow(values)
            my_file.close()
            print('Regr_Suite_Runs_Comparison_Data.csv appended with %s' % test_case)
        return csv_written

import sys

# sys.argv is a list of arguments passed in by command line / terminal
# sys_args is a list made to be a copy of sys.argv
sys_args = sys.argv
# GenerateMetrics is a class  , and determin_testcases is the method, in which it passes the list sys_args
GenerateMetrics.determine_testcases(sys_args)