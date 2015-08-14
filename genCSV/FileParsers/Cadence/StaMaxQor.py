from FileParsers.Parser import Parser


class StaMaxQor(Parser):
    def __init__(self, file):
        super(StaMaxQor, self).__init__(file)

    @staticmethod
    def match_line(line, regex1):
        import re
        match_word = regex1.replace(" ", "[\s]*")
        line_variables = '.*(%s)[\s]*([-\d\.]*).*' % match_word
        result = re.search(line_variables, line)
        return result

    def search_file(self):
        found_section = False

        worst_setup_violations_metric_name = self.replace_space('sta max tttt REG2REG worst setup viols')
        total_negative_slack_metric_name = self.replace_space('sta max tttt REG2REG TNS')
        cell_count_metric_name = self.replace_space('sta Cell Count')
        max_transition_count_metric_name = self.replace_space('sta max trans viols')
        max_capacitance_count_metric_name = self.replace_space('sta max cap viols')

        for line in self.get_file_lines():
            found_reg2reg_section = self.match_line(line, "Timing Path Group 'REG2REG' \(max_delay\/setup\)")
            found_worst_setup_violations = self.match_line(line, 'Critical Path Slack:')
            found_total_neg_slack = self.match_line(line, 'Total Negative Slack:')
            found_cell_count = self.match_line(line, 'Leaf Cell Count:')
            found_max_trans_count = self.match_line(line, 'max_transition Count:')
            found_max_cap_count = self.match_line(line, 'max_capacitance Count:')
            found_next_section = self.match_line(line, 'Timing Path Group')

            if found_reg2reg_section:
                found_section = True
            elif found_section:
                if found_worst_setup_violations:
                    self.metrics.append((worst_setup_violations_metric_name, self.format_metric_values(found_worst_setup_violations.group(2))))
                elif found_total_neg_slack:
                    self.metrics.append((total_negative_slack_metric_name, self.format_metric_values(found_total_neg_slack.group(2))))
                elif found_next_section:
                    found_section = False
            elif found_cell_count:
                self.metrics.append((cell_count_metric_name, self.format_metric_values(found_cell_count.group(2))))
            elif found_max_trans_count:
                self.metrics.append((max_transition_count_metric_name, self.format_metric_values(found_max_trans_count.group(2))))
            elif found_max_cap_count:
                self.metrics.append((max_capacitance_count_metric_name, self.format_metric_values(found_max_cap_count.group(2))))
