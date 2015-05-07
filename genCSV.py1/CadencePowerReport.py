__author__ = ''


class CadencePowerRptData:
    pass


class CadencePowerRpt:
    @staticmethod
    def mathcLine(line, *args):
        import re
        match_words = ""
        no_match = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
            no_match += arg.replace(" ", "")
        # print(match_words, no_match)
        line_variables = '.*(%s)[^%s\d]*([-\d\.]+).*' % (match_words, no_match)
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    @staticmethod
    def searchfile(file):
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()

        # close the file after reading the lines.
        f.close()
        data_items = []
        power_rpt_data = CadencePowerRptData()
        power_rpt_data.found_power_internal = [CadencePowerRpt.replace_space('apr Power Internal'), "N/A"]
        power_rpt_data.found_power_switching = [CadencePowerRpt.replace_space('apr Power Switching'), "N/A"]
        power_rpt_data.found_power_leakage = [CadencePowerRpt.replace_space('apr Power Leakage'), "N/A"]
        power_rpt_data.found_power_total = [CadencePowerRpt.replace_space('apr Power Total'), "N/A"]

        for line in lines:
            found_power_internal = CadencePowerRpt.mathcLine(line, 'Total', 'Internal', 'Power')
            found_power_switching = CadencePowerRpt.mathcLine(line, 'Total', 'Switching', 'Power')
            found_power_leakage = CadencePowerRpt.mathcLine(line, 'Total', 'Leakage', 'Power')
            found_power_total = CadencePowerRpt.mathcLine(line, 'Total', 'Power')

            if found_power_internal:
                power_rpt_data.found_power_internal[1] = found_power_internal.group(2)
            elif found_power_switching:
                power_rpt_data.found_power_switching[1] = found_power_switching.group(2)
            elif found_power_leakage:
                power_rpt_data.found_power_leakage[1] = found_power_leakage.group(2)
            elif found_power_total:
                power_rpt_data.found_power_total[1] = found_power_total.group(2)

        data_items.append(tuple(power_rpt_data.found_power_internal))
        data_items.append(tuple(power_rpt_data.found_power_switching))
        data_items.append(tuple(power_rpt_data.found_power_leakage))
        data_items.append(tuple(power_rpt_data.found_power_total))

        return data_items