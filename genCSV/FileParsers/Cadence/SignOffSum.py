__author__ = ''


class CadenceSignOffSumData:
    pass


class CadenceSignOffSum:
    @staticmethod
    def mathc_line(regex1, line):
        import re
        line_variables = '.*(%s)[^\|]*\|[^\|]*\|[\s]*([\d.]*).*' % regex1
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replace_space(metricname):
        import re
        new_name = re.sub(r'[\W]+', "_", metricname)
        return new_name

    @staticmethod
    def search_file(file):
        from Metrics.FormatMetric import FormatMetric

        print(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        data_items = []
        # close the file after reading the lines.
        f.close()
        formt = FormatMetric()
        s_o_sum = CadenceSignOffSumData()
        s_o_sum.found_wns = [CadenceSignOffSum.replace_space('apr REG2REG WNS'), "N/A"]
        s_o_sum.found_apr_tns = [CadenceSignOffSum.replace_space('apr REG2REG TNS'), "N/A"]
        s_o_sum.found_max_cap = [CadenceSignOffSum.replace_space('apr max cap viols'), "N/A"]
        s_o_sum.found_max_trans = [CadenceSignOffSum.replace_space('apr max trans viols'), "N/A"]

        for line in lines:
            found_wns = CadenceSignOffSum.mathc_line('WNS', line)
            found_tns = CadenceSignOffSum.mathc_line('TNS', line)
            found_max_cap = CadenceSignOffSum.mathc_line('max_cap', line)
            found_max_trans = CadenceSignOffSum.mathc_line('max_tran', line)

            if found_wns:
                s_o_sum.found_wns[1] = formt.format_metric_values(found_wns.group(2))
            elif found_tns:
                s_o_sum.found_apr_tns[1] = formt.format_metric_values(found_tns.group(2))
            elif found_max_cap:
                s_o_sum.found_max_cap[1] = formt.format_metric_values(found_max_cap.group(2))
            elif found_max_trans:
                s_o_sum.found_max_trans[1] = formt.format_metric_values(found_max_trans.group(2))

        data_items.append(tuple(s_o_sum.found_wns))
        data_items.append(tuple(s_o_sum.found_apr_tns))
        data_items.append(tuple(s_o_sum.found_max_cap))
        data_items.append(tuple(s_o_sum.found_max_trans))

        return data_items