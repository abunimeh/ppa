class RunTimeRptData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class RunTimeRpt:
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_power = re.search(r'.*pv.*power.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)
        if pv_max:
            stage = 'pv max tttt'
        if pv_min:
            stage = 'pv min tttt'
        if pv_power:
            stage = 'pv power tttt'
        if pv_noise:
            stage = 'pv noise tttt'
        return stage

    @staticmethod
    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    @staticmethod
    def searchfile(file):
        import re
        stage = RunTimeRpt.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        DataItems = []
        rptData = RunTimeRptData()
        rptData.foundRunTime = [RunTimeRpt.replaceSpace(stage + " run time"), "N/A"]

        for line in lines:
            foundRunTime = re.search(r'(Runtime[\s]*of[\s]*Entire[\s]*Timing[\s]*Run)[\s]*=+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if foundRunTime:
                rptData.foundRunTime[1] = foundRunTime.group(2)

        DataItems.append(rptData.foundRunTime)

        return DataItems