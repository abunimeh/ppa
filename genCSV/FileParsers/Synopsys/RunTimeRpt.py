class RunTimeRptData:
    pass

from FileParsers.Parser import Parser


class RunTimeRpt(Parser):
    def __init__(self, file):
        super(RunTimeRpt, self).__init__(file)

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

    # search_file() opens the file sent to it and searches for the specified temp_metric_collection
    def search_file(self):
        import re
        import Metrics.FormatMetric as Format

        stage = RunTimeRpt.metric_naming(self.file)
        lines = self.get_file_lines()
        DataItems = []
        rptData = RunTimeRptData()
        # rptData.foundRunTime_max = [Format.replace_space("pv max tttt" + " run time")+" (secs)", "N/A"]
        # rptData.foundRunTime_min = [Format.replace_space("pv min tttt" + " run time")+" (secs)", "N/A"]
        # rptData.foundRunTime_noise = [Format.replace_space("pv noise tttt" + " run time")+" (secs)", "N/A"]
        # rptData.foundRunTime_power = [Format.replace_space("pv power tttt" + " run time")+" (secs)", "N/A"]

        for line in lines:
            found_run_time = re.search(r'(Runtime[\s]*of[\s]*Entire[\s]*Timing[\s]*Run)[\s]*=+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if found_run_time:
                self.metrics.append((Format.replace_space(stage + " run time") + " (secs)"),
                                    Format.format_metric_values(found_run_time.group(2)))
        #         if "pv max tttt" == stage:
        #             rptData.foundRunTime_max[1] = Format.format_metric_values(found_run_time.group(2))
        #         elif "pv min tttt" == stage:
        #             rptData.foundRunTime_min[1] = Format.format_metric_values(found_run_time.group(2))
        #         elif "pv power tttt" == stage:
        #             rptData.foundRunTime_noise[1] = Format.format_metric_values(found_run_time.group(2))
        #         elif "pv noise tttt" == stage:
        #             rptData.foundRunTime_power[1] = Format.format_metric_values(found_run_time.group(2))
        #
        # self.metrics.append(tuple(rptData.foundRunTime_max))
        # self.metrics.append(tuple(rptData.foundRunTime_min))
        # self.metrics.append(tuple(rptData.foundRunTime_power))
        # self.metrics.append(tuple(rptData.foundRunTime_noise))
