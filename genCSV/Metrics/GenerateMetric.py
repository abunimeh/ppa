__author__ = ''


class GenerateMetric:
    @staticmethod
    def determine_testcases(command_line_args):

        test_cases = []
        test_case_args = GenerateMetric.trim_argument_list(command_line_args)
        dir_structure = GenerateMetric.get_directory_search_key()

        print("Number locations to search:", (len(test_case_args)))
        print("Locations:", test_case_args)
        print()
        print("### Finding the required testcases ###")
        print()

        # The following 4 statements is how the script searches for testcases in the given arguments
        # 1 is designed for the current megatest with the duplicate directory
        if dir_structure == "1":
            test_cases.extend(GenerateMetric.search_directory(test_case_args, 2))
            test_cases = list(GenerateMetric.combine_identical_testcases(test_cases))

        # 2 is designed for megatest when the duplicate testcase folder is removed
        elif dir_structure == "2":
            test_cases.extend(GenerateMetric.search_directory(test_case_args, 1))
            test_cases = list(GenerateMetric.combine_identical_testcases(test_cases))

        # 3 is for searching by the testcase itself
        elif dir_structure == "3":
            test_cases.extend(GenerateMetric.verify_test_case_directory(test_case_args))

        # 4 is for searching by the date folder and three levels into that
        elif dir_structure == "4":
            test_cases.extend(GenerateMetric.search_directory(test_case_args, 3))

        print("Found %s testcases" % len(test_cases))
        print("Testcases:", test_cases)

        GenerateMetric.get_metrics(test_cases)

    @staticmethod
    def trim_argument_list(command_line_args):
        # command_line_args[0] is always the script location so we get rid of it since we don't need it anymore
        test_case_args = command_line_args[1:len(command_line_args)]

        for test_case_arg in test_case_args:
            if test_case_arg.endswith('.json'):
                test_case_args.remove(test_case_arg)

        return test_case_args

    @staticmethod
    def get_directory_search_key():
        import json
        from FindFile import FindFiles

        config_file = FindFiles.return_config_name()
        print("My config file:", config_file)

        # With open is a secure way to open and close a file. Using with we don't have to implicitly close the file
        # as it does it on its own
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # finds the default value for the order number to search files in the json file
            dir_structure = json_data['Search_Key']["Order"]["default"]

        return dir_structure

    @staticmethod
    def search_directory(paths, directory_level):
        import os
        path_collections = []
        my_name = ""
        directory_level -= 1

        for path in paths:
            path_collection = [os.path.join(path, name) for name in os.listdir(path)if os.path.isdir(
                    os.path.join(path, name)) if os.path.join(path, name).endswith(my_name)]
            path_collections.extend(path_collection)

        if directory_level != 0:
            path_collections = GenerateMetric.search_directory(path_collections, directory_level)
        else:
            path_collections = GenerateMetric.verify_test_case_directory(path_collections)

        return path_collections

    @staticmethod
    def verify_test_case_directory(paths):
        import os
        test_case_directories = ['syn', 'apr', 'drc_lvs', 'sta', 'pv', 'ext', 'denall_reuse',
                                 'drcc', 'gden', 'HV', 'drc_IPall', 'lvs', 'drcd', 'trclvs']
        for path in paths:
            if path.endswith("fdkex_mcmm"):
                print("SKIPPED:", path)
                continue
            directories = [name for name in os.listdir(path) if os.path.isdir(os.path.join(
                           path, name)) if name in test_case_directories]
            if len(directories) == 0:
                paths.remove(path)

        return paths

    @staticmethod
    def combine_identical_testcases(test_cases):
        import os
        test_case_names = []
        new_test_cases = []

        for test_case in test_cases:
            test_case_name = os.path.basename(test_case)
            if test_case_name not in test_case_names:
                test_case_names.append(test_case_name)

        for test_case_name in test_case_names:
            temp_test_cases = []
            for test_case in test_cases:
                temp_test_case_name = os.path.basename(test_case)
                if temp_test_case_name == test_case_name:
                    temp_test_cases.append(test_case)

            new_test_cases.append(tuple(temp_test_cases))

        return new_test_cases

    @staticmethod
    def get_metrics(test_cases):
        import os
        from FindFile import FindFiles
        from Metrics.CadenceMetric import CadenceMetric
        from Metrics.SynopsysMetric import SynopsysMetric

        csv_written = False
        csv_name = FindFiles.return_csv_name()

        for test_case in test_cases:
            metrics_collections = []
            list_of_files = []

            if isinstance(test_case, (list, tuple)):
                for temp_test_case in range(len(test_case)):
                    tool = GenerateMetric.check_tool(test_case[temp_test_case])
                    list_of_files.extend(FindFiles.search_dir(test_case[temp_test_case], tool))
                test_case = test_case[0]
            else:
                tool = GenerateMetric.check_tool(test_case)
                list_of_files.extend(FindFiles.search_dir(test_case, tool))

            print("Files to be searched:")

            for file in list_of_files:
                print(file, os.path.getsize(file))

            print(len(list_of_files), "Total found")
            print()
            print("### Searching:", test_case)
            print()

            if tool is "cadence":
                metrics_collections.extend(CadenceMetric.get_cadence_metrics(list_of_files, test_case, tool))
            else:
                metrics_collections.extend(SynopsysMetric.get_synopsys_metrics(list_of_files, test_case, tool))

            csv_written = GenerateMetric.write_csv(metrics_collections, csv_written, test_case, csv_name)

        GenerateMetric.check_csv(csv_name)

    @staticmethod
    def check_tool(test_case):
        import re

        # The following regular expressions are made to find the tool for megatest testcases
        cadence_tool = re.search(r'/([a-zA-Z_]{1,3}[\d\.]+_[cC]{1})/', test_case)

        if "cadence" in test_case or cadence_tool:
            tool = "cadence"
        else:
            # default tool is synopsys
            tool = "synopsys"

        return tool

    @staticmethod
    def get_csv_values(metrics_collections, csv_written):
        metric_name = 0
        metric_value = 1
        names = []
        values = []
        metric_values = []

        print("Metrics found: ")
        for metric_pair in metrics_collections:
            # temp_metric_list = tuple(temp_metric_collection)
            print(metric_pair)
            if csv_written is False:
                names.append(metric_pair[metric_name])
                values.append(metric_pair[metric_value])
            else:
                values.append(metric_pair[metric_value])

        metric_values.append(names)
        metric_values.append(values)

        return metric_values

    @staticmethod
    def write_csv(metrics_collections, csv_written, test_case, csv_name):
        import csv

        names = 0
        values = 1
        metric_values = GenerateMetric.get_csv_values(metrics_collections, csv_written)

        if csv_written is False:
            csv_written = True
            # Creates a csv with the first testcase only
            # The 'wt' argument in the following "with open" statement means that if the file doesnt exist then it
            # will be and if one does exist it will be completely overwritten.
            try:
                with open(csv_name, 'wt') as my_file:
                    writer = csv.writer(my_file, lineterminator='\n')
                    writer.writerow(metric_values[names])
                    writer = csv.writer(my_file, lineterminator='\n', quoting=csv.QUOTE_ALL)
                    writer.writerow(metric_values[values])
                print(csv_name, 'created with', test_case)
            except IOError:
                print("### Unable to open the csv file. The file might be open in a csv reader. ###")
        else:
            try:
                # The 'a' argument in the following "with open" statement means that if the file does exist then it will be
                # appended to.
                with open(csv_name, 'a') as my_file:
                    writer = csv.writer(my_file, lineterminator='\n', quoting=csv.QUOTE_ALL)
                    writer.writerow(metric_values[values])
                print(csv_name, 'appended with', test_case)
            except IOError:
                print("### Unable to open the csv file. The file might be open in a csv reader. ###")
        print()
        return csv_written

    @staticmethod
    def check_csv(csv_name):
        max_comma_count = 500
        csv_aligned = True
        line_number = 0

        with open(csv_name, 'r') as my_file:
            for line in my_file:
                line_number += 1
                line_commas = line.count(",")
                if line_commas < max_comma_count:
                    max_comma_count = line_commas
                if line_commas != max_comma_count and max_comma_count is not 0:
                    csv_aligned = False
                    print("##Line: %s has a different amount of metrics" % line_number)
        print()
        if csv_aligned is True:
            print("The csv is ready to upload to polaris")
        else:
            print("The csv needs to be fixed before uploading to polaris")
