__author__ = ''


class CadenceStaMinQorData:
    pass


class CadenceStaMinQor:
    @staticmethod
    def mathcLine(line, regex1):
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
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        # close the file after reading the lines.
        f.close()
        data_items = []
        found_section = False
        sta_min_qor_data = CadenceStaMinQorData()
        sta_min_qor_data.found_hold_viol = [CadenceStaMinQor.replace_space('sta min tttt REG2REG worst hold viols'), "N/A"]
        sta_min_qor_data.found_min_tns = [CadenceStaMinQor.replace_space('sta min tttt REG2REG TNS'), "N/A"]

        for line in lines:
            found_reg2reg_section = CadenceStaMinQor.mathcLine(line, "Timing Path Group 'REG2REG' \(min_delay\/hold\)")
            found_hold_viol = CadenceStaMinQor.mathcLine(line, 'Critical Path Slack:')
            found_min_tns = CadenceStaMinQor.mathcLine(line, 'Total Negative Slack:')
            found_next_section = CadenceStaMinQor.mathcLine(line, 'Timing Path Group')

            if found_reg2reg_section:
                found_section = True
            elif found_section:
                if found_hold_viol:
                    sta_min_qor_data.found_hold_viol[1] = found_hold_viol.group(2)
                elif found_min_tns:
                    sta_min_qor_data.found_min_tns[1] = found_min_tns.group(2)
                elif found_next_section:
                    found_section = False

        data_items.append(tuple(sta_min_qor_data.found_hold_viol))
        data_items.append(tuple(sta_min_qor_data.found_min_tns))

        return data_items