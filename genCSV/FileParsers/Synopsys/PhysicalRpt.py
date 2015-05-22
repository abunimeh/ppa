# This class is future a soon slight refactor of the metrics gathering process
class PhysicalRptData:
    pass


class PhysicalRpt:
    # This method is what is used to do the regular expression on the lines of the file. The method simply takes in
    # the three first arguments as the names for the regular expression and the fourth argument as the line the
    # regular expression will search.
    @staticmethod
    def match_line(regex1, regex2, regex3, file_line):
        import re
        words_to_match = r'(%s[\s]*%s[\s]*%s[\s]*.*):+[\s]*([\d\.]+).*' % (regex1, regex2, regex3)
        regular_expression = re.search(words_to_match, file_line, re.I)
        return regular_expression

    # This method is used to basically replace the spaces in the given metric name with underscores
    @staticmethod
    def replace_space(metric_name):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_name)
        return new_name

    # This method is used to search the given file and retrieve the required metrics out of those files
    @staticmethod
    def search_file(file):
        from Metrics.FormatMetric import FormatMetric

        metric_list = []
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "file_lines" is a list containing all file_lines
        file_lines = f.readlines()
        f.close()
        rpt_data = PhysicalRptData()
        rpt_data.found_util = [PhysicalRpt.replace_space("apr utilization")+" (%)", "\t"]
        rpt_data.found_total_error = [PhysicalRpt.replace_space("apr DRC"), "\t"]
        rpt_data.found_total_mem = [PhysicalRpt.replace_space("apr Memory")+" (MB)", "\t"]

        # Loop through each file_line to find the metrics
        for file_line in file_lines:
            found_util = PhysicalRpt.match_line("Std", "cells", "utilization", file_line)
            found_short = PhysicalRpt.match_line("Short", " ", " ", file_line)
            found_total_error = PhysicalRpt.match_line("Total", "error", "number", file_line)
            found_total_mem = PhysicalRpt.match_line("Total", "Proc", "Memory", file_line)

            # Regular expression method 'search' returns the found regular expressions back in groups designated by
            # the parentheses in the regular expression
            if found_util:
                rpt_data.found_util[1] = FormatMetric.format_metric_values(found_util.group(2))
            elif found_short:
                rpt_data.found_short = PhysicalRpt.replace_space("apr Shorts"), FormatMetric.format_metric_values(found_short.group(2))
                metric_list.append(rpt_data.found_short)
            elif found_total_error:
                rpt_data.found_total_error[1] = FormatMetric.format_metric_values(found_total_error.group(2))
            elif found_total_mem:
                rpt_data.found_total_mem[1] = FormatMetric.format_metric_values(found_total_mem.group(2))

        # Append the metrics that we found to the metric_list
        metric_list.append(tuple(rpt_data.found_util))
        metric_list.append(tuple(rpt_data.found_total_error))
        metric_list.append(tuple(rpt_data.found_total_mem))

        return metric_list
