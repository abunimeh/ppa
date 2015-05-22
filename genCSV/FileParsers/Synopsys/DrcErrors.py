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
    def replace_space(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    @staticmethod
    def does_fin_rpt_exist(file):
        import os
        directory = os.path.dirname(file)
        files_in_directory = os.listdir(directory)
        if "Final_Report.txt" in files_in_directory:
            print("Using Final_Report.txt to get errors in %s\n" % directory)
            return 1
    @staticmethod
    def tool_version_found(metricNames):
        for metric in metricNames:
            met = tuple(metric)
            for name in range(len(met)):
                if "drc_tool_version" in met[name][0]:
                    return True
        return False
    @staticmethod
    def search_file(file, metricNames):
        import re
        stage = DRCError.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        errorData = DRCErrorData()
        violationCount = 0
        data_items = []
        fin_rpt = DRCError.does_fin_rpt_exist(file)
        tool_found = DRCError.tool_version_found(metricNames)
        for line in lines:
            found_tool_version = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
            if found_tool_version:
                if tool_found is False:
                    errorData.found_tool_version = DRCError.replace_space("drc tool version"), found_tool_version.group(2)
                    data_items.append(errorData.found_tool_version)
            if fin_rpt != 1:
                found_violation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)
                if found_violation:
                    violationCount += int(found_violation.group(1))

        if fin_rpt == 1:
            return data_items
        if violationCount > 0:
            errorData.found_violation = DRCError.replace_space(stage), violationCount
            data_items.append(errorData.found_violation)
        else:
            errorData.found_violation = DRCError.replace_space(stage), "PASS"
            data_items.append(errorData.found_violation)

        return data_items