__author__ = 'dcart_000'


class Parser(object):
    def __init__(self, file):
        self.metrics = []
        self.file = file

    def get_file_lines(self):
        # Open the file with read only permit
        with open(self.file, "r") as f:
                # The variable "lines" is a list containing all lines
                lines = f.readlines()
        return lines

    def check_list(self, metric_name):
        metric_in_list = False
        for metric_pair in self.metrics:
            if metric_name == metric_pair[0]:
                metric_in_list = True
                break
        return metric_in_list

    def add_to_metrics(self, metric_regexp, metric_name):
        import Metrics.FormatMetric as Format
        if metric_regexp:
            self.metrics.append((metric_name, Format.format_metric_values(metric_regexp.group(2))))

    @staticmethod
    def replace_space(metric_name):
        import re
        formatted_name = re.sub(r'[\W]+', "_", metric_name)
        return formatted_name