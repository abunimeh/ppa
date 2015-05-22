__author__ = ''

class FormatMetrics:
    @staticmethod
    def format_metric_values(metric_value):
        try:
            metric_value = "{0:.2f}".format(float(metric_value))
        except ValueError:
            metric_value = metric_value
        return metric_value

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name