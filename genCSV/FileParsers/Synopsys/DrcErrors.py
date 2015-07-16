class DRCErrorData:
    pass

from FileParsers.Parser import Parser


class DRCError(Parser):
    def __init__(self, file, metric_collections):
        super(DRCError, self).__init__(file)
        self.metric_collections = metric_collections

    def metric_naming(self):
        import re
        stage = ""
        denall = re.search(r'.*denall_reuse.*', self.file, re.I)
        ipall = re.search(r'.*drc_IPall.*', self.file, re.I)
        drcd = re.search(r'.*drcd.*', self.file, re.I)
        trclvs = re.search(r'.*trclvs.*', self.file, re.I)
        if denall:
            stage = 'drc denall'
        if ipall:
            stage = 'drc IPall'
        if drcd:
            stage = 'drc drcd'
        if trclvs:
            stage = 'drc trclvs'
        return stage

    def check_for_final_report(self):
        import os

        final_report_exist = False
        directory = os.path.dirname(self.file)
        files_in_directory = os.listdir(directory)

        if "Final_Report.txt" in files_in_directory:
            print("Using Final_Report.txt to get errors in %s" % directory)
            final_report_exist = True

        return final_report_exist

    def tool_version_found(self):
        for metric_pair in self.metric_collections:
            if "drc_tool_version" == metric_pair[0]:
                return True
        return False

    def search_file(self):
        import re
        import Metrics.FormatMetric as Format

        stage = Format.replace_space(self.metric_naming())
        lines = self.get_file_lines()
        errorData = DRCErrorData()
        violation_count = 0
        # final_report_exist = DRCError.check_for_final_report()
        # tool_found = DRCError.tool_version_found(self.metric_collections)
        final_report_exist = self.check_for_final_report()
        tool_version_name = Format.replace_space("drc tool version")
        violation_name = stage + " (NB)"

        for line in lines:
            found_tool_version = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
            if found_tool_version:
                if not self.tool_version_found():
                    # errorData.found_tool_version = Format.replace_space("drc tool version"), found_tool_version.group(2)
                    self.metrics.append((tool_version_name, found_tool_version.group(2)))
            elif not final_report_exist:
                found_violation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)
                if found_violation:
                    violation_count += int(found_violation.group(1))
        print("COUNT", violation_count)
        if final_report_exist:
            return self.metrics
        if violation_count > 0:
            # errorData.found_violation = stage + " (NB)", Format.format_metric_values(violation_count)
            self.metrics.append((violation_name, violation_count))
        else:
            # errorData.found_violation = stage + " (NB)", "PASS"
            self.metrics.append((violation_name, "PASS"))