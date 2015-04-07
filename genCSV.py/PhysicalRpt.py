class PhysicalRptData:
    @staticmethod
    def outdata(metric_list):
        for metrics in metric_list:
            print(metrics)

class PhysicalRpt:
    @staticmethod
    def mathcLine(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    @staticmethod
    def replaceSpace(metric_name):
        import re
        newName = re.sub(r'[\W]+', "_", metric_name)
        return newName

    @staticmethod
    def searchfile(file):
        DataItems = []
        from operator import itemgetter
        # Open the file with read only permit
        f = open(file, "r")
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
                rptData.foundUtil = PhysicalRpt.replaceSpace("apr utilization"), foundUtil.group(2)
                DataItems.append(rptData.foundUtil)
            if foundShort:
                rptData.foundShort = PhysicalRpt.replaceSpace("apr Shorts"), foundShort.group(2)
                DataItems.append(rptData.foundShort)
            if foundTotalEr:
                rptData.foundTotalEr = PhysicalRpt.replaceSpace("apr DRC"), foundTotalEr.group(2)
                DataItems.append(rptData.foundTotalEr)
            if foundTotalMem:
                rptData.foundTotalMem = PhysicalRpt.replaceSpace("apr Memory"), foundTotalMem.group(2)
                DataItems.append(rptData.foundTotalMem)

        data_items = sorted(DataItems, key=itemgetter(0))
        return ["%s" % i[0] for i in data_items], ["%s" % i[1] for i in data_items]
