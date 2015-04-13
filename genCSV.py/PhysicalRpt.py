class PhysicalRptData:
    pass
class PhysicalRpt:
    @staticmethod
    def mathcLine(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*([\d]+[\.]*[\d]*.*%s*)' %(regex1, regex2, regex3, '%')
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
            elif foundShort:
                rptData.foundShort = PhysicalRpt.replaceSpace("apr Shorts"), foundShort.group(2)
                DataItems.append(rptData.foundShort)
            elif foundTotalEr:
                rptData.foundTotalEr = PhysicalRpt.replaceSpace("apr DRC"), foundTotalEr.group(2)
                DataItems.append(rptData.foundTotalEr)
            elif foundTotalMem:
                rptData.foundTotalMem = PhysicalRpt.replaceSpace("apr Memory"), foundTotalMem.group(2)
                DataItems.append(rptData.foundTotalMem)

        return DataItems
