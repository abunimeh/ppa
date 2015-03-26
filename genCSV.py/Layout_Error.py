class LayoutErrorData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class LayoutError:

    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    def searchfile():
        import re
        # Open the file with read only permit
        f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\drc_lvs\denall\cpu.LAYOUT_ERRORS', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        erData = LayoutErrorData()
        violationCount = 0
        DataItems = []

        for line in lines:
            foundToolVersion = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
            foundViolation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)

            if foundToolVersion:
                erData.foundToolVersion = LayoutError.replaceSpace(foundToolVersion.group(1)), foundToolVersion.group(2)
                DataItems.append(erData.foundToolVersion)
            if foundViolation:
                tempfound = foundViolation.group(2)
                violationCount += int(foundViolation.group(1))
        if violationCount > 0:
            erData.foundViolation = (tempfound, violationCount)
            DataItems.append(erData.foundViolation)
        return DataItems
