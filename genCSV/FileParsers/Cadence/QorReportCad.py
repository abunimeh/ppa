from FileParsers.Parser import Parser


class CadenceQorReport(Parser):
    def __init__(self, file):
        super(CadenceQorReport, self).__init__(file)

    @staticmethod
    def match_line(line, *args):
        import re
        match_words = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
        line_variables = '^(%s)[^\d-]*([-\d\.:]+)[\s]*([-\d\.:]*).*' % match_words
        result = re.search(line_variables, line, re.I)
        return result

    def search_file(self):

        syn_wns_metric_name = self.replace_space('syn REG2REG WNS')
        syn_tns_metric_name = self.replace_space('syn REG2REG TNS')
        cell_count_metric_name = self.replace_space('syn Cell Count')
        runtime_metric_name = self.replace_space('syn cpu runTIME')+" (secs)"

        for line in self.get_file_lines():
            found_syn_reg = self.match_line(line, 'REG2REG')
            found_cell_count = self.match_line(line, 'Leaf Instance Count')
            found_runtime = self.match_line(line, 'Runtime')

            if found_syn_reg:
                self.metrics.append((syn_wns_metric_name, self.format_metric_values(found_syn_reg.group(2))))
                self.metrics.append((syn_tns_metric_name, self.format_metric_values(found_syn_reg.group(3))))
            elif self.add_to_metrics(found_cell_count, cell_count_metric_name):
                pass
            elif self.add_to_metrics(found_runtime, runtime_metric_name):
                pass


