class dpLogData:
    pass
class dpLog:
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
    def replace_space(metric_name):
        import re
        newName = re.sub(r'[\W]+', "_", metric_name)
        return newName

    @staticmethod
    def search_file(file):
        import re
        from Metrics.FormatMetric import FormatMetric
        foundFlag = 0
        DataItems = []
        stage = dpLog.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        i = 0
        formt = FormatMetric()
        dpData = dpLogData()
        dpData.foundPeakMem = [dpLog.replace_space(stage + " Peak Memory") + " (MB)", "N/A"]
        dpData.foundRuntime = [dpLog.replace_space(stage + " Runtime")+" (secs)", "N/A"]
        # reversed in order to find the last value in the file
        for line in reversed(lines):
            foundPeakMem = re.search(r'.*:[\s]*(Peak)[\s]*=[\s]*([\d]*[\s]*)\(mb\)', line, re.I)
            foundRuntime = re.search(r'(Overall[\s]*engine[\s]*time)[\s]*=+[\s]*([\d]*:*[\d]*:*[\d]+)+', line, re.I)

            if foundPeakMem:
                dpData.foundPeakMem[1] = formt.format_metric_values(foundPeakMem.group(2))
                DataItems.append(tuple(dpData.foundPeakMem))
            elif foundRuntime:
                dpData.foundRuntime[1] = formt.format_metric_values(foundRuntime.group(2))
                DataItems.append(tuple(dpData.foundRuntime))
            if len(DataItems) == 2:
                break

        return DataItems
