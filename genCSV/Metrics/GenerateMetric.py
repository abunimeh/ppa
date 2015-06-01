__author__ = ''


class GenerateMetric:
    @staticmethod
    def determine_testcases(command_line_args):
        import json
        import os
        from FindFile import FindFiles

        config_file = FindFiles.return_config_name()

        print("My config file:", config_file)
        # command_line_args[0] is always the script location so we get rid of it since we don't need it anymore
        test_case_args = command_line_args[1:len(command_line_args)]
        for test_case_arg in test_case_args:
            if test_case_arg.endswith('.json'):
                test_case_args.remove(test_case_arg)
        # command_line_args[0] is always the script location so we get rid of it since we don't need it anymore
        # if command_line_args[1].endswith("config.json"):
        #     test_case_args = command_line_args[2:len(command_line_args)]
        # else:
        #     test_case_args = command_line_args[1:len(command_line_args)]

        # With open is a secure way to open and close a file. Using with we don't have to implicitly close the file
        # as it does it on its own
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # finds the default value for the order number to search files in the json file
            dir_structure = json_data['Search_Key']["Order"]["default"]

        print("Number locations to search:", (len(test_case_args)))
        print()
        print("Locations:", test_case_args)
        print()
        test_cases_list = []
        print("### Finding the required testcases ###")
        print()

        # The following 4 statements/loops is how the script searches for testcases in the given arguments
        # 1 is designed for the current megatest with the duplicate directory
        if dir_structure == "1":
            for argument in test_case_args:
                # command_line_args[0] is always the name of the script so we exclude it from the search
                first_level = [os.path.join(argument, name) for name in os.listdir(argument) if os.path.isdir(
                    os.path.join(argument, name))]

                for dir_names in first_level:
                    files_to_search = [os.path.join(dir_names, name) for name in os.listdir(dir_names)if os.path.isdir(
                        os.path.join(dir_names, name))]

                    for files in files_to_search:
                        test_cases_list.append(files)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)

        # 2 is designed for megatest when the duplicate testcase folder is removed
        elif dir_structure == "2":
            for argument in test_case_args:
                files_to_search = [os.path.join(argument, name) for name in os.listdir(argument)if os.path.isdir(
                    os.path.join(argument, name))]

                for files in files_to_search:
                    test_cases_list.append(files)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)

        # 3 is for searching by the testcase itself
        elif dir_structure == "3":
            for argument in test_case_args:
                test_cases_list.append(argument)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)

        # 4 is for searching by the date folder and three levels into that
        elif dir_structure == "4":
            for argument in test_case_args:
                first_level = [os.path.join(argument, name) for name in os.listdir(argument)if os.path.isdir(
                    os.path.join(argument, name)) if os.path.join(argument, name).endswith("runs")]

                for dir_names in first_level:
                    second_level = [os.path.join(dir_names, name) for name in os.listdir(dir_names)if os.path.isdir(
                        os.path.join(dir_names, name))]

                    for second_lvl_files in second_level:
                        third_level = [os.path.join(second_lvl_files, name) for name in os.listdir(
                            second_lvl_files) if os.path.isdir(os.path.join(second_lvl_files, name))]

                        for third_lvl_files in third_level:
                            if third_lvl_files.endswith("fdkex_mcmm"):
                                print("SKIPPED:", third_lvl_files)
                                continue
                            else:
                                test_cases_list.append(third_lvl_files)
            print("Found %s testcases" % len(test_cases_list))
            print("Testcases:", test_cases_list)
        GenerateMetric.get_metrics(test_cases_list)

    @staticmethod
    def get_metrics(test_cases_list):
        from FindFile import FindFiles
        from Metrics.CadenceMetric import CadenceMetric
        from Metrics.SynopsysMetric import SynopsysMetric

        csv_written = False
        csv_name = FindFiles.return_csv_name()

        for test_case in test_cases_list:
            # default tool is synopsys
            tool = "synopsys"
            metrics_collections = []

            print("### Searching:", test_case)
            print()

            if "cadence" in test_case:
                tool = "cadence"
            elif "synopsys" in test_case:
                tool = "synopsys"

            list_of_files = FindFiles.search_dir(test_case, tool)

            if tool is "cadence":
                metrics_collections.extend(CadenceMetric.get_cadence_metrics(list_of_files, test_case, tool))
            else:
                metrics_collections.extend(SynopsysMetric.get_synopsys_metrics(list_of_files, test_case, tool))

            csv_written = GenerateMetric.write_csv(metrics_collections, csv_written, test_case, csv_name)
        GenerateMetric.check_csv(csv_name)

        # temp_metric_collections = OrganizeMetric.normalize_list(metrics_collections)
        # print(temp_metric_collections)
        # for temp_metric_collection in temp_metric_collections:
        #     formatted_metric_list = OrganizeMetric.sort_metrics(temp_metric_collection)
        #     csv_written = GenerateMetric.generate_csv(formatted_metric_list, csv_written)

    @staticmethod
    def generate_csv_data(metrics_collections, csv_written):
        metric_name = 0
        metric_value = 1
        metrics = []
        values = []
        print("Metrics found: ")
        for metric_pair in metrics_collections:
            # temp_metric_list = tuple(temp_metric_collection)
            if csv_written is False:
                metrics += [metric_pair[metric_name]]
            else:
                metrics += [metric_pair[metric_value]]
            # for metric in range(len(temp_metric_list)):
            #     print(temp_metric_list[metric])
            #     # Names and values are concatenated into a string in order to have horizontal column
            #     names += [temp_metric_list[metric][name]]
            #     values += [temp_metric_list[metric][value]]
        return metrics

    @staticmethod
    def generate_csv(metrics_collections, csv_written):
        metrics = GenerateMetric.generate_csv_data(metrics_collections, csv_written)
        csv_written = GenerateMetric.write_csv(metrics, csv_written)
        return csv_written

    @staticmethod
    def write_csv(metrics_collections, csv_written, test_case, csv_name):
        import csv

        metric_name = 0
        metric_value = 1
        names = []
        values = []

        print("Metrics found: ")
        for metric_pair in metrics_collections:
            # temp_metric_list = tuple(temp_metric_collection)
            print(metric_pair)
            if csv_written is False:
                names.append(metric_pair[metric_name])
                values.append(metric_pair[metric_value])
            else:
                values.append(metric_pair[metric_value])
            # for metric in range(len(temp_metric_list)):
            #     print(temp_metric_list[metric])
            #     # Names and values are concatenated into a string in order to have horizontal column
            #     names += [temp_metric_list[metric][name]]
            #     values += [temp_metric_list[metric][value]]
        # names, values = [], []
        # name = 0
        # value = 1
        # metrics = GenerateMetric.generate_csv_data(formatted_metric_list, csv_written)

        # for temp_metric_collection in sorted_metrics:
        #     temp_metric_list = tuple(temp_metric_collection)
        #     for metric in range(len(temp_metric_list)):
        #         print(temp_metric_list[metric])
        #         # Names and values are concatenated into a string in order to have horizontal column
        #         names += [temp_metric_list[metric][name]]
        #         values += [temp_metric_list[metric][value]]

        if csv_written is False:
            csv_written = True
            # Creates a csv with the first testcase only
            # The 'wt' argument in the following "with open" statement means that if the file doesnt exist then it
            # will be and if one does exist it will be completely overwritten.
            try:
                with open(csv_name, 'wt') as my_file:
                    writer = csv.writer(my_file, lineterminator='\n')
                    writer.writerow(names)
                    writer = csv.writer(my_file, lineterminator='\n', quoting=csv.QUOTE_ALL)
                    writer.writerow(values)
                print(csv_name, 'created with', test_case)
            except IOError:
                print("### Unable to open the csv file. The file might be open in a csv reader. ###")
        else:
            try:
                # The 'a' argument in the following "with open" statement means that if the file does exist then it will be
                # appended to.
                with open(csv_name, 'a') as my_file:
                    writer = csv.writer(my_file, lineterminator='\n', quoting=csv.QUOTE_ALL)
                    writer.writerow(values)
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

    # @staticmethod
    # def return_csv_name():
    #     import json
    #     config_file = GenerateMetric.return_config_name()
    #     with open(config_file, 'r') as f:
    #         json_data = json.load(f)
    #         # finds the default value for the order number to search files in the json file
    #         csv_location = json_data['Csv_location']
    #     return csv_location
    #
    # @staticmethod
    # def return_config_name():
    #     import sys
    #     import os
    #     for argument in sys.argv:
    #         if argument.endswith(".json"):
    #            config_file = argument
    #            return config_file
    #         else:
    #            config_file = os.path.join(sys.path[0], 'config.json')
    #     return config_file