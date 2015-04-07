class PvPowerData:
    @staticmethod
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class PvPower:
    @staticmethod
    def mathcLine(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+[\s]*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    @staticmethod
    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    @staticmethod
    def searchfile(file):
        DataItems = []
        # Open the file with read only permit
        from operator import itemgetter

        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        pvData = PvPowerData()
        for line in lines:
            foundCInternPwr = PvPower.mathcLine("Cell", "Internal", "Power", line)
            foundCLeakPwr = PvPower.mathcLine("Cell", "Leakage", "Power", line)
            foundNetSwPwr = PvPower.mathcLine("Net", "switching", "Power", line)
            foundTotalPwr = PvPower.mathcLine("Total", "Power", " ", line)
            pv = "pv power tttt"
            if foundCInternPwr:
                pvData.foundCInternPwr = PvPower.replaceSpace(pv + " internal"), foundCInternPwr.group(2)
                DataItems.append(pvData.foundCInternPwr)
            if foundCLeakPwr:
                pvData.foundCLeakPwr = PvPower.replaceSpace(pv + " leakage"), foundCLeakPwr.group(2)
                DataItems.append(pvData.foundCLeakPwr)
            if foundNetSwPwr:
                pvData.foundNetSwPwr = PvPower.replaceSpace(pv + " switch"), foundNetSwPwr.group(2)
                DataItems.append(pvData.foundNetSwPwr)
            if foundTotalPwr:
                pvData.foundTotalPwr = PvPower.replaceSpace(pv + " total"), foundTotalPwr.group(2)
                DataItems.append(pvData.foundTotalPwr)

        data_items = sorted(DataItems, key=itemgetter(0))
        return ["%s" % i[0] for i in data_items], ["%s" % i[1] for i in data_items]