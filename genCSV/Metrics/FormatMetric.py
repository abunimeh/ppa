__author__ = ''


class FormatMetric:
    @staticmethod
    def format_metric_values(metric_value):
        import re
        try:
            hr_min_secs_frmt = re.search(r'[\d]+:[\d]+:[\d]+', metric_value)
            if hr_min_secs_frmt:
                metric_value = FormatMetric.convert_to_seconds_format(metric_value)
        except TypeError:
            pass
        metric_value = FormatMetric.two_point_float_format(metric_value)
        return metric_value

    @staticmethod
    def convert_to_seconds_format(metric_value):
        import time
        from datetime import timedelta
        try:
            temp_time = time.strptime(metric_value, '%H:%M:%S')
            metric_value = timedelta(hours=temp_time.tm_hour, minutes=temp_time.tm_min, seconds=temp_time.tm_sec).total_seconds()
        except ValueError:
            print("Could not convert %s to secs__" % metric_value)
        return metric_value

    @staticmethod
    def two_point_float_format(metric_value):
        try:
            metric_value = "{0:.2f}".format(float(metric_value))
        except ValueError:
            pass
        return metric_value

    # @staticmethod
    # def format_metric_names(metric_names):


    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name