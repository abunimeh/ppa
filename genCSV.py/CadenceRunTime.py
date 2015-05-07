__author__ = ''


class CadenceRunTimeData:
    pass


class CadenceRunTime:
    @staticmethod
    def mathcLine(line, *args):
        import re
        match_words = ""
        no_match = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
        line_variables = '.*(%s)[\D]*([-\d\:]*).*' % match_words
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    @staticmethod
    def search_file(file):
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        # close the file after reading the lines.
        f.close()
        data_items = []
        run_time_data = CadenceRunTimeData()
        run_time_data.found_run_time = [CadenceRunTime.replace_space('sta Run Time'), "N/A"]

        for line in lines:
            found_run_time = CadenceRunTime.mathcLine(line, 'Ending "Tempus Timing Signoff Solution"')

            if found_run_time:
                run_time_data.found_run_time[1] = found_run_time.group(2)

        data_items.append(tuple(run_time_data.found_run_time))

        return data_items