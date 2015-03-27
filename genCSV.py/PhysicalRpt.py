class PhysicalRptData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class PhysicalRpt:
    def mathcLine(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    def replaceSpace(metric_name):
        import re
        newName = re.sub(r'[\W]+', "_", metric_name)
        return newName

    def searchfile():
        DataItems = []
        from Configurations import Configurations
        base_path = Configurations().parser_final()
        # Open the file with read only permit
        f = open(base_path + 'cpu_testcase\apr\cpu.fill.physical.rpt', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        rptData = PhysicalRptData()

        for line in lines:
            foundUtil = PhysicalRpt.mathcLine("Std", "cells", "utilization", line)
            foundShort = PhysicalRpt.mathcLine("Short", " ", " ", line)
            foundTotalEr = PhysicalRpt.mathcLine("Total", "error", "number", line)
            foundTotalMem = PhysicalRpt.mathcLine("Total", "Proc", "Memory", line)

            if foundUtil:
                rptData.foundUtil = (PhysicalRpt.replaceSpace(foundUtil.group(1))), foundUtil.group(2)
                DataItems.append(rptData.foundUtil)
            if foundShort:
                rptData.foundShort = (PhysicalRpt.replaceSpace(foundShort.group(1))), foundShort.group(2)
                DataItems.append(rptData.foundShort)
            if foundTotalEr:
                rptData.foundTotalEr = (PhysicalRpt.replaceSpace(foundTotalEr.group(1)), foundTotalEr.group(2))
                DataItems.append(rptData.foundTotalEr)
            if foundTotalMem:
                rptData.foundTotalMem = (PhysicalRpt.replaceSpace(foundTotalMem.group(1)), foundTotalMem.group(2))
                DataItems.append(rptData.foundTotalMem)

        return ["%s" % i[0] for i in DataItems], ["%s" % i[1] for i in DataItems]
        #return DataItems
