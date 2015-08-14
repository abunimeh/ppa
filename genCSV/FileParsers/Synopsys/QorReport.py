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

        stage = self.metric_stage_name()
        # in_reg2reg_section is used to search a certain amount after reg2reg
        in_reg2reg_section = False

        # Loop through each line to find the metrics
        for line in self.get_file_lines():
            # Regular expression method 'search' returns the found regular expressions back in groups designated by
            # the parentheses in the regular expression
            found_reg_group = re.search(r'.*(REG2REG).*', line, re.I)
            found_version = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
            if self.add_to_metrics(found_version, self.replace_space(stage + " tool version")):
                pass
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
                found_crit_slack = self.match_line("Critical", "path", "slack", line)
                found_worst_hold_vio = self.match_line("Worst", "hold", "violation", line)
                found_crit_path_length = self.match_line("critical", "path", "length", line)
                found_tot_neg_slack = self.match_line("total", "Negative", "slack", line)
                found_tot_hold_vio = self.match_line("total", "hold", "violation", line)
                found_new_section = re.search(r'.*Timing[\s]*Path[\s]*Group.*', line, re.I)

                if found_crit_slack:
                    if 'pv min' in stage:
                        self.metrics.append((self.replace_space(stage + " REG2REG " + "worst hold viol"),
                                             self.format_metric_values(found_crit_slack.group(2))))
                    else:
                        self.metrics.append((self.replace_space(stage + " REG2REG " + "worst setup viol"),
                                             self.format_metric_values(found_crit_slack.group(2))))
                elif self.add_to_metrics(found_worst_hold_vio, self.replace_space(stage + " REG2REG " + "worst hold violation")):
                    pass
                elif self.add_to_metrics(found_crit_path_length, self.replace_space(stage + " REG2REG " + "critical path len")):
                    pass
                elif self.add_to_metrics(found_tot_neg_slack, self.replace_space(stage + " REG2REG " + "total neg slack")):
                    pass
                elif self.add_to_metrics(found_tot_hold_vio, self.replace_space(stage + " REG2REG " + "total hold viol")):
                    pass
                elif found_new_section:
                    in_reg2reg_section = False

            found_cell_count = self.match_line("Leaf", "Cell", "Count", line)
            found_compile_time = self.match_line("Overall", "Compile", "Time", line)
            found_max_trans_vi = self.match_line("Max", "trans", "Violations", line)
            found_max_cap_vi = self.match_line("Max", "Cap", "Violations", line)
            found_max_fan_vi = self.match_line("Max", "Fanout", "Violations", line)

            if self.add_to_metrics(found_cell_count, self.replace_space(stage + " Cell Count")):
                pass
            elif self.add_to_metrics(found_compile_time, self.replace_space(stage + " cpu runTIME")+" (secs)"):
                pass
            elif self.add_to_metrics(found_max_trans_vi, self.replace_space(stage + " max trans viols")):
                pass
            elif self.add_to_metrics(found_max_cap_vi, self.replace_space(stage + " max cap viols")):
                pass
            elif self.add_to_metrics(found_max_fan_vi, self.replace_space(stage + " max fanout viols")):
                pass

