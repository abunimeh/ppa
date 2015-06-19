__author__ = ''


class CadenceStaMaxQorData:
    pass


class StaMaxQor:
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
        found_section = False
        sta_max_qor_data = CadenceStaMaxQorData()

        for line in lines:
            found_reg2reg_section = StaMaxQor.match_line(line, "Timing Path Group 'REG2REG' \(max_delay\/setup\)")
            found_crit_path = StaMaxQor.match_line(line, 'Critical Path Slack:')
            found_total_neg_slack = StaMaxQor.match_line(line, 'Total Negative Slack:')
            found_cell_count = StaMaxQor.match_line(line, 'Leaf Cell Count:')
            found_max_trans_count = StaMaxQor.match_line(line, 'max_transition Count:')
            found_max_cap_count = StaMaxQor.match_line(line, 'max_capacitance Count:')
            found_next_section = StaMaxQor.match_line(line, 'Timing Path Group')

            if found_reg2reg_section:
                found_section = True
            elif found_section:
                if found_crit_path:
                    sta_max_qor_data.found_crit_path = Format.replace_space('sta max tttt REG2REG worst setup viols'),\
                                                       Format.format_metric_values(found_crit_path.group(2))
                    data_items.append(sta_max_qor_data.found_crit_path)
                elif found_total_neg_slack:
                    sta_max_qor_data.found_total_neg_slack = Format.replace_space('sta max tttt REG2REG TNS'),\
                                                             Format.format_metric_values(found_total_neg_slack.group(2))
                    data_items.append(sta_max_qor_data.found_total_neg_slack)
                elif found_next_section:
                    found_section = False
            elif found_cell_count:
                sta_max_qor_data.found_cell_count = Format.replace_space('sta Cell Count'), Format.format_metric_values(found_cell_count.group(2))
                data_items.append(sta_max_qor_data.found_cell_count)
            elif found_max_trans_count:
                sta_max_qor_data.found_max_trans_count = Format.replace_space('sta max trans viols'), \
                                                         Format.format_metric_values(found_max_trans_count.group(2))
                data_items.append(sta_max_qor_data.found_max_trans_count)
            elif found_max_cap_count:
                sta_max_qor_data.found_max_cap_count = Format.replace_space('sta max cap viols'),\
                                                       Format.format_metric_values(found_max_cap_count.group(2))
                data_items.append(sta_max_qor_data.found_max_cap_count)

        return data_items