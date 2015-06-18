class DRCErrorData:
    pass

class DRCError:
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        denall = re.search(r'.*denall_reuse.*', file, re.I)
        ipall = re.search(r'.*drc_IPall.*', file, re.I)
        drcd = re.search(r'.*drcd.*', file, re.I)
        trclvs = re.search(r'.*trclvs.*', file, re.I)
        if denall:
            stage = 'drc denall'
        if ipall:
            stage = 'drc IPall'
        if drcd:
            stage = 'drc drcd'
        if trclvs:
            stage = 'drc trclvs'
        return stage

    @staticmethod
    def replace_space(metric_name):
        import re
        newName = re.sub(r'[\W]+', "_", metric_name)
        return newName

    @staticmethod
    def does_fin_rpt_exist(file):
        import os
        directory = os.path.dirname(file)
        files_in_directory = os.listdir(directory)
        if "Final_Report.txt" in files_in_directory:
            print("Using Final_Report.txt to get errors in %s" % directory)
            return 1
    @staticmethod
    def tool_version_found(metric_collections):
        for metric_pair in metric_collections:
            # met = tuple(metric)
            # for name in range(len(met)):
                if "drc_tool_version" in metric_pair[0]:
                    return True
        return False
    @staticmethod
    def search_file(file, metric_collections):
        import re
        import Metrics.FormatMetric as Format

        stage = Format.replace_space(DRCError.metric_naming(file))
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        errorData = DRCErrorData()
        violationCount = 0
        metric_items = []
        fin_rpt = DRCError.does_fin_rpt_exist(file)
        tool_found = DRCError.tool_version_found(metric_collections)
        for line in lines:
            found_tool_version = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
            if found_tool_version:
                if tool_found is False:
                    errorData.found_tool_version = DRCError.replace_space("drc tool version"), found_tool_version.group(2)
                    metric_items.append(errorData.found_tool_version)
            if fin_rpt != 1:
                found_violation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)
                if found_violation:
                    violationCount += int(found_violation.group(1))

        if fin_rpt == 1:
            return metric_items
        if violationCount > 0:
            errorData.found_violation = stage + " (NB)", Format.format_metric_values(violationCount)
            metric_items.append(errorData.found_violation)
        else:
            errorData.found_violation = stage + " (NB)", "PASS"
            metric_items.append(errorData.found_violation)

        return metric_items