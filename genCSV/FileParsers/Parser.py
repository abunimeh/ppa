__author__ = 'dcart_000'


class Parser(object):

    def get_file_lines(self):
        with open(self.file, "r") as f:
                # The variable "lines" is a list containing all lines
                lines = f.readlines()
        return lines

    @staticmethod
    def check_list(metric_list, metric_name):
        metric_in_list = True
        for metrics in metric_list:
            if metric_name == metrics[0]:
                metric_in_list = False
                break
        return metric_in_list

    @staticmethod
    def replace_space(metric_name):
        import re
        newName = re.sub(r'[\W]+', "_", metric_name)
        return newName