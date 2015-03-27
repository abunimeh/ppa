class dpLogData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)
class dpLog:
    def searchfile():
        import re
        from Configurations import Configurations
        base_path = Configurations().parser_final()
        foundFlag = 0
        DataItems = []
        # Open the file with read only permit
        f = open(base_path + r'cpu_testcase\drc_lvs\trclvs\trclvs.dp.log', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        dpData = dpLogData()

        # reversed in order to find the last value in the file
        for line in reversed(lines):
            foundPeakMem = re.search(r':+[\s]*(Peak)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\s]*\(mb\)+)+', line, re.I)
            foundRuntime = re.search(r'(Overall[\s]*engine[\s]*time)[\s]*=+[\s]*([\d]*:*[\d]*:*[\d]+)+', line, re.I)

            if foundPeakMem and foundFlag != 1:
                dpData.foundPeakMem = (foundPeakMem.group(1), foundPeakMem.group(2))
                DataItems.append(dpData.foundPeakMem)
                foundFlag = 1
            if foundRuntime:
                dpData.foundRuntime = re.sub(r'[\W]+', "_", foundRuntime.group(1)), foundRuntime.group(2)
                DataItems.append(dpData.foundRuntime)

        return ["%s" % i[0] for i in DataItems], ["%s" % i[1] for i in DataItems]
