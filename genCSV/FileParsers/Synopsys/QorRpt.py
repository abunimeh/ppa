# This class is future a soon slight refactor of the metrics gathering process
class QorRptData:
    pass


class QorRpt:
    # @staticmethod is put before methods when the self variable won't be used in the method
    # This method is used to find and return the stage(e.g. "syn" or "py") by using the file name that was passed into
    # the method search_file. The method then uses regular expressions to find and return the stage name.
    @staticmethod
    def metric_stage_name(file):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', file, re.I)
        apr = re.search(r'.*apr.*', file, re.I)
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)
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

    # This method is what is used to do the regular expression on the lines of the file. The method simply takes in
    # the three first arguments as the names for the regular expression and the fourth argument as the line the
    # regular expression will search.
    @staticmethod
    def match_line(regex1, regex2, regex3, file_line):
        import re
        line_variables = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*([-\d\.]*)+.*' % (regex1, regex2, regex3)
        result = re.search(line_variables, file_line, re.I)
        return result

    # This method is used to basically replace the spaces in the given metric name with underscores
    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    # This method is used to search the given file and retrieve the required metrics out of those files
    @staticmethod
    def search_file(file):
        import re
        from OrganizingAndFormatingMetrics.FormatMetrics import FormatMetrics
        stage = QorRpt.metric_stage_name(file)

        # Open the file with read only permit
        f = open(file, "r")
        # The variable "file_lines" is a list containing all file_lines
        file_lines = f.readlines()
        # Close the file after reading the file_lines.
        f.close()
        # in_section is used to search a certain amount after reg2reg
        in_section = False
        metric_list = []
        rpt_data = QorRptData()
        rpt_data.found_version = [QorRpt.replace_space(stage + " tool version"), "\t"]
        rpt_data.found_crit_slack = [QorRpt.replace_space(stage + " REG2REG " + "worst setup viol"), "\t"]
        if 'pv min' in stage:
            rpt_data.found_crit_slack[0] = QorRpt.replace_space(stage + " REG2REG " + "worst hold viol")
        rpt_data.found_worst_hold_vio = [QorRpt.replace_space(stage + " REG2REG " + "worst hold violation"), "\t"]
        rpt_data.found_crit_path_length = [QorRpt.replace_space(stage + " REG2REG " + "critical path len"), "\t"]
        rpt_data.found_tot_neg_slack = [QorRpt.replace_space(stage + " REG2REG " + "total neg slack"), "\t"]
        rpt_data.found_tot_hold_vio = [QorRpt.replace_space(stage + " REG2REG " + "total hold viol"), "\t"]
        rpt_data.found_cell_count = [QorRpt.replace_space(stage + " Cell Count"), "\t"]
        rpt_data.foundCompileTime = [QorRpt.replace_space(stage + " cpu runtime"), "\t"]
        rpt_data.foundMaxTransVi = [QorRpt.replace_space(stage + " max trans viols"), "\t"]
        rpt_data.foundMaxCapVi = [QorRpt.replace_space(stage + " max cap viols"), "\t"]
        rpt_data.foundMaxFanVi = [QorRpt.replace_space(stage + " max fanout viols"), "\t"]

        # Loop through each file_line to find the metrics
        for file_line in file_lines:
            found_reg_group = re.search(r'.*(REG2REG).*', file_line, re.I)
            found_version = re.search(r'(Version):[\s]*([\S]*)', file_line, re.I)
            if found_version:
                # Regular expression method 'search' returns the found regular expressions back in groups designated by
                # the parentheses in the regular expression
                rpt_data.found_version[1] = found_version.group(2)
            # If we found the line that contains the word REG2REG then we set 'in_section' to True
            elif found_reg_group:
                if 'pv max tttt' in stage:
                    if 'max_delay/setup' in file_line:
                        in_section = True
                elif 'pv min tttt' in stage:
                    if 'min_delay/hold' in file_line:
                        in_section = True
                else:
                    in_section = True
            # If 'in_section' is true and the stage is not 'pv noise tttt' then search for the certain metrics that are
            # found in that section
            elif in_section and stage != 'pv noise tttt':
                found_crit_slack = QorRpt.match_line("Critical", "path", "slack", file_line)
                found_worst_hold_vio = QorRpt.match_line("Worst", "hold", "violation", file_line)
                found_crit_path_length = QorRpt.match_line("critical", "path", "length", file_line)
                found_tot_neg_slack = QorRpt.match_line("total", "Negative", "slack", file_line)
                found_tot_hold_vio = QorRpt.match_line("total", "hold", "violation", file_line)
                found_new_section = re.search(r'.*Timing[\s]*Path[\s]*Group.*', file_line, re.I)

                if found_crit_slack:
                    rpt_data.found_crit_slack[1] = FormatMetrics.format_metric_values(found_crit_slack.group(2))
                elif found_worst_hold_vio:
                    rpt_data.found_worst_hold_vio[1] = FormatMetrics.format_metric_values(found_worst_hold_vio.group(2))
                elif found_crit_path_length:
                    rpt_data.found_crit_path_length[1] = FormatMetrics.format_metric_values(found_crit_path_length.group(2))
                elif found_tot_neg_slack:
                    rpt_data.found_tot_neg_slack[1] = FormatMetrics.format_metric_values(found_tot_neg_slack.group(2))
                elif found_tot_hold_vio:
                    rpt_data.found_tot_hold_vio[1] = FormatMetrics.format_metric_values(found_tot_hold_vio.group(2))
                elif found_new_section:
                    in_section = False

            found_cell_count = QorRpt.match_line("Leaf", "Cell", "Count", file_line)
            found_compile_time = QorRpt.match_line("Overall", "Compile", "Time", file_line)
            found_max_trans_vi = QorRpt.match_line("Max", "trans", "Violations", file_line)
            found_max_cap_vi = QorRpt.match_line("Max", "Cap", "Violations", file_line)
            found_max_fan_vi = QorRpt.match_line("Max", "Fanout", "Violations", file_line)

            if found_cell_count:
                rpt_data.found_cell_count[1] = found_cell_count.group(2)
            elif found_compile_time:
                rpt_data.foundCompileTime[1] = found_compile_time.group(2)
            elif found_max_trans_vi:
                rpt_data.foundMaxTransVi[1] = FormatMetrics.format_metric_values(found_max_trans_vi.group(2))
            elif found_max_cap_vi:
                rpt_data.foundMaxCapVi[1] = FormatMetrics.format_metric_values(found_max_cap_vi.group(2))
            elif found_max_fan_vi:
                rpt_data.foundMaxFanVi[1] = FormatMetrics.format_metric_values(found_max_fan_vi.group(2))

        # Append the metrics that we found to the metric_list
        metric_list.append(tuple(rpt_data.found_version))
        metric_list.append(tuple(rpt_data.found_crit_slack))
        metric_list.append(tuple(rpt_data.found_worst_hold_vio))
        metric_list.append(tuple(rpt_data.found_crit_path_length))
        metric_list.append(tuple(rpt_data.found_tot_neg_slack))
        metric_list.append(tuple(rpt_data.found_tot_hold_vio))
        metric_list.append(tuple(rpt_data.found_cell_count))
        metric_list.append(tuple(rpt_data.foundCompileTime))
        metric_list.append(tuple(rpt_data.foundMaxTransVi))
        metric_list.append(tuple(rpt_data.foundMaxCapVi))
        metric_list.append(tuple(rpt_data.foundMaxFanVi))

        return metric_list
