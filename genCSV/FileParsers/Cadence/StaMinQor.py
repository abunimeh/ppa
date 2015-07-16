__author__ = ''

from FileParsers.Parser import Parser


class StaMinQor(Parser):
    def __init__(self, file):
        super(StaMinQor, self).__init__(file)
    @staticmethod
    def match_line(line, regex1):
        import re
        match_word = regex1.replace(" ", "[\s]*")
        line_variables = '.*(%s)[\s]*([-\d\.]*).*' % match_word
        result = re.search(line_variables, line)
        return result

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    def search_file(self):
        import Metrics.FormatMetric as Format

        found_section = False

        for line in self.get_file_lines():
            found_reg2reg_section = StaMinQor.match_line(line, "Timing Path Group 'REG2REG' \(min_delay\/hold\)")
            found_hold_viol = StaMinQor.match_line(line, 'Critical Path Slack:')
            found_min_tns = StaMinQor.match_line(line, 'Total Negative Slack:')
            found_next_section = StaMinQor.match_line(line, 'Timing Path Group')

            if found_reg2reg_section:
                found_section = True
            elif found_section:
                if found_hold_viol:
                    self.metrics.append((StaMinQor.replace_space('sta min tttt REG2REG worst hold viols'),
                                         Format.format_metric_values(found_hold_viol.group(2))))
                elif found_min_tns:
                    self.metrics.append((StaMinQor.replace_space('sta min tttt REG2REG TNS'),
                                         Format.format_metric_values(found_min_tns.group(2))))
                elif found_next_section:
                    found_section = False
