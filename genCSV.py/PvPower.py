class PvPowerData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class PvPower:
    def mathcLine(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+[\s]*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    def searchfile():
        DataItems = []
        # Open the file with read only permit
        f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\pv_runs\power\cpu.power.power.rpt', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        pvData = PvPowerData()
        for line in lines:
            foundCInternPwr = PvPower.mathcLine("Cell","Internal","Power",line)
            foundCLeakPwr = PvPower.mathcLine("Cell","Leakage","Power",line)
            foundNetSwPwr = PvPower.mathcLine("Net","switching","Power",line)
            foundTotalPwr = PvPower.mathcLine("Total","Power", " ", line)

            if foundCInternPwr:
                pvData.foundCInternPwr = PvPower.replaceSpace(foundCInternPwr.group(1)), foundCInternPwr.group(2)
                DataItems.append(pvData.foundCInternPwr)
            if foundCLeakPwr:
                pvData.foundCLeakPwr = PvPower.replaceSpace(foundCLeakPwr.group(1)), foundCLeakPwr.group(2)
                DataItems.append(pvData.foundCLeakPwr)
            if foundNetSwPwr:
                pvData.foundNetSwPwr = PvPower.replaceSpace(foundNetSwPwr.group(1)), foundNetSwPwr.group(2)
                DataItems.append(pvData.foundNetSwPwr)
            if foundTotalPwr:
                pvData.foundTotalPwr = PvPower.replaceSpace(foundTotalPwr.group(1)), foundTotalPwr.group(2)
                DataItems.append(pvData.foundTotalPwr)

        return DataItems