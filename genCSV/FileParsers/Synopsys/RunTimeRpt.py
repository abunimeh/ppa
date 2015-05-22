class RunTimeRptData:
    pass


class RunTimeRpt:
    # metric_stage_name() finds the stage of the temp_metric_collection and returns the name
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        pv_max = re.search(r'.*pv.*max.*|.*sta.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*|.*sta.*min.*', file, re.I)
        pv_power = re.search(r'.*pv.*power.*|.*sta.*power.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*|.*sta.*noise.*', file, re.I)
        if pv_max:
            stage = 'pv max tttt'
        elif pv_min:
            stage = 'pv min tttt'
        elif pv_power:
            stage = 'pv power tttt'
        elif pv_noise:
            stage = 'pv noise tttt'
        return stage

    # replace_space() replaces all the blank spaces with underscores
    @staticmethod
    def replace_space(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    # search_file() opens the file sent to it and searches for the specified temp_metric_collection
    @staticmethod
    def search_file(file):
        import re
        from Metrics.FormatMetric import FormatMetric

        stage = RunTimeRpt.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        DataItems = []
        rptData = RunTimeRptData()
        rptData.foundRunTime_max = [RunTimeRpt.replace_space("pv max tttt" + " run time")+" (secs)", "N/A"]
        rptData.foundRunTime_min = [RunTimeRpt.replace_space("pv min tttt" + " run time")+" (secs)", "N/A"]
        rptData.foundRunTime_noise = [RunTimeRpt.replace_space("pv noise tttt" + " run time")+" (secs)", "N/A"]
        rptData.foundRunTime_power = [RunTimeRpt.replace_space("pv power tttt" + " run time")+" (secs)", "N/A"]

        for line in lines:
            foundRunTime = re.search(r'(Runtime[\s]*of[\s]*Entire[\s]*Timing[\s]*Run)[\s]*=+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if foundRunTime:
                if "pv max tttt" is stage:
                    rptData.foundRunTime_max[1] = FormatMetric.format_metric_values(foundRunTime.group(2))
                elif "pv min tttt" is stage:
                    rptData.foundRunTime_min[1] = FormatMetric.format_metric_values(foundRunTime.group(2))
                elif "pv power tttt" is stage:
                    rptData.foundRunTime_noise[1] = FormatMetric.format_metric_values(foundRunTime.group(2))
                elif "pv noise tttt" is stage:
                    rptData.foundRunTime_power[1] = FormatMetric.format_metric_values(foundRunTime.group(2))

        DataItems.append(tuple(rptData.foundRunTime_max))
        DataItems.append(tuple(rptData.foundRunTime_min))
        DataItems.append(tuple(rptData.foundRunTime_power))
        DataItems.append(tuple(rptData.foundRunTime_noise))

        return DataItems