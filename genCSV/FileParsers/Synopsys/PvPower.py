class PvPowerData:
    pass
class PvPower:
    @staticmethod
    def match_line(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+[\s]*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    @staticmethod
    def replace_space(metric_name):
        import re
        newName = re.sub(r'[\W]+', "_", metric_name)
        return newName

    @staticmethod
    def search_file(file):
        from Metrics.FormatMetric import FormatMetric

        DataItems = []
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        pvData = PvPowerData()
        pv = "pv power tttt"
        pvData.foundCInternPwr = [PvPower.replace_space(pv + " internal"), "N/A"]
        pvData.foundCLeakPwr = [PvPower.replace_space(pv + " leakage"), "N/A"]
        pvData.foundNetSwPwr = [PvPower.replace_space(pv + " switch"), "N/A"]
        pvData.foundTotalPwr = [PvPower.replace_space(pv + " total"), "N/A"]

        for line in lines:
            foundCInternPwr = PvPower.match_line("Cell", "Internal", "Power", line)
            foundCLeakPwr = PvPower.match_line("Cell", "Leakage", "Power", line)
            foundNetSwPwr = PvPower.match_line("Net", "switching", "Power", line)
            foundTotalPwr = PvPower.match_line("Total", "Power", " ", line)

            if foundCInternPwr:
                pvData.foundCInternPwr[1] = FormatMetric.format_metric_values(foundCInternPwr.group(2))
            elif foundCLeakPwr:
                pvData.foundCLeakPwr[1] = FormatMetric.format_metric_values(foundCLeakPwr.group(2))
            elif foundNetSwPwr:
                pvData.foundNetSwPwr[1] = FormatMetric.format_metric_values(foundNetSwPwr.group(2))
            elif foundTotalPwr:
                pvData.foundTotalPwr[1] = FormatMetric.format_metric_values(foundTotalPwr.group(2))

        DataItems.append(tuple(pvData.foundCInternPwr))
        DataItems.append(tuple(pvData.foundCLeakPwr))
        DataItems.append(tuple(pvData.foundNetSwPwr))
        DataItems.append(tuple(pvData.foundTotalPwr))

        return DataItems
