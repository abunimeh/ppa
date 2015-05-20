__author__ = ''


class OtherMetricClass:
    @staticmethod
    def mathcLine(regex1, line):
        import re
        keyword = regex1.replace(" ", "")
        line_variables = regex1
        # print("line_var:", line_variables)
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replaceSpace(metricname):
        import re
        new_name = re.sub(r'[\W]+', "_", metricname)
        return new_name

    @staticmethod
    def metric_naming_1(file):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', file, re.I)
        apr = re.search(r'.*apr.*', file, re.I)
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)
        if apr:
            stage = 'apr_'
        elif pv_max:
            stage = 'pv_max_tttt_'
        elif pv_min:
            stage = 'pv_min_tttt_'
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

    @staticmethod
    def search_file(file, tool):
        ending = ""
        import json
        from GenerateMetrics import GenerateMetrics
        config_file = GenerateMetrics.return_config_name()
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # gets the line_keywords from the JSON file
            list_of_files = json_data['line_keywords'][tool]

        for metric_objects in list_of_files:
            if file.endswith(metric_objects):
                # ending contains the dictionary of variables for a given file type (e.g. fill.qor.rpt)
                ending = metric_objects
                break
        if ending is not "":
            f = open(file, "r")
            # The variable "lines" is a list containing all lines
            lines = f.readlines()
            # close the file after reading the lines.
            f.close()
        data_items = []
        section = 0
        last_line = ""
        if ending is not "":
            for line in lines:
                for metric_object, metric_object_name in list_of_files[ending].items():
                    if metric_object_name["found_section_reg_exp"]["begin_line"] == "none":
                        if metric_object_name["stage"] == "none":
                            met_name = metric_object_name["metric_name"]
                        elif metric_object_name["stage"] == 1:
                            met_name = OtherMetricClass.metric_naming_1(file) + metric_object_name["metric_name"]
                        elif metric_object_name["stage"] == 2:
                            met_name = OtherMetricClass.metric_naming_2(file) + metric_object_name["metric_name"]
                        elif metric_object_name["stage"] == 3:
                            met_name = OtherMetricClass.metric_naming_3(file) + metric_object_name["metric_name"]
                        met_value = OtherMetricClass.mathcLine(metric_object_name["metric_reg_exp"], line)
                        if met_value:
                            if met_value.group(2) == '':
                                metric = met_name, 0
                            else:
                                if "add_to_value" in metric_object_name:
                                    metric = met_name, met_value.group(2)+metric_object_name["add_to_value"]
                                else:
                                    metric = met_name, met_value.group(2)
                            data_items.append(metric)
                    else:
                        if last_line != line:
                            beginning_line = OtherMetricClass.mathcLine(metric_object_name["found_section_reg_exp"]["begin_line"], line)
                            if beginning_line:
                                if last_line != line:
                                    section = 1
                                continue
                            ending_line = OtherMetricClass.mathcLine(metric_object_name["found_section_reg_exp"]["end_line"], line)
                        if section == 1:
                            if metric_object_name["stage"] == "none":
                                met_name = metric_object_name["metric_name"]
                            elif metric_object_name["stage"] == 1:
                                met_name = OtherMetricClass.metric_naming_1(file) + metric_object_name["metric_name"]
                            elif metric_object_name["stage"] == 2:
                                met_name = OtherMetricClass.metric_naming_2(file) + metric_object_name["metric_name"]
                            elif metric_object_name["stage"] == 3:
                                met_name = OtherMetricClass.metric_naming_3(file) + metric_object_name["metric_name"]
                            met_value = OtherMetricClass.mathcLine(metric_object_name["metric_reg_exp"], line)
                            if met_value:
                                if met_value.group(2) == '':
                                    metric = met_name, 0
                                else:
                                    metric = met_name, met_value.group(2)
                                data_items.append(metric)
                            if ending_line:
                                section = 0
                        last_line = line

        return data_items

