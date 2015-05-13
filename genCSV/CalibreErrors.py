__author__ = ''


class CalibreErrorsData:
    pass


class CalibreErrors:
    @staticmethod
    def metric_naming(file):
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
            stage = ' denall reuse'
        elif ipall:
            stage = ' IPall'
        elif drcd:
            stage = ' drcc'
        elif trclvs:
            stage = ' lvs'
        elif gden:
            stage = ' gden'
        elif HV:
            stage = ' HV'
        return stage

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    @staticmethod
    def search_file(file):
        import re
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        # close the file after reading the lines.
        f.close()
        data_items = []
        stage = CalibreErrors.metric_naming(file)
        calibre_errors = CalibreErrorsData()
        calibre_errors.found_violation = [CalibreErrors.replace_space('calibre' + stage), "N/A"]
        calibre_errors.found_fail_violations = [CalibreErrors.replace_space('calibre' + stage), "N/A"]

        if file.endswith("drc.sum"):
            for line in lines:
                found_violation = re.search('(TOTAL[\s]*DRC[\s]*Results[\s]*Generated:)[\s]*([-\d\.]*).*', line, re.I)
                if found_violation:
                    calibre_errors.found_violation[1] = found_violation.group(2)
                    data_items.append(tuple(calibre_errors.found_violation))
                    return data_items

        elif file.endswith("lvs.report"):
            for line in lines:
                found_fail_violation = re.search('.*#*[\s]*(INCORRECT)[\s]*.*', line, re.I)
                if found_fail_violation:
                    calibre_errors.found_fail_violations[1] = "FAIL"
                    data_items.append(tuple(calibre_errors.found_fail_violations))
                    return data_items

        data_items.append(tuple(calibre_errors.found_violation))
        data_items.append(tuple(calibre_errors.found_fail_violations))

        return data_items