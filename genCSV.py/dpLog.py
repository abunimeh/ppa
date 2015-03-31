class dpLogData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)


class dpLog:
    def metric_naming(file):
        import re
        stage = ""
        denall = re.search(r'.*denall.*', file, re.I)
        ipall = re.search(r'.*drcd.*', file, re.I)
        drcd = re.search(r'.*ipall.*', file, re.I)
        trclvs = re.search(r'.*trclvs.*', file, re.I)
        if denall:
            stage = 'drc denall reuse'
        if ipall:
            stage = 'drc IPall'
        if drcd:
            stage = 'drc drcd'
        if trclvs:
            stage = 'drc trclvs'
        return stage

    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    def searchfile(file):
        import re
        from Configurations import Configurations
        base_path = Configurations().parser_final()
        foundFlag = 0
        DataItems = []
        stage = dpLog.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        dpData = dpLogData()

        # reversed in order to find the last value in the file
        for line in reversed(lines):
            foundPeakMem = re.search(r':+[\s]*(Peak)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\s]*\(mb\)+)+', line, re.I)
            foundRuntime = re.search(r'(Overall[\s]*engine[\s]*time)[\s]*=+[\s]*([\d]*:*[\d]*:*[\d]+)+', line, re.I)

            if foundPeakMem and foundFlag != 1:
                dpData.foundPeakMem =dpLog.replaceSpace(stage +" Peak Memory"), foundPeakMem.group(2)
                DataItems.append(dpData.foundPeakMem)
                foundFlag = 1
            if foundRuntime:
                dpData.foundRuntime = dpLog.replaceSpace(stage +" Runtime"), foundRuntime.group(2)
                DataItems.append(dpData.foundRuntime)

        return ["%s" % i[0] for i in DataItems], ["%s" % i[1] for i in DataItems]
