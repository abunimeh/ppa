class findFiles:
    def searchDir():
        import fnmatch
        import os
        from Configurations import Configurations

        fileNames = ['*.fill.qor.rpt', '*.fill.physical.rpt', '*.cts.clock_tree.rpt', 'icc.log', '*.min.qor.rpt',
                    '*.inc_compile.qor.rpt' , 'dc.log', '*.link.rpt', '*.max.qor.rpt', '*.run_time.rpt',
                    '*.noise.qor.rpt', '*.power.power.rpt', '*.LAYOUT_ERRORS', 'Final_Report.txt',
                    'drc_IPall.dp.log', 'trclvs.dp.log']
        base_path = Configurations().parser_final()
        matches = []

        for root, dirnames, filenames in os.walk(base_path):
            for files in fileNames:
                for filename in fnmatch.filter(filenames, files):
                    matches.append(os.path.join(root, filename))
        for file in matches:
            print(file)
        print(len(matches), "\n\n\n")
        return matches