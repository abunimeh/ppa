class findFiles:
    @staticmethod
    def searchDir(test_case):
        import fnmatch
        import os
        from Configurations import Configurations

        fileNames = ('*.fill.qor.rpt', '*.fill.physical.rpt', '*.cts.clock_tree.rpt', 'icc.log', '*.min.qor.rpt',
                    '*.inc_compile.qor.rpt' , 'dc.log', '*.link.rpt', '*.max.qor.rpt', '*.run_time.rpt',
                    '*.noise.qor.rpt', '*.power.power.rpt', '*.LAYOUT_ERRORS', 'Final_Report.txt',
                    'drc_IPall.dp.log', 'trclvs.dp.log')
        base_path = Configurations().parser_final() + test_case
        matches = []

        for root, dirnames, filenames in os.walk(base_path):
            for file in fileNames:
                if ".LAYOUT_ERRORS" not in file:
                    for filename in fnmatch.filter(filenames, file):
                        matches.append(os.path.join(root, filename))
                else:
                    if 'drc_lvs' in root:
                        for filename in fnmatch.filter(filenames, file):
                            matches.append(os.path.join(root, filename))
        for file in matches:
            print(file)
        print(len(matches), "\n\n\n")
        return matches