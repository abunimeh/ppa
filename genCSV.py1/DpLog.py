class dpLogData:
    pass
class DpLog:
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        denall = re.search(r'.*denall_reuse.*', file, re.I)
        drcd = re.search(r'.*drcd.*', file, re.I)
        ipall = re.search(r'.*ipall.*', file, re.I)
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

    @staticmethod
    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    @staticmethod
    def searchfile(file):
        import re
        foundFlag = 0
        DataItems = []
        stage = DpLog.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        i = 0
        dpData = dpLogData()
        dpData.foundPeakMem = [DpLog.replaceSpace(stage + " Peak Memory"), "N/A"]
        dpData.foundRuntime = [DpLog.replaceSpace(stage + " Runtime"), "N/A"]
        # reversed in order to find the last value in the file
        for line in reversed(lines):
            foundPeakMem = re.search(r'.*:[\s]*(Peak)[\s]*=[\s]*([\d]*[\s]*\(mb\))', line, re.I)
            foundRuntime = re.search(r'(Overall[\s]*engine[\s]*time)[\s]*=+[\s]*([\d]*:*[\d]*:*[\d]+)+', line, re.I)

            if foundPeakMem:
                dpData.foundPeakMem[1] = foundPeakMem.group(2)
                DataItems.append(tuple(dpData.foundPeakMem))
            elif foundRuntime:
                dpData.foundRuntime[1] = foundRuntime.group(2)
                DataItems.append(tuple(dpData.foundRuntime))
            if len(DataItems) == 2:
                break

        return DataItems
