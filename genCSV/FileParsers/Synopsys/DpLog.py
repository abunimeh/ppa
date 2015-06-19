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
    def replace_space(metric_name):
        import re
        newName = re.sub(r'[\W]+', "_", metric_name)
        return newName

    @staticmethod
    def check_list(metrics, metric_name):
        metric_in_list = True
        for metric_pair in metrics:
            if metric_name == metric_pair[0]:
                metric_in_list = False
                break
        return metric_in_list

    @staticmethod
    def search_file(file):
        import re
        import Metrics.FormatMetric as Format
        DataItems = []
        stage = DpLog.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        dpData = dpLogData()
        dpData.foundPeakMem = [Format.replace_space(stage + " Peak Memory") + " (MB)", "N/A"]
        dpData.foundRuntime = [Format.replace_space(stage + " Runtime")+" (secs)", "N/A"]
        # We read in the lines in reversed in order to find the last value in the file
        for line in reversed(lines):
            if DpLog.check_list(DataItems, dpData.foundPeakMem[0]):
                foundPeakMem = re.search(r'.*:[\s]*(Peak)[\s]*=[\s]*([\d]+[\s]*)\(mb\)', line, re.I)
                if foundPeakMem:
                    dpData.foundPeakMem[1] = Format.format_metric_values(foundPeakMem.group(2))
                    DataItems.append(tuple(dpData.foundPeakMem))
            if DpLog.check_list(DataItems, dpData.foundRuntime[0]):
                foundRuntime = re.search(r'(Overall[\s]*engine[\s]*time)[\s]*=+[\s]*([\d]*:*[\d]*:*[\d]+)+', line, re.I)
                if foundRuntime:
                    dpData.foundRuntime[1] = Format.format_metric_values(foundRuntime.group(2))
                    DataItems.append(tuple(dpData.foundRuntime))
            if len(DataItems) == 2:
                break

        return DataItems
