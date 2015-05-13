class PvPowerData:
    pass
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
    def search_file(file):
        DataItems = []
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        pvData = PvPowerData()
        pv = "pv power tttt"
        pvData.foundCInternPwr = [PvPower.replaceSpace(pv + " internal"), "N/A"]
        pvData.foundCLeakPwr = [PvPower.replaceSpace(pv + " leakage"), "N/A"]
        pvData.foundNetSwPwr = [PvPower.replaceSpace(pv + " switch"), "N/A"]
        pvData.foundTotalPwr = [PvPower.replaceSpace(pv + " total"), "N/A"]

        for line in lines:
            foundCInternPwr = PvPower.mathcLine("Cell", "Internal", "Power", line)
            foundCLeakPwr = PvPower.mathcLine("Cell", "Leakage", "Power", line)
            foundNetSwPwr = PvPower.mathcLine("Net", "switching", "Power", line)
            foundTotalPwr = PvPower.mathcLine("Total", "Power", " ", line)

            if foundCInternPwr:
                pvData.foundCInternPwr[1] = foundCInternPwr.group(2)
            elif foundCLeakPwr:
                pvData.foundCLeakPwr[1] = foundCLeakPwr.group(2)
            elif foundNetSwPwr:
                pvData.foundNetSwPwr[1] = foundNetSwPwr.group(2)
            elif foundTotalPwr:
                pvData.foundTotalPwr[1] = foundTotalPwr.group(2)

        DataItems.append(tuple(pvData.foundCInternPwr))
        DataItems.append(tuple(pvData.foundCLeakPwr))
        DataItems.append(tuple(pvData.foundNetSwPwr))
        DataItems.append(tuple(pvData.foundTotalPwr))

        return DataItems
