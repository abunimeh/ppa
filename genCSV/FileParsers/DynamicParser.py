__author__ = ''
from FileParsers.Parser import Parser


class DynamicParser(Parser):
    def __init__(self, file, tool):
        super(DynamicParser, self).__init__(file)
        self.tool = tool
        self.file_ending = ""

    @staticmethod
    def match_line(regex1, line):
        import re
        line_variables = regex1
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def metric_naming_1(file):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', file, re.I)
        apr = re.search(r'.*apr.*', file, re.I)
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_power = re.search(r'.*pv.*power.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)

        if apr:
            stage = 'apr_'
        elif pv_max:
            stage = 'pv_max_tttt_'
        elif pv_min:
            stage = 'pv_min_tttt_'
        elif pv_power:
            stage = 'pv_power_tttt_'
        elif pv_noise:
            stage = 'pv_noise_tttt_'
        elif syn:
            stage = 'syn_'
        return stage


    @staticmethod
    def metric_naming_2(file):
        import re
        stage = ""
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_power = re.search(r'.*pv.*power.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)
        if pv_max:
            stage = 'pv_max_tttt_'
        elif pv_min:
            stage = 'pv_min_tttt_'
        elif pv_power:
            stage = 'pv_power_tttt_'
        elif pv_noise:
            stage = 'pv_noise_tttt_'
        return stage

    @staticmethod
    def metric_naming_3(file):
        import re
        import os.path
        stage = ""
        dir_name = os.path.split(os.path.dirname(file))[1]
        denall = re.search(r'.*denall_reuse.*', dir_name, re.I)
        ipall = re.search(r'.*ipall.*', dir_name, re.I)
        drcd = re.search(r'.*drcc.*', dir_name, re.I)
        trclvs = re.search(r'.*lvs.*', dir_name, re.I)
        gden = re.search(r'.*gden.*', dir_name, re.I)
        HV = re.search(r'.*HV.*', dir_name, re.I)
        if denall:
            stage = '_denall_reuse'
        elif ipall:
            stage = '_IPall'
        elif drcd:
            stage = '_drcc'
        elif trclvs:
            stage = '_lvs'
        elif gden:
            stage = '_gden'
        elif HV:
            stage = '_HV'
        return stage

    def determine_metric_name(self, metric_object_name):
        # if metric_object_name["stage"] == "none":
        #     return metric_object_name["metric_name"]
        if metric_object_name["stage"] == 1:
            return self.metric_naming_1(self.file) + metric_object_name["metric_name"]
        elif metric_object_name["stage"] == 2:
            return self.metric_naming_2(self.file) + metric_object_name["metric_name"]
        elif metric_object_name["stage"] == 3:
            return self.metric_naming_3(self.file) + metric_object_name["metric_name"]
        return metric_object_name["metric_name"]

    def get_file_lines(self):
        from time import sleep
        if self.file_ending is not "":
            with open(self.file, "r") as f:
                # The variable "lines" is a list containing all lines
                return f.readlines()
        else:
            print("***Error! The file %s is not in the configuration file \n" % self.file)
            sleep(4)
            return

    def append_metric(self, metric_object_name, line):
        metric_name = self.determine_metric_name(metric_object_name)
        metric_regexp = self.match_line(metric_object_name["metric_reg_exp"], line)

        if metric_regexp:
            if metric_regexp.group(2) == '':
                metric = metric_name, 0.00
            else:
                metric = metric_name, self.format_metric_values(metric_regexp.group(2))
            self.metrics.append(metric)

    def get_metrics_dictionary(self):
        import json
        import FindFile
        config_file = FindFile.return_config_name()

        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # gets the line_keywords from the JSON file
            try:
                metrics_dictionary = json_data['metrics_dictionary'][self.tool]
            except KeyError:
                print("***Error! Something is wrong in the json configuration file \n")
        return metrics_dictionary

    def check_for_file_in_metrics_dictionary(self, metrics_dictionary):
        for key_files in metrics_dictionary:
            if self.file.endswith(key_files):
                # file_ending contains the dictionary of variables for a given file type (e.g. fill.qor.rpt)
                self.file_ending = key_files
                break

    def search_file(self):
        metrics_dictionary = self.get_metrics_dictionary()
        self.check_for_file_in_metrics_dictionary(metrics_dictionary)
        section = 0
        last_line = ""
        if self.file_ending is not "":
            for line in self.get_file_lines():
                for metric_object, metric_object_name in metrics_dictionary[self.file_ending].items():
                    if metric_object_name["found_section_reg_exp"]["begin_line"] == "none":
                        self.append_metric(metric_object_name, line)
                    else:
                        if last_line != line:
                            beginning_line = self.match_line(metric_object_name["found_section_reg_exp"]["begin_line"], line)
                            if beginning_line:
                                if last_line != line:
                                    section = 1
                                continue
                            ending_line = self.match_line(metric_object_name["found_section_reg_exp"]["end_line"], line)
                        if section == 1:
                            self.append_metric(metric_object_name, line)
                            if ending_line:
                                section = 0
                        last_line = line