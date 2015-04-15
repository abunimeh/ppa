class findFiles:
    @staticmethod
    def searchDir(test_case):
        import fnmatch
        import os
        from Configurations import Configurations

        # file_names = ['*.fill.qor.rpt', '*.fill.physical.rpt', '*.cts.clock_tree.rpt', 'icc.log', '*.min.qor.rpt',
        #             '*.inc_compile.qor.rpt' , 'dc.log', '*.link.rpt', '*.max.qor.rpt', '*.run_time.rpt',
        #             '*.noise.qor.rpt', '*.power.power.rpt', '*.LAYOUT_ERRORS', 'Final_Report.txt',
        #             'drc_IPall.dp.log', 'denall_reuse.dp.log', 'trclvs.dp.log']
        file_names = list(Configurations().get_file_endings().split(","))
        print("Current file endings to search for:", file_names)
        file_names = list(filter(None, file_names))
        print("NOW Current file endings to search for:", file_names)
        # test_case is the argument sent in when the user call the script
        if '--add' in test_case:
            file_names = findFiles.add_file_ending(file_names)
            exit("exiting the script")
        elif '--remove' in test_case:
            file_names = findFiles.remove_file_ending(file_names)
            exit("exiting the script")
        matches = []
        print("os.walk in",  test_case)
        for root, dirnames, filenames in os.walk(test_case):
            for file in file_names:
                if ".LAYOUT_ERRORS" not in file:
                    for filename in fnmatch.filter(filenames, file):
                        matches.append(os.path.join(root, filename))
                else:
                    if 'drc_lvs' in root:
                        for filename in fnmatch.filter(filenames, file):
                            matches.append(os.path.join(root, filename))
        print("files to be searched:")
        for file in matches:
            print(file)
        print(len(matches), "Total found\n\n")
        return matches

    @staticmethod
    def add_file_ending(file_names):
        from configparser import ConfigParser
        answer = "N"
        file_ending = "s"
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
                        config.set('file_endings', 'filenames', new_file_names)
                        # Write to 'Config.ini'
                        with open('Config.ini', 'w') as configfile:
                            config.write(configfile)
                        return file_names
                    else:
                        answer = "N"
        if file_ending == "exit":
                        exit("exiting")
        return file_names

    @staticmethod
    def remove_file_ending(file_names):
        from configparser import ConfigParser
        answer = "N"
        file_ending = "s"
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
                        config.set('file_endings', 'filenames', new_file_names)
                        # Write to 'Config.ini'
                        with open('Config.ini', 'w') as configfile:
                            config.write(configfile)
                        return file_names
                    else:
                        answer = "N"
        if file_ending == "exit":
                        exit("exiting")
        return file_names