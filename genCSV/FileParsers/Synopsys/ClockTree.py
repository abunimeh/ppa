from FileParsers.Parser import Parser


class ClockTreeReport(Parser):
    def __init__(self, file):
        super(ClockTreeReport, self).__init__(file)

    def search_file(self):
        import re
        max_global_skew_name = "apr_cts_max_global_skew"

        for line in self.get_file_lines():
            found_max_globe_skew = re.search(r'(Max[\s]*global[\s]*skew)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
            if self.add_to_metrics(found_max_globe_skew, max_global_skew_name):
                break