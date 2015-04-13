
class QorRptData:
    foundCellCount = ()
class QorRpt:
    foundCellCount = ()
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', file, re.I)
        apr = re.search(r'.*apr.*', file, re.I)
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)
        if syn:
            stage = 'syn'
        if apr:
            stage = 'apr'
        if pv_max:
            stage = 'pv max tttt'
        if pv_min:
            stage = 'pv min tttt'
        if pv_noise:
            stage = 'pv noise tttt'
        return stage

    @staticmethod
    def mathcLine(regex1, regex2, regex3, line):
        import re
        line_variables = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*(-*[\d]+[\.]*[\d]*)+.*' % (regex1, regex2, regex3)
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replaceSpace(metricname):
        import re
        new_name = re.sub(r'[\W]+', "_", metricname)
        return new_name

    @staticmethod
    def searchfile(file):
        import re
        stage = QorRpt.metric_naming(file)

        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()

        # look_count is used to search a certain amount after reg2reg
        look_count = 0
        reportDataItems = []
        # close the file after reading the lines.
        f.close()
        rptData = QorRptData()

        for line in lines:
            rptData.foundRegGroup = re.search(r'.*(REG2REG).*', line, re.I)
            foundVersion = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
            if foundVersion:
                rptData.foundVersion = QorRpt.replaceSpace(stage + " tool version"), foundVersion.group(2)
                reportDataItems.append(rptData.foundVersion)
            elif rptData.foundRegGroup:
                look_count = 10
            if look_count != 0:
                foundCritSlack = QorRpt.mathcLine("Critical", "path", "slack", line)
                foundWorstHoldVio = QorRpt.mathcLine("Worst", "hold", "violation", line)
                foundCritPathLength = QorRpt.mathcLine("critical", "path", "length", line)
                foundTotNegSlack = QorRpt.mathcLine("total", "Negative", "slack", line)
                foundTotHoldVio = QorRpt.mathcLine("total", "hold", "violation", line)

                if foundCritSlack:
                    rptData.foundCritSlack = QorRpt.replaceSpace(stage + " REG2REG " + "worst setup viol"), foundCritSlack.group(2)
                    reportDataItems.append(rptData.foundCritSlack)
                elif foundWorstHoldVio:
                    rptData.foundWorstHoldVio = QorRpt.replaceSpace(stage + " REG2REG " + "worst hold viol"), foundWorstHoldVio.group(2)
                    reportDataItems.append(rptData.foundWorstHoldVio)
                elif foundCritPathLength:
                    rptData.foundCritPathLength = QorRpt.replaceSpace(stage + " REG2REG " + "critical path len"), foundCritPathLength.group(2)
                    reportDataItems.append(rptData.foundCritPathLength)
                elif foundTotNegSlack:
                    rptData.foundTotNegSlack = QorRpt.replaceSpace(stage + " REG2REG " + "total neg slack"), foundTotNegSlack.group(2)
                    reportDataItems.append(rptData.foundTotNegSlack)
                elif foundTotHoldVio:
                    rptData.foundTotHoldVio = QorRpt.replaceSpace(stage + " REG2REG " + "total hold viol"), foundTotHoldVio.group(2)
                    reportDataItems.append(rptData.foundTotHoldVio)
                look_count -= 1

            foundCellCount = QorRpt.mathcLine("Leaf", "Cell", "Count", line)
            foundCompileTime = QorRpt.mathcLine("Overall", "Compile", "Time", line)
            foundMaxTransVi = QorRpt.mathcLine("Max", "trans", "Violations", line)
            foundMaxCapVi = QorRpt.mathcLine("Max", "Cap", "Violations", line)
            foundMaxFanVi = QorRpt.mathcLine("Max", "Fanout", "Violations", line)

            if foundCellCount:
                QorRptData.foundCellCount = QorRpt.replaceSpace(stage + " Cell Count"), foundCellCount.group(2)
                reportDataItems.append(rptData.foundCellCount)
            elif foundCompileTime:
                rptData.foundCompileTime = QorRpt.replaceSpace(stage + " cpu runtime"), foundCompileTime.group(2)
                reportDataItems.append(rptData.foundCompileTime)
            elif foundMaxTransVi:
                rptData.foundMaxTransVi = QorRpt.replaceSpace(stage + " max trans viols"), foundMaxTransVi.group(2)
                reportDataItems.append(rptData.foundMaxTransVi)
            elif foundMaxCapVi:
                rptData.foundMaxCapVi = QorRpt.replaceSpace(stage + " max cap viols"), foundMaxCapVi.group(2)
                reportDataItems.append(rptData.foundMaxCapVi)
            elif foundMaxFanVi:
                rptData.foundMaxFanVi = QorRpt.replaceSpace(stage + " max fanout viols"), foundMaxFanVi.group(2)
                reportDataItems.append(rptData.foundMaxFanVi)

        return reportDataItems
