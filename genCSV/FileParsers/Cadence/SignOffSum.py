from FileParsers.Parser import Parser


class CadenceSignOffSum(Parser):
    def __init__(self, file):
        super(CadenceSignOffSum, self).__init__(file)

    @staticmethod
    def match_line(regex1, line):
        import re
        line_variables = '.*(%s)[^\|]*\|[^\|]*\|[\s]*([\d.]*).*' % regex1
        result = re.search(line_variables, line, re.I)
        return result

    def search_file(self):

        wns_metric_name = self.replace_space('apr REG2REG WNS')
        apr_tns_metric_name = self.replace_space('apr REG2REG TNS')
        max_cap_metric_name = self.replace_space('apr max cap viols')
        max_trans_metric_name = self.replace_space('apr max trans viols')

        for line in self.get_file_lines():
            found_wns = self.match_line('WNS', line)
            found_tns = self.match_line('TNS', line)
            found_max_cap = self.match_line('max_cap', line)
            found_max_trans = self.match_line('max_tran', line)

            if self.add_to_metrics(found_wns, wns_metric_name):
                pass
            elif self.add_to_metrics(found_tns, apr_tns_metric_name):
                self.metrics.append((apr_tns_metric_name, self.format_metric_values(found_tns.group(2))))
            elif self.add_to_metrics(found_max_cap, max_cap_metric_name):
                self.metrics.append((max_cap_metric_name, self.format_metric_values(found_max_cap.group(2))))
            elif self.add_to_metrics(found_max_trans, max_trans_metric_name):
                self.metrics.append((max_trans_metric_name, self.format_metric_values(found_max_trans.group(2))))