from FileParsers.Parser import Parser


class AprRunLog(Parser):
    def __init__(self, file):
        super(AprRunLog, self).__init__(file)

    # matchLine() takes the line that the method search_file() is looking for at the time and the keywords of the regular
    # expression. The method does the regular expression and returns it.
    @staticmethod
    def match_line(line, *args):
        import re
        # match_words will be the string of args with "[\s]*" replacing " "
        match_words = ""
        # no_match will be the string of args with no spaces
        no_match = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
            no_match += arg.replace(" ", "")
        match_words = match_words.replace("(", "\(")
        line_variables = '.*(%s)[^\d]*([-\d\.:]+).*' % (match_words)
        result = re.search(line_variables, line, re.I)
        return result


    def search_file(self):
        import re

        drc_violation_metric_name = self.replace_space('apr DRC Violations')
        run_time_metric_name = self.replace_space('apr Run TIME') + ' (secs)'
        kit_metric_name = "Kit"

        for line in self.get_file_lines():
            found_drc_vio = self.match_line(line, 'Total number of DRC violations')
            found_run_time = self.match_line(line, 'Ending "Encounter" (totcpu=')
            found_kit = re.search(r'(==>INFORMATION:[\s]*P_source_if_exists:[\s]*Sourcing)[\s]*.*/([afdkitcsr]+[afdkitcsr\._\d]+[_]+[afdkitcsr\._\d]*[^/])/',line)

            if found_drc_vio:
                if not self.check_list(drc_violation_metric_name):
                    self.metrics.append((drc_violation_metric_name, self.format_metric_values(found_drc_vio.group(2))))
            elif found_run_time:
                if not self.check_list(run_time_metric_name):
                    self.metrics.append((run_time_metric_name, self.format_metric_values(found_run_time.group(2))))
            elif found_kit:
                if not self.check_list(kit_metric_name):
                    self.metrics.append((kit_metric_name, found_kit.group(2)))
            if len(self.metrics) == 3:
                break