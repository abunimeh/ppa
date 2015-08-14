from FileParsers.Parser import Parser


class CalibreErrors(Parser):
    def __init__(self, file):
        super(CalibreErrors, self).__init__(file)

    def metric_naming(self):
        import re
        import os.path

        executing_file_location = os.path.realpath(__file__)
        dir_name = os.path.split(os.path.dirname(self.file))[1]
        stage_found = re.search(r'(denall_reuse|ipall|drcc|lvs|gden|HV)', dir_name, re.I)

        if stage_found:
            stage_name = " " + stage_found.group(1)
            if stage_name == ' ipall':
                stage_name = " Ipall"
            return stage_name
        else:
            print("Error!! Stage not found!! The method 'metric_naming' in the file %s needs to be edited \n" % executing_file_location)

    def search_file(self):
        import re

        stage = self.metric_naming()
        violation_metric_name = self.replace_space('calibre' + stage)
        fail_violation_metric_name = self.replace_space('calibre' + stage)

        if self.file.endswith("drc.sum"):
            for line in self.get_file_lines():
                found_violation = re.search('(TOTAL[\s]*DRC[\s]*Results[\s]*Generated:)[\s]*([-\d\.]*).*', line, re.I)
                if found_violation:
                    self.metrics.append((violation_metric_name, self.format_metric_values(found_violation.group(2))))
                    break

        elif self.file.endswith("lvs.report"):
            for line in self.get_file_lines():
                found_fail_violation = re.search('.*#*[\s]*(INCORRECT)[\s]*.*', line, re.I)
                if found_fail_violation:
                    self.metrics.append((fail_violation_metric_name, "FAIL"))
                    break
