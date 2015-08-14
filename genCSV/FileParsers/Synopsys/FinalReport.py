from FileParsers.Parser import Parser


class FinalReport(Parser):
    def __init__(self, file):
        super(FinalReport, self).__init__(file)

    def metric_naming(self):
        import re
        import os.path
        executing_file_location = os.path.realpath(__file__)
        found_stage = re.search(r'(denall|ipall|drcd|trclvs)', self.file, re.I)

        if found_stage:
            stage_name = found_stage.group(1)
            if stage_name == "ipall":
                stage_name = "Ipall"
            return stage_name
        else:
            print("Error!! Stage not found!! The method 'metric_naming' in the file %s needs to be edited \n" % executing_file_location)

    def search_file(self):
        import re
        stage = self.metric_naming()
        violation_name = self.replace_space("drc " + stage) + " (NB)"

        for line in self.get_file_lines():
            found_violation = re.search(r'(The[\s]*number[\s]*of[\s]*actual[\s]*errors)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if self.add_to_metrics(found_violation, violation_name):
                break
