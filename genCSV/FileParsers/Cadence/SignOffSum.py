__author__ = ''


class CadenceSignOffSumData:
    pass


class CadenceSignOffSum:
    @staticmethod
    def mathcLine(regex1, line):
        import re
        line_variables = '.*(%s)[^\|]*\|[^\|]*\|[\s]*([\d.]*).*' % regex1
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replaceSpace(metricname):
        import re
        new_name = re.sub(r'[\W]+', "_", metricname)
        return new_name

    @staticmethod
    def search_file(file):
        from OrganizingAndFormatingMetrics.FormatMetrics import FormatMetrics
        print(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        data_items = []
        # close the file after reading the lines.
        f.close()
        s_o_sum = CadenceSignOffSumData()
        s_o_sum.found_wns = [CadenceSignOffSum.replaceSpace('apr REG2REG WNS'), "N/A"]
        s_o_sum.found_apr_tns = [CadenceSignOffSum.replaceSpace('apr REG2REG TNS'), "N/A"]
        s_o_sum.found_max_cap = [CadenceSignOffSum.replaceSpace('apr max cap viols'), "N/A"]
        s_o_sum.found_max_trans = [CadenceSignOffSum.replaceSpace('apr max trans viols'), "N/A"]

        for line in lines:
            found_wns = CadenceSignOffSum.mathcLine('WNS', line)
            found_tns = CadenceSignOffSum.mathcLine('TNS', line)
            found_max_cap = CadenceSignOffSum.mathcLine('max_cap', line)
            found_max_trans = CadenceSignOffSum.mathcLine('max_tran', line)

            if found_wns:
                s_o_sum.found_wns[1] = FormatMetrics.format_metric_values(found_wns.group(2))
            elif found_tns:
                s_o_sum.found_apr_tns[1] = FormatMetrics.format_metric_values(found_tns.group(2))
            elif found_max_cap:
                s_o_sum.found_max_cap[1] = FormatMetrics.format_metric_values(found_max_cap.group(2))
            elif found_max_trans:
                s_o_sum.found_max_trans[1] = FormatMetrics.format_metric_values(found_max_trans.group(2))

        data_items.append(tuple(s_o_sum.found_wns))
        data_items.append(tuple(s_o_sum.found_apr_tns))
        data_items.append(tuple(s_o_sum.found_max_cap))
        data_items.append(tuple(s_o_sum.found_max_trans))

        return data_items