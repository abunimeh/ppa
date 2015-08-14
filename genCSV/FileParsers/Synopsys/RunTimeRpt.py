class RunTimeRptData:
    pass

from FileParsers.Parser import Parser


class RunTimeRpt(Parser):
    def __init__(self, file):
        super(RunTimeRpt, self).__init__(file)

    # metric_stage_name() finds the stage of the temp_metric_collection and returns the name
    def metric_naming(self):
        import re
        stage = ""
        pv_max = re.search(r'.*pv.*max.*|.*sta.*max.*', self.file, re.I)
        pv_min = re.search(r'.*pv.*min.*|.*sta.*min.*', self.file, re.I)
        pv_power = re.search(r'.*pv.*power.*|.*sta.*power.*', self.file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*|.*sta.*noise.*', self.file, re.I)
        if pv_max:
            stage = 'pv max tttt'
        elif pv_min:
            stage = 'pv min tttt'
        elif pv_power:
            stage = 'pv power tttt'
        elif pv_noise:
            stage = 'pv noise tttt'
        return stage

    # search_file() opens the file sent to it and searches for the specified metrics
    def search_file(self):
        import re

        stage = self.metric_naming(self.file)

        for line in self.get_file_lines():
            found_run_time = re.search(r'(Runtime[\s]*of[\s]*Entire[\s]*Timing[\s]*Run)[\s]*=+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if self.add_to_metrics(found_run_time, self.replace_space(stage + " run TIME") + " (secs)"):
                break
                # self.metrics.append(,
                #                     self.format_metric_values(found_run_time.group(2)))
