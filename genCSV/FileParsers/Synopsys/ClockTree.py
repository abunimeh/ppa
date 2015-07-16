class clockTreeRptData:
    pass

from FileParsers.Parser import Parser


class ClockTreeReport(Parser):
    def __init__(self, file):
        super(ClockTreeReport, self).__init__(file)

    def search_file(self):
        import re
        import Metrics.FormatMetric as Format
        lines = self.get_file_lines()
        # rptData = clockTreeRptData()
        max_global_skew_name = "apr_cts_max_global_skew"

        for line in lines:
            found_max_globe_skew = re.search(r'(Max[\s]*global[\s]*skew)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
            if found_max_globe_skew:
                # rptData.foundMaxGlobeSkew = "apr_cts_max_global_skew", Format.format_metric_values(found_max_globe_skew.group(2))
                self.metrics.append((max_global_skew_name, Format.format_metric_values(found_max_globe_skew.group(2))))
                break