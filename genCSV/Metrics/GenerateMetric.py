__author__ = ''


def determine_testcases(search_path_arguments):
    import genCSV
    test_cases = []
    combine_test_cases = False
    directories_down = genCSV.args.d
    dir_structure = int(get_directory_search_key())

    print("Number of locations to search: %s \n" % (len(search_path_arguments)))
    print("Locations: %s \n\n" % search_path_arguments)
    print("### Finding the required testcases ### \n\n")

    if genCSV.args.comb:
        combine_test_cases = True

    if genCSV.args.a:
        print("Automatically searching for testcase(s). \n")
        for search_path_argument in search_path_arguments:
            test_cases.extend(search_directory(search_path_argument, 20, True))

    elif directories_down:
        print("Looking %s directories deep \n" % directories_down)
        test_cases.extend(search_directory(search_path_arguments, directories_down, False))

    # The following 4 statements is how the script searches for testcases in the given arguments
    # 1 is designed for the current megatest with the duplicate directory
    elif dir_structure == 1:
        print("Searching for Megatest testcases with duplicate testcase names in the path \n")
        test_cases.extend(search_directory(search_path_arguments, 2, False))
        combine_test_cases = False

    # 2 is designed for megatest when the duplicate testcase folder is removed
    elif dir_structure == 2:
        print("Searching for Megatest testcases \n")
        test_cases.extend(search_directory(search_path_arguments, 1, False))
        combine_test_cases = False

    # 3 is for searching by the testcase itself
    elif dir_structure == 3:
        print("Searching the given testcase argument(s) \n")
        test_cases.extend(verify_test_case_directory(search_path_arguments))

    # 4 is for searching by the date folder and three levels into that
    elif dir_structure == 4:
        print("Searching for Nigthly testcase(s) \n")
        test_cases.extend(search_directory(search_path_arguments, 3, False))

    if combine_test_cases:
        test_cases = list(combine_identical_testcases(test_cases))

    found_testcases = len(test_cases)

    if found_testcases > 0:
        print("Found %s testcases \n" % found_testcases)
        print("Testcases:  %s \n\n" % (', '.join(test_cases)))
    else:
        print("*** Error couldn't find any testcases. Are you sure you have the right configuration option? "
              "Exiting the script!")
        raise SystemExit
    get_metrics(test_cases)


def get_directory_search_key():
    import json
    import FindFile

    config_file = FindFile.return_config_name()
    print("\nMy config file: %s \n" % config_file)
    # With open is a secure way to open and close a file. Using with we don't have to implicitly close the file
    # as it does it on its own
    try:
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # finds the default value for the order number to search files in the json file
            dir_structure = json_data['Search_Key']["Order"]["default"]
    except FileNotFoundError:
        print("*** Error the configuration file: %s  was not found!! Exiting the script!! ***\n\n" % config_file)
        raise SystemExit

    return int(dir_structure)


def get_subdirectories(paths):
    import os
    path_collections = []
    if isinstance(paths, (list, tuple)):
        for path in paths:
            path_collection = [os.path.join(path, name) for name in os.listdir(path)if os.path.isdir(
                               os.path.join(path, name))]
            path_collections.extend(path_collection)
    else:
        path_collection = [os.path.join(paths, name) for name in os.listdir(paths)if os.path.isdir(
                           os.path.join(paths, name))]
        path_collections.extend(path_collection)
    return path_collections


def search_directory(paths, directory_level, auto_search):
    directory_level -= 1
    path_collections = get_subdirectories(paths)
    if auto_search:
        test_cases = verify_test_case_directory(path_collections)
        if len(test_cases) > 0:
            return test_cases
    if directory_level != 0:
        path_collections = search_directory(path_collections, directory_level, auto_search)
    else:
        path_collections = verify_test_case_directory(path_collections)

    return path_collections


def verify_test_case_directory(paths):
    import os
    import genCSV
    test_cases = []
    default_test_case_sub_dirs = ('syn', 'apr', 'drc_lvs', 'sta', 'pv', 'ext', 'denall_reuse',
                                  'drcc', 'gden', 'HV', 'drc_IPall', 'lvs', 'drcd', 'trclvs')
    default_test_case_files = ("testcase_src_path", "last_1_rundirs", "design_name")

    for path in paths:
        try:
            directories = [file_name for file_name in os.listdir(path) if check_directory(
                           path, file_name, default_test_case_sub_dirs, default_test_case_files)]
            if path.endswith("fdkex_mcmm") or len(directories) == 0:
                if not genCSV.args.a:
                    print("SKIPPED:  %s \n" % path)
                continue
            else:
                test_cases.append(path)
        except FileNotFoundError:
            print("*** Error the file: %s was not found *** \n\n" % path)
            continue

    return test_cases


def check_directory(path, file_name, default_test_case_sub_dirs, default_test_case_files):
    import os
    file = os.path.join(path, file_name)
    sub_dirs = ("reports", "logs", "inputs", 'outputs')

    if os.path.isdir(file)and file_name in default_test_case_sub_dirs:
        for directory in os.listdir(file):
            if directory in sub_dirs:
                return True
    elif file_name in default_test_case_files:
        return True
    return False


