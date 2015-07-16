from FileParsers.Parser import Parser


class QorReport(Parser):
    def __init__(self, file):
        super(QorReport, self).__init__(file)

    # This method is used to find and return the stage(e.g. "syn" or "py") by using the file name that was passed into
    # the method search_file. The method then uses regular expressions to find and return the stage name.
    def metric_stage_name(self):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', self.file, re.I)
        apr = re.search(r'.*apr.*', self.file, re.I)
        pv_max = re.search(r'.*pv.*max.*', self.file, re.I)
        pv_min = re.search(r'.*pv.*min.*', self.file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', self.file, re.I)
        if apr:
            stage = 'apr'
        elif pv_max:
            stage = 'pv max tttt'
        elif pv_min:
            stage = 'pv min tttt'
        elif pv_noise:
            stage = 'pv noise tttt'
        elif syn:
            stage = 'syn'
        return stage

    # @staticmethod is put before methods when the self variable won't be used in the method
    # This method is what is used to do the regular expression on the lines of the file. The method simply takes in
    # the three first arguments as the names for the regular expression and the fourth argument as the line the
    # regular expression will search.
    @staticmethod
    def match_line(regex1, regex2, regex3, file_line):
        import re
        line_variables = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*([-\d\.]*)+.*' % (regex1, regex2, regex3)
        result = re.search(line_variables, file_line, re.I)
        return result

    # This method is used to search the given file and retrieve the required metrics out of those files
    def search_file(self):
        import re
        import Metrics.FormatMetric as Format

        stage = self.metric_stage_name()
        # in_reg2reg_section is used to search a certain amount after reg2reg
        in_reg2reg_section = False

        # Loop through each line to find the metrics
        for line in self.get_file_lines():
            found_reg_group = re.search(r'.*(REG2REG).*', line, re.I)
            found_version = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
            if found_version:
                # Regular expression method 'search' returns the found regular expressions back in groups designated by
                # the parentheses in the regular expression
                self.metrics.append((Format.replace_space(stage + " tool version"), found_version.group(2)))
            # If we found the line that contains the word REG2REG then we set 'in_reg2reg_section' to True
            elif found_reg_group:
                if 'pv max tttt' in stage:
                    if 'max_delay/setup' in line:
                        in_reg2reg_section = True
                elif 'pv min tttt' in stage:
                    if 'min_delay/hold' in line:
                        in_reg2reg_section = True
                else:
                    in_reg2reg_section = True

            # If 'in_reg2reg_section' is true and the stage is not 'pv noise tttt' then search for the certain metrics that are
            # found in that section
            elif in_reg2reg_section and stage != 'pv noise tttt':
                found_crit_slack = QorReport.match_line("Critical", "path", "slack", line)
                found_worst_hold_vio = QorReport.match_line("Worst", "hold", "violation", line)
                found_crit_path_length = QorReport.match_line("critical", "path", "length", line)
                found_tot_neg_slack = QorReport.match_line("total", "Negative", "slack", line)
                found_tot_hold_vio = QorReport.match_line("total", "hold", "violation", line)
                found_new_section = re.search(r'.*Timing[\s]*Path[\s]*Group.*', line, re.I)

                if found_crit_slack:
                    if 'pv min' in stage:
                        self.metrics.append((Format.replace_space(stage + " REG2REG " + "worst hold viol"),
                                             Format.format_metric_values(found_crit_slack.group(2))))
                    else:
                        self.metrics.append((Format.replace_space(stage + " REG2REG " + "worst setup viol"),
                                             Format.format_metric_values(found_crit_slack.group(2))))
                elif found_worst_hold_vio:
                    self.metrics.append((Format.replace_space(stage + " REG2REG " + "worst hold violation"),
                                         Format.format_metric_values(found_worst_hold_vio.group(2))))
                elif found_crit_path_length:
                    self.metrics.append((Format.replace_space(stage + " REG2REG " + "critical path len"),
                                         Format.format_metric_values(found_crit_path_length.group(2))))
                elif found_tot_neg_slack:
                    self.metrics.append((Format.replace_space(stage + " REG2REG " + "total neg slack"),
                                         Format.format_metric_values(found_tot_neg_slack.group(2))))
                elif found_tot_hold_vio:
                    self.metrics.append((Format.replace_space(stage + " REG2REG " + "total hold viol"),
                                          Format.format_metric_values(found_tot_hold_vio.group(2))))
                elif found_new_section:
                    in_reg2reg_section = False

            found_cell_count = QorReport.match_line("Leaf", "Cell", "Count", line)
            found_compile_time = QorReport.match_line("Overall", "Compile", "Time", line)
            found_max_trans_vi = QorReport.match_line("Max", "trans", "Violations", line)
            found_max_cap_vi = QorReport.match_line("Max", "Cap", "Violations", line)
            found_max_fan_vi = QorReport.match_line("Max", "Fanout", "Violations", line)

            if found_cell_count:
                self.metrics.append((Format.replace_space(stage + " Cell Count"),
                                     Format.format_metric_valuesfound_cell_count.group(2)))
            elif found_compile_time:
                self.metrics.append((Format.replace_space(stage + " cpu runtime")+" (secs)",
                                     Format.format_metric_valuesfound_compile_time.group(2)))
            elif found_max_trans_vi:
                self.metrics.append((Format.replace_space(stage + " max trans viols"),
                                     Format.format_metric_values(found_max_trans_vi.group(2))))
            elif found_max_cap_vi:
                self.metrics.append((Format.replace_space(stage + " max cap viols"),
                                     Format.format_metric_values(found_max_cap_vi.group(2))))
            elif found_max_fan_vi:
                self.metrics.append((Format.replace_space(stage + " max fanout viols"),
                                     Format.format_metric_values(found_max_fan_vi.group(2))))
