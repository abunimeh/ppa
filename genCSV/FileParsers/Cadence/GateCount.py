from FileParsers.Parser import Parser


class CadenceGateCount(Parser):
    def __init__(self, file):
        super(CadenceGateCount, self).__init__(file)

    @staticmethod
    def match_line(regex1, line):
        import re
        keyword = regex1.replace(" ", "")
        line_variables = '.*(%s)[^%s\d]*([-\d\.]*).*' % (regex1, keyword)
        result = re.search(line_variables, line, re.I)
        return result

    def search_file(self):

        cell_count_metric_name = self.replace_space('apr Cell Count')
        found_utilization_metric_name = self.replace_space('apr utilization') + " (%)"

        for line in self.get_file_lines():
            found_cell_count = self.match_line('Inst count', line)
            found_utilization = self.match_line('Density', line)

            if found_utilization:
                self.metrics.append((found_utilization_metric_name, self.format_metric_values(float(found_utilization.group(2))*100)))
            else:
                self.add_to_metrics(found_cell_count, cell_count_metric_name)

