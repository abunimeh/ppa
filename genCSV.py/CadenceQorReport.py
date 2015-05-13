__author__ = ''


class CadenceQorReportData:
    pass


class CadenceQorReport:
    @staticmethod
    def mathcLine(line, *args):
        import re
        match_words = ""
        no_match = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
        line_variables = '^(%s)[\s]*([-\d\.:]+)[\s]*([-\d\.:]*).*' % match_words
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    @staticmethod
    def search_file(file):
        # Open the file with read only permit
        with open(file, "r") as lines:
            # # The variable "lines" is a list containing all lines
            # lines = f.readlines()
            #
            # # close the file after reading the lines.
            # f.close()
            data_items = []
            qor_rpt_data = CadenceQorReportData()
            qor_rpt_data.found_syn_wns = [CadenceQorReport.replace_space('syn REG2REG WNS'), "N/A"]
            qor_rpt_data.found_syn_tns = [CadenceQorReport.replace_space('syn REG2REG TNS'), "N/A"]
            qor_rpt_data.found_cell_count = [CadenceQorReport.replace_space('syn Cell Count'), "N/A"]
            qor_rpt_data.found_runtime = [CadenceQorReport.replace_space('syn cpu runtime'), "N/A"]
            for line in lines:
                found_syn_reg = CadenceQorReport.mathcLine(line, 'REG2REG')
                found_cell_count = CadenceQorReport.mathcLine(line, 'Leaf Instance Count')
                found_runtime = CadenceQorReport.mathcLine(line, 'Runtime')

                if found_syn_reg:
                    qor_rpt_data.found_syn_wns[1] = found_syn_reg.group(2)
                    qor_rpt_data.found_syn_tns[1] = found_syn_reg.group(3)
                elif found_cell_count:
                    qor_rpt_data.found_cell_count[1] = found_cell_count.group(2)
                elif found_runtime:
                    qor_rpt_data.found_runtime[1] = found_runtime.group(2)

        data_items.append(tuple(qor_rpt_data.found_syn_wns))
        data_items.append(tuple(qor_rpt_data.found_syn_tns))
        data_items.append(tuple(qor_rpt_data.found_cell_count))
        data_items.append(tuple(qor_rpt_data.found_runtime))

        return data_items