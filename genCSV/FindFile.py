class FindFiles:
    @staticmethod
    def search_dir(test_case, tool):
        import fnmatch
        import os

        file_endings = FindFiles.return_file_endings(tool)
        found_files = []
        included_path_names = [test_case, 'syn', 'apr', 'drc_lvs', 'sta', 'pv', 'runs', 'reports', 'logs',
                   'reports_max', 'reports_min', 'denall_reuse', 'drcc', 'gden', 'HV', 'drc_IPall', 'lvs', 'max',
                   'min', 'power', 'noise', 'drcd', 'trclvs']

        # print("Current file endings to search for:", file_endings)
        # print()
        #
        # # test_case is the argument sent in when the user calls the script
        # print("Searching for files in",  test_case)

        for root, dirnames, filenames in os.walk(test_case, topdown=True):
            # This statement makes sure that we only search for paths that includes the names in the list, included_path_names
            dirnames[:] = [d for d in dirnames if d in included_path_names]

            # Because the files we are searching for in the drc_lvs directory does not follow the patterns that the rest of the files do we have to do the following
            if "drcd" in root or "denall_reuse" in root or "drc_IPall" in root or "trclvs" in root:
                for root_name, directory_names, files in os.walk(root):
                    for file_ending in file_endings:
                        for drcd_file in fnmatch.filter(files, file_ending):
                            found_files.append(os.path.join(root_name, drcd_file))

            else:
                for file in file_endings:
                    if 'drc.sum' in file:
                        if 'drc_lvs' in root:
                            for filename in fnmatch.filter(filenames, file):
                                found_files.append(os.path.join(root, filename))

                    elif '*.link.rpt' in file:
                        if 'pv' in root or 'sta' in root:
                            for filename in fnmatch.filter(filenames, file):
                                found_files.append(os.path.join(root, filename))

                    else:
                        for filename in fnmatch.filter(filenames, file):
                            found_files.append(os.path.join(root, filename))

        return found_files

    @staticmethod
    def return_csv_name():
        import json

        config_file = FindFiles.return_config_name()

        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # finds the default value for the order number to search files in the json file
            csv_location = json_data['Csv_location']

        return csv_location

    @staticmethod
    def return_config_name():
        import sys
        import os

        # If a config.json file is passed in then the program will use that as the configuration file otherwise we use the one
        # located at the script location
        # sys.argv is a built in list that contains the command line arguments
        for argument in sys.argv:
            if argument.endswith(".json"):
               config_file = argument
               return config_file

            else:
               config_file = os.path.join(sys.path[0], 'config.json')

        return config_file

    @staticmethod
    def return_file_endings(tool):
        import json

        config_file = FindFiles.return_config_name()

        # Finds the file name endings
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            file_endings = json_data['file_endings'][tool]

        # This line gets rid of empty strings just in case one is accidently passed
        file_endings = list(filter(None, file_endings))

        return file_endings