def combine_identical_testcases(test_cases):
    import os
    test_case_names = []
    grouped_test_cases = []

    # This loop creates a list of testcase names
    for test_case in test_cases:
        test_case_name = os.path.basename(test_case)
        if test_case_name not in test_case_names:
            test_case_names.append(test_case_name)

    # This loop adds all paths with the same testcase name
    for test_case_name in test_case_names:
        similar_test_cases = []
        for test_case in test_cases:
            temp_test_case_name = os.path.basename(test_case)
            if temp_test_case_name == test_case_name:
                similar_test_cases.append(test_case)

        grouped_test_cases.append(tuple(similar_test_cases))

    return grouped_test_cases


def get_metrics(test_cases):
    import os
    import FindFile
    from Metrics.ToolMetric import ToolMetric

    csv_written = False
    csv_name = FindFile.return_csv_name()

    for test_case in test_cases:
        metrics_collections = []
        list_of_files = []

        if isinstance(test_case, (list, tuple)):
            for temp_test_case in range(len(test_case)):
                tool = check_tool(test_case[temp_test_case])
                list_of_files.extend(FindFile.search_dir(test_case[temp_test_case], tool))
            test_case = test_case[0]
        else:
            tool = check_tool(test_case)
            list_of_files.extend(FindFile.search_dir(test_case, tool))

        print("Files to be searched:")

        for file in list_of_files:
            print("%s %s \n" % (file, format_file_size(os.path.getsize(file))))

        print("%s Total found \n\n" % len(list_of_files))
        tool_metric = ToolMetric(list_of_files, test_case, tool)
        if tool is "cadence":
            metrics_collections.extend(tool_metric.get_cadence_metrics())
        else:
            metrics_collections.extend(tool_metric.get_synopsys_metrics())

        csv_written = write_csv(metrics_collections, csv_written, test_case, csv_name)

    check_csv(csv_name)


def format_file_size(unformatted_size):
    import math
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(unformatted_size, 1024)))
    p = math.pow(1024, i)
    s = round(unformatted_size/p, 2)
    if s > 0:
        return '%s %s' % (s, size_name[i])
    else:
        return '0B'


def check_tool(test_case):
    import re

    test_case_tool_path = get_test_case_tool_path(test_case)
    # The following regular expressions are made to find the tool for megatest testcases
    cadence_tool = re.search(r'/([a-zA-Z_]{1,3}[\d\.]+_[cC]{1})/', test_case_tool_path)

    if "cadence" in test_case_tool_path or cadence_tool:
        return "cadence"
    else:
        # default tool is synopsys
        return "synopsys"


def get_test_case_tool_path(test_case):
    import os
    sub_directories = os.listdir(test_case)

    if "testcase_src_path" in sub_directories:
        tool_file = "testcase_src_path"
    elif "last_1_rundirs" in sub_directories:
        tool_file = "last_1_rundirs"
    else:
        return test_case
    try:
        with open(os.path.join(test_case, tool_file), 'r') as file:
            return file.readline()
    except IOError:
        return test_case


def write_csv(metrics_collections, csv_written, test_case, csv_name):
    names = 0
    values = 1
    metric_values = get_csv_values(metrics_collections, csv_written)

    if csv_written is False:
        csv_written = True
        write_header(csv_name, metric_values[names])
        write_values(csv_name, metric_values[values])
        print('%s created with %s \n\n' % (csv_name, test_case))
    else:
        write_values(csv_name, metric_values[values])
        print('%s appended with %s \n\n' % (csv_name, test_case))

    return csv_written


def get_csv_values(metrics_collections, csv_written):
    metric_name = 0
    metric_value = 1
    names = []
    values = []
    metric_values = []

    print("Metrics found: ")
    for metric_pair in metrics_collections:
        print(metric_pair)
        if csv_written is False:
            names.append(metric_pair[metric_name])
            values.append(metric_pair[metric_value])
        else:
            values.append(metric_pair[metric_value])
    print("\n")
    metric_values.append(names)
    metric_values.append(values)

    return metric_values


def write_header(csv_name, metric_names):
    import csv
    # The 'w' argument in the following "with open" statement means that if the file doesnt exist then it
    # will be and if one does exist it will be completely overwritten.
    try:
        with open(csv_name, 'w') as my_file:
            writer = csv.writer(my_file, lineterminator='\n')
            writer.writerow(metric_names)
    except IOError:
        exit_script()


def write_values(csv_name, metric_values):
    import csv
    try:
        # The 'a' argument in the following "with open" statement means that if the file does exist then it will be
        # appended to.
        with open(csv_name, 'a') as my_file:
            writer = csv.writer(my_file, lineterminator='\n', quoting=csv.QUOTE_ALL)
            writer.writerow(metric_values)
    except IOError:
        exit_script()


def exit_script():
    answer = input("### Unable to open the csv file. The file might be open in a csv reader."
                   " Enter 0 to exit or enter anything else to continue ###")
    if answer == "0":
        raise SystemExit


def check_csv(csv_name):
    max_comma_count = 500
    csv_aligned = True
    line_number = 0

    try:
        with open(csv_name, 'a+') as my_file:
            for line in my_file:
                line_number += 1
                line_commas = line.count(",")
                if line_commas < max_comma_count:
                    max_comma_count = line_commas
                if line_commas != max_comma_count and max_comma_count is not 0:
                    csv_aligned = False
                    print("##Line: %s has a different amount of metrics \n" % line_number)
        if csv_aligned is True:
            print("The csv is ready to upload to polaris")
        else:
            print("The csv needs to be fixed before uploading to polaris")
    except IOError:
            raise SystemExit
