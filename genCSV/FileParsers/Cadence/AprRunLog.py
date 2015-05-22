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
        line_variables = '.*(%s)[^%s\d]*([-\d\.:]+).*' % (match_words, no_match)
        result = re.search(line_variables, line, re.I)
        return result

    # replace_space() replaces the empty spaces with underscores
    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    # search_file() takes the file name given to it by
    @staticmethod
    def search_file(file):
        from OrganizingAndFormatingMetrics.FormatMetrics import FormatMetrics
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()

        # close the file after reading the lines.
        f.close()
        data_items = []
        found_drc_violations = False
        run_log_data = CadenceAprRunLogData()
        i = 0
        run_log_data.found_drc_vio = [AprRunLog.replace_space('apr DRC Violations'), "N/A"]
        run_log_data.found_run_time = [AprRunLog.replace_space('apr Run Time'), "N/A"]
        for line in reversed(lines):
            found_drc_vio = AprRunLog.mathcLine(line, 'Total number of DRC violations')
            found_run_time = AprRunLog.mathcLine(line, 'Ending "Encounter" (totcpu=')
            if found_drc_vio:
                run_log_data.found_drc_vio[1] = found_drc_vio.group(2)
                data_items.append(tuple(run_log_data.found_drc_vio))
            elif found_run_time:
                run_log_data.found_run_time[1] = found_run_time.group(2)
                data_items.append(tuple(run_log_data.found_run_time))
            if len(data_items) == 2:
                break

        return data_items