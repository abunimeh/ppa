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
        if metric_regexp:
            self.metrics.append((metric_name, self.format_metric_values(metric_regexp.group(2))))
            return True
        else:
            return False

    # This method is used to basically replace the spaces in the given metric name with underscores
    @staticmethod
    def replace_space(metric_name):
        import re
        formatted_name = re.sub(r'[\W]+', "_", metric_name)
        return formatted_name

    def format_metric_values(self, metric_value):
        import re
        try:
            hr_min_secs_frmt = re.search(r'[\d]+:[\d]+:[\d]+', metric_value)
            if hr_min_secs_frmt:
                metric_value = self.convert_to_seconds_format(metric_value)
        except TypeError:
            pass
        metric_value = self.two_point_float_format(metric_value)
        return metric_value

    @staticmethod
    def convert_to_seconds_format(metric_value):
        try:
            metric_value = metric_value.replace(" ", "")
            hours, minutes, seconds = (float(time_units) for time_units in metric_value.split(":"))
            metric_value = (hours*60*60) + (minutes*60) + seconds
        except ValueError:
            print("Could not convert %s to secs" % metric_value)
            return metric_value
        return metric_value

    @staticmethod
    def two_point_float_format(metric_value):
        try:
            metric_value = "{0:.2f}".format(float(metric_value))
        except ValueError:
            pass
        return metric_value