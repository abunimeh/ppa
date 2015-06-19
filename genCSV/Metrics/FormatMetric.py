__author__ = ''


def format_metric_values(metric_value):
    import re
    try:
        hr_min_secs_frmt = re.search(r'[\d]+:[\d]+:[\d]+', metric_value)
        if hr_min_secs_frmt:
            metric_value = convert_to_seconds_format(metric_value)
    except TypeError:
        pass
    metric_value = two_point_float_format(metric_value)
    return metric_value


def convert_to_seconds_format(metric_value):
    try:
        metric_value = metric_value.replace(" ", "")
        hours, minutes, seconds = (float(time_units) for time_units in metric_value.split(":"))
        metric_value = (hours*60*60) + (minutes*60) + seconds
    except ValueError:
        print("Could not convert %s to secs" % metric_value)
        return metric_value
    return metric_value


def two_point_float_format(metric_value):
    try:
        metric_value = "{0:.2f}".format(float(metric_value))
    except ValueError:
        pass
    return metric_value

# @staticmethod
# def format_metric_names(metric_names):

# This method is used to basically replace the spaces in the given metric name with underscores
def replace_space(metric_name):
    import re
    new_name = re.sub(r'[\W]+', "_", metric_name)
    return new_name