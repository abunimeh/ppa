__author__ = ''


class CadenceAprRunLogData:
    pass


class AprRunLog:
    # matchLine() takes the line that the method search_file() is looking for at the time and the keywords of the regular
    # expression. The method does the regular expression and returns it.
    @staticmethod
    def mathcLine(line, *args):
        import re
        # match_words will be the string of args with "[\s]*" replacing " "
        match_words = ""
        # no_match will be the string of args with no spaces
        no_match = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
            no_match += arg.replace(" ", "")
        match_words = match_words.replace("(", "\(")
        line_variables = '.*(%s)[^\d]*([-\d\.:]+).*' % (match_words)
        result = re.search(line_variables, line, re.I)
        return result

    # replace_space() replaces the empty spaces with underscores
    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    # check_list() checks to see if the metric has already been added to the list
    @staticmethod
    def check_list(metric_list, metric_name):
        metric_in_list = True
        for metrics in metric_list:
            if metric_name is metrics[0]:
                metric_in_list = False
        return metric_in_list

    # search_file() takes the file name given to it by
    @staticmethod
    def search_file(file):
        import re
        from Metrics.FormatMetric import FormatMetric
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()

        # close the file after reading the lines.
        f.close()
        data_items = []
        found_drc_violations = False
        run_log_data = CadenceAprRunLogData()
        formt = FormatMetric
        for line in reversed(lines):
            found_drc_vio = AprRunLog.mathcLine(line, 'Total number of DRC violations')
            found_run_time = AprRunLog.mathcLine(line, 'Ending "Encounter" (totcpu=')
            found_kit = re.search(r'(==>INFORMATION:[\s]*P_source_if_exists:[\s]*Sourcing)[\s]*.*/([afdkitcsr\._\d]+[_]+[afdkitcsr\._\d]*[^/])/',line)

            if found_drc_vio:
                run_log_data.found_drc_vio = AprRunLog.replace_space('apr DRC Violations'), formt.format_metric_values(found_drc_vio.group(2))
                if AprRunLog.check_list(data_items, run_log_data.found_drc_vio[0]):
                    data_items.append(run_log_data.found_drc_vio)
            elif found_run_time:
                run_log_data.found_run_time = AprRunLog.replace_space('apr Run Time') + ' (secs)', formt.format_metric_values(found_run_time.group(2))
                if AprRunLog.check_list(data_items, run_log_data.found_run_time[0]):
                    data_items.append(run_log_data.found_run_time)
            elif found_kit:
                run_log_data.found_kit = "Kit", found_kit.group(2)
                if AprRunLog.check_list(data_items, run_log_data.found_kit[0]):
                    data_items.append(run_log_data.found_kit)
            if len(data_items) == 3:
                break
        print(data_items)
        return data_items