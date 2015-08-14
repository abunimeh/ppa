from FileParsers.Parser import Parser


class PhysicalReport(Parser):
    def __init__(self, file):
        super(PhysicalReport, self).__init__(file)

    # This method is what is used to do the regular expression on the lines of the file. The method simply takes in
    # the three first arguments as the names for the regular expression and the fourth argument as the line the
    # regular expression will search.
    @staticmethod
    def match_line(regex1, regex2, regex3, file_line):
        import re
        words_to_match = r'(%s[\s]*%s[\s]*%s[\s]*.*):+[\s]*([\d\.]+).*' % (regex1, regex2, regex3)
        regular_expression = re.search(words_to_match, file_line, re.I)
        return regular_expression

    # This method is used to search the given file and retrieve the required metrics out of those files
    def search_file(self):
        apr_utilization_name = self.replace_space("apr utilization")+" (%)"
        apr_short_name = self.replace_space("apr Shorts")
        apr_error_name = self.replace_space("apr DRC")
        apr_memory_name = self.replace_space("apr Memory")+" (MB)"

        # Loop through each file line to find the metrics
        for line in self.get_file_lines():
            found_apr_utilization = self.match_line("Std", "cells", "utilization", line)
            found_apr_short = self.match_line("Short", " ", " ", line)
            found_total_error = self.match_line("Total", "error", "number", line)
            found_total_mem = self.match_line("Total", "Proc", "Memory", line)

            # Regular expression method 'search' returns the found regular expressions back in groups designated by
            # the parentheses in the regular expression
            if self.add_to_metrics(found_apr_utilization, apr_utilization_name):
                pass
            elif self.add_to_metrics(found_apr_short, apr_short_name):
                pass
            elif self.add_to_metrics(found_total_error, apr_error_name):
                pass
            elif found_total_mem:
                if not self.check_list(apr_memory_name):
                    self.metrics.append((apr_memory_name, self.format_metric_values(found_total_mem.group(2))))