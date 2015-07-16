class FinalRptData:
    pass
from FileParsers.Parser import Parser


class FinalReport(Parser):
    def __init__(self, file):
        super(FinalReport, self).__init__(file)

    def metric_naming(self):
        import re
        stage = ""
        denall = re.search(r'.*denall.*', self.file, re.I)
        ipall = re.search(r'.*ipall.*', self.file, re.I)
        drcd = re.search(r'.*drcd.*', self.file, re.I)
        trclvs = re.search(r'.*trclvs.*', self.file, re.I)
        if denall:
            stage = 'drc denall'
        if ipall:
            stage = 'drc IPall'
        if drcd:
            stage = 'drc drcd'
        if trclvs:
            stage = 'drc trclvs'
        return stage

    def search_file(self):
        import re
        import Metrics.FormatMetric as Format
        stage = self.metric_naming()
        lines = self.get_file_lines()
        rptData = FinalRptData()
        violation_name = Format.replace_space(stage) + " (NB)"

        for line in lines:
            found_violation = re.search(r'(The[\s]*number[\s]*of[\s]*actual[\s]*errors)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
            if found_violation:
                self.metrics.append((violation_name, Format.format_metric_values(found_violation.group(2))))
                break
