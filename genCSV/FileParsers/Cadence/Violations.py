__author__ = ''

from FileParsers.Parser import Parser


class CadenceViolations(Parser):
    def __init__(self, file):
        super(CadenceViolations, self).__init__(file)

    @staticmethod
    def match_line(line, *args):
        import re
        match_words = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
        line_variables = '.*(%s)([-\d]*).*' % match_words
        result = re.search(line_variables, line, re.I)
        return result

    def search_file(self):
        value_found = 0
        for line in self.get_file_lines():
            found_max_trans = self.match_line(line, 'Max_transition design rule:')
            found_max_cap = self.match_line(line, 'Max_capacitance design rule:')
            found_max_fanout = self.match_line(line, 'Max_fanout design rule:')

            if found_max_trans:
                if found_max_trans.group(2) == '':
                    value_found = 0
                else:
                    value_found = self.format_metric_values(found_max_trans.group(2))
                self.metrics.append((self.replace_space('syn max trans viols'), value_found))
            elif found_max_cap:
                if found_max_cap.group(2) == '':
                    value_found = 0
                else:
                    value_found = self.format_metric_values(found_max_cap.group(2))
                self.metrics.append((self.replace_space('syn max cap viols'), value_found))
            elif found_max_fanout:
                if found_max_fanout.group(2) == '':
                    value_found = 0
                else:
                    value_found = self.format_metric_values(found_max_fanout.group(2))
                self.metrics.append((self.replace_space('syn max fanout viols'), value_found))