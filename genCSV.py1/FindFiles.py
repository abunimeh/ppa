class findFiles:
    @staticmethod
    def search_dir(test_case, tool):
        import fnmatch
        import os
        import json
        from Configurations import Configurations
        #from OtherMetricClass import OtherMetricClass


        # Finds the file name endings
        with open(r'config.json', 'r') as f:
            json_data = json.load(f)
            file_names = json_data['file_endings'][tool]

        # This line gets rid of empty strings just in case one is accidently passed
        file_names = list(filter(None, file_names))

        print("Current file endings to search for:", file_names)
        # test_case is the argument sent in when the user call the script
        if '--add' in test_case:
            file_ending = findFiles.add_file_ending(file_names)
            ans = input("Would you like to add metrics associated with the new file ending(Y or N)?")
            while ans != "Y" or ans != "N":
                if ans == "Y":
                    #OtherMetricClass.search_file(file_ending)
                    break
                elif ans == "N":
                    exit("Exiting the script")
                else:
                    ans = input("Would you like to add metrics associated with the new file ending(Y or N)?")
            exit("Exiting the script")
        elif '--remove' in test_case:
            file_ending = findFiles.remove_file_ending(file_names)
            ans = input("Would you like to remove the metrics searched associated with the new file ending(Y or N)?")
            while ans != "Y" or ans != "N":
                if ans == "Y":
                    #OtherMetricClass.search_file(file_ending)
                    break
                elif ans == "N":
                    exit("Exiting the script")
                else:
                    ans = input("Would you like to remove metrics associated with the file ending(Y or N)?")
            exit("Exiting the script")
        matches = []
        include = [test_case, 'syn', 'apr', 'drc_lvs', 'sta', 'pv', 'runs', 'reports', 'logs', 'logs', 'reports_max',
                   'reports_min', 'denall_reuse', 'drcc', 'gden', 'HV', 'drc_IPall', 'lvs', 'max', 'min', 'power',
                   'noise', 'drcd', 'trclvs']
        print("os.walk in",  test_case)
        for root, dirnames, filenames in os.walk(test_case, topdown=True):
            dirnames[:] = [d for d in dirnames if d in include]
            # Because the files we are searching for in the drc_lvs directory does not follow the patterns that the rest of the files do we have to do the following
            if "drcd" in root or "denall_reuse" in root or "drc_IPall" in root or "trclvs" in root:
                for root_name, directory_names, files in os.walk(root):
                    for file_endings in file_names:
                        for drcd_file in fnmatch.filter(files, file_endings):
                            matches.append(os.path.join(root_name, drcd_file))

            else:
                for file in file_names:
                    if 'drc.sum' in file:
                        if 'drc_lvs' in root:
                            for filename in fnmatch.filter(filenames, file):
                                matches.append(os.path.join(root, filename))
                    elif '*.link.rpt' in file:
                        if 'pv' in root or 'sta' in root:
                            for filename in fnmatch.filter(filenames, file):
                                matches.append(os.path.join(root, filename))
                    else:
                        for filename in fnmatch.filter(filenames, file):
                            matches.append(os.path.join(root, filename))

        print("Files to be searched:")
        for file in matches:
            print(file)
        print(len(matches), "Total found\n\n")
        return matches

    @staticmethod
    def add_file_ending(file_names):
        from configparser import ConfigParser
        answer = "N"
        file_ending = ""
        tool = "synopsys"
        which_tool = input("Enter 1 for Cadence, 2 for Synopsys")
        if which_tool == 1:
            tool = "synopsys"
        elif which_tool == 2:
            tool = "cadence"
        while file_ending != "exit":
            if answer == "N":
                file_ending = input("Enter the unique file ending (type 'exit' to quit):")
                print("Received: '%s' Are you sure? Type Y or N" % file_ending)
                answer = input()
            if answer == "Y":
                if file_ending in file_names:
                    print("'%s' is already being used." % file_ending)
                    answer = "N"
                elif file_ending not in file_names:
                    print("'%s' Will be added to the list of file endings. Are you sure? Type Y or N" % file_ending)
                    answer_2 = input()
                    if answer_2 == "Y":
                        new_file_names = ""
                        file_names.append(file_ending)
                        for names in file_names:
                            if names != "":
                                print(names)
                                new_file_names += names + ","
                        print("New list:", new_file_names)
                        config = ConfigParser()
                        config.read('Config.ini')
                        config.set('file_endings', tool, new_file_names)
                        # Write to 'Config.ini'
                        with open('Config.ini', 'w') as configfile:
                            config.write(configfile)
                        return file_names
                    else:
                        answer = "N"
        if file_ending == "exit":
                        exit("exiting")
        return file_ending

    @staticmethod
    def remove_file_ending(file_names):
        from configparser import ConfigParser
        answer = "N"
        file_ending = ""
        tool = "synopsys"
        which_tool = input("Enter 1 for Cadence, 2 for Synopsys")
        if which_tool == 1:
            tool = "synopsys"
        elif which_tool == 2:
            tool = "cadence"
        while file_ending != "exit":
            if answer == "N":
                file_ending = input("Enter the unique file ending to be removed(type 'exit' to quit):")
                print("Received: '%s' Are you sure? Type Y or N" % file_ending)
                answer = input()
            if answer == "Y":
                if file_ending not in file_names:
                    print("'%s' is already being used." % file_ending)
                    answer = "N"
                elif file_ending in file_names:
                    print("'%s' Will be removed to the list of file endings. Are you sure? Type Y or N" % file_ending)
                    answer_2 = input()
                    if answer_2 == "Y":
                        new_file_names = ""
                        file_names.remove(file_ending)
                        for names in file_names:
                            if names != "":
                                print(names)
                                new_file_names += names + ","
                        print("New list:", new_file_names)
                        config = ConfigParser()
                        config.read('Config.ini')
                        config.set('file_endings', tool, new_file_names)
                        # Write to 'Config.ini'
                        with open('Config.ini', 'w') as configfile:
                            config.write(configfile)
                        return file_names
                    else:
                        answer = "N"
        if file_ending == "exit":
                        exit("exiting")
        return file_ending