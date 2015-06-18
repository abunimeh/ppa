__author__ = ''


class CadenceViolationsData:
    pass


class CadenceViolations:
    @staticmethod
    def match_line(line, *args):
        import re
        match_words = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
        line_variables = '.*(%s)([-\d]*).*' % match_words
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    @staticmethod
    def search_file(file):
        import Metrics.FormatMetric as Format
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        # close the file after reading the lines.
        f.close()
        data_items = []
        viol_data = CadenceViolationsData()
        value_found = 0
        viol_data.found_max_trans = [CadenceViolations.replace_space('syn max trans viols'), "N/A"]
        viol_data.found_max_cap = [CadenceViolations.replace_space('syn max cap viols'), "N/A"]
        viol_data.found_max_fanout = [CadenceViolations.replace_space('syn max fanout viols'), "N/A"]

        for line in lines:
            found_max_trans = CadenceViolations.match_line(line, 'Max_transition design rule:')
            found_max_cap = CadenceViolations.match_line(line, 'Max_capacitance design rule:')
            found_max_fanout = CadenceViolations.match_line(line, 'Max_fanout design rule:')

            if found_max_trans:
                if found_max_trans.group(2) == '':
                    value_found = 0
                else:
                    value_found = Format.format_metric_values(found_max_trans.group(2))
                viol_data.found_max_trans[1] = value_found

            elif found_max_cap:
                if found_max_cap.group(2) == '':
                    value_found = 0
                else:
                    value_found = Format.format_metric_values(found_max_cap.group(2))
                viol_data.found_max_cap[1] = value_found

            elif found_max_fanout:
                if found_max_fanout.group(2) == '':
                    value_found = 0
                else:
                    value_found = Format.format_metric_values(found_max_fanout.group(2))
                viol_data.found_max_fanout[1] = value_found

        data_items.append(tuple(viol_data.found_max_trans))
        data_items.append(tuple(viol_data.found_max_cap))
        data_items.append(tuple(viol_data.found_max_fanout))

        return data_items