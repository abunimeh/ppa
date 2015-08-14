from FileParsers.Parser import Parser


class PowerReport(Parser):
    def __init__(self, file):
        super(PowerReport, self).__init__(file)

    @staticmethod
    def match_line(line, *args):
        import re
        match_words = ""
        no_match = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
            no_match += arg.replace(" ", "")
        line_variables = '.*(%s)[^%s\d]*([-\d\.]+).*' % (match_words, no_match)
        result = re.search(line_variables, line, re.I)
        return result

    def search_file(self):

        internal_metric_name = self.replace_space('apr Power Internal')
        switching_metric_name = self.replace_space('apr Power Switching')
        leakage_metric_name = self.replace_space('apr Power Leakage')
        total_metric_name = self.replace_space('apr Power Total')

        for line in self.get_file_lines():
            found_power_internal = self.match_line(line, 'Total', 'Internal', 'Power')
            if self.add_to_metrics(found_power_internal, internal_metric_name):
                continue

            found_power_switching = self.match_line(line, 'Total', 'Switching', 'Power')
            if self.add_to_metrics(found_power_switching, switching_metric_name):
                continue

            found_power_leakage = self.match_line(line, 'Total', 'Leakage', 'Power')
            if self.add_to_metrics(found_power_leakage, leakage_metric_name):
                continue

            found_power_total = self.match_line(line, 'Total', 'Power')
            if self.add_to_metrics(found_power_total, total_metric_name):
                continue

