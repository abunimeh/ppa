__author__ = ''


class CadenceGateCountData:
    pass


class CadenceGateCount:
    @staticmethod
    def mathcLine(regex1, line):
        import re
        keyword = regex1.replace(" ", "")
        line_variables = '.*(%s)[^%s\d]*([-\d\.]*).*' % (regex1, keyword)
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
        gate_count = CadenceGateCountData()

        gate_count.found_cell_count = [CadenceGateCount.replace_space('apr Cell Count'), "N/A"]
        gate_count.found_utilization = [CadenceGateCount.replace_space('apr utilization') + " (%)", "N/A"]

        for line in lines:
            found_cell_count = CadenceGateCount.mathcLine('Inst count', line)
            found_utilization = CadenceGateCount.mathcLine('Density', line)
            if found_cell_count:
                gate_count.found_cell_count[1] = Format.format_metric_values(found_cell_count.group(2))
            elif found_utilization:
                gate_count.found_utilization[1] = Format.format_metric_values(float(found_utilization.group(2))*100) #"{0:.2f}".format(float(found_utilization.group(2))*100)

        data_items.append(tuple(gate_count.found_cell_count))
        data_items.append(tuple(gate_count.found_utilization))
        return data_items