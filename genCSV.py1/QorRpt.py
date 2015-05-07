
class QorRptData:
    pass


class QorRpt:

    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', file, re.I)
        apr = re.search(r'.*apr.*', file, re.I)
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)
        if apr:
            stage = 'apr'
        elif pv_max:
            stage = 'pv max tttt'
        elif pv_min:
            stage = 'pv min tttt'
        elif pv_noise:
            stage = 'pv noise tttt'
        elif syn:
            stage = 'syn'
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
        rptData.foundVersion = [QorRpt.replaceSpace(stage + " tool version"), "N/A"]
        rptData.foundCritSlack = [QorRpt.replaceSpace(stage + " REG2REG " + "worst setup viol"), "N/A"]
        if 'pv min' in stage:
            rptData.foundCritSlack[0] = QorRpt.replaceSpace(stage + " REG2REG " + "worst hold viol")
        rptData.foundWorstHoldVio = [QorRpt.replaceSpace(stage + " REG2REG " + "worst hold violation"), "N/A"]
        rptData.foundCritPathLength = [QorRpt.replaceSpace(stage + " REG2REG " + "critical path len"), "N/A"]
        rptData.foundTotNegSlack = [QorRpt.replaceSpace(stage + " REG2REG " + "total neg slack"), "N/A"]
        rptData.foundTotHoldVio = [QorRpt.replaceSpace(stage + " REG2REG " + "total hold viol"), "N/A"]
        QorRptData.foundCellCount = [QorRpt.replaceSpace(stage + " Cell Count"), "N/A"]
        rptData.foundCompileTime = [QorRpt.replaceSpace(stage + " cpu runtime"), "N/A"]
        rptData.foundMaxTransVi = [QorRpt.replaceSpace(stage + " max trans viols"), "N/A"]
        rptData.foundMaxCapVi = [QorRpt.replaceSpace(stage + " max cap viols"), "N/A"]
        rptData.foundMaxFanVi = [QorRpt.replaceSpace(stage + " max fanout viols"), "N/A"]

        for line in lines:
            rptData.foundRegGroup = re.search(r'.*(REG2REG).*', line, re.I)
            foundVersion = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
            if foundVersion:
                rptData.foundVersion[1] = foundVersion.group(2)
            elif rptData.foundRegGroup:
                if 'pv max tttt' in stage:
                    if 'max_delay/setup' in line:
                        look_count = 10
                elif 'pv min tttt' in stage:
                    if 'min_delay/hold' in line:
                        look_count = 10
                else:
                    look_count = 10
            elif look_count != 0 and stage != 'pv noise tttt':
                foundCritSlack = QorRpt.mathcLine("Critical", "path", "slack", line)
                foundWorstHoldVio = QorRpt.mathcLine("Worst", "hold", "violation", line)
                foundCritPathLength = QorRpt.mathcLine("critical", "path", "length", line)
                foundTotNegSlack = QorRpt.mathcLine("total", "Negative", "slack", line)
                foundTotHoldVio = QorRpt.mathcLine("total", "hold", "violation", line)
                found_new_section = re.search(r'.*Timing[\s]*Path[\s]*Group.*', line, re.I)

                if foundCritSlack:
                    rptData.foundCritSlack[1] = foundCritSlack.group(2)
                elif foundWorstHoldVio:
                    rptData.foundWorstHoldVio[1] = foundWorstHoldVio.group(2)
                elif foundCritPathLength:
                    rptData.foundCritPathLength[1] = foundCritPathLength.group(2)
                elif foundTotNegSlack:
                    rptData.foundTotNegSlack[1] = foundTotNegSlack.group(2)
                elif foundTotHoldVio:
                    rptData.foundTotHoldVio[1] = foundTotHoldVio.group(2)
                elif found_new_section:
                    look_count = 0

            foundCellCount = QorRpt.mathcLine("Leaf", "Cell", "Count", line)
            foundCompileTime = QorRpt.mathcLine("Overall", "Compile", "Time", line)
            foundMaxTransVi = QorRpt.mathcLine("Max", "trans", "Violations", line)
            foundMaxCapVi = QorRpt.mathcLine("Max", "Cap", "Violations", line)
            foundMaxFanVi = QorRpt.mathcLine("Max", "Fanout", "Violations", line)

            if foundCellCount:
                rptData.foundCellCount[1] = foundCellCount.group(2)
            elif foundCompileTime:
                rptData.foundCompileTime[1] = foundCompileTime.group(2)
            elif foundMaxTransVi:
                rptData.foundMaxTransVi[1] = foundMaxTransVi.group(2)
            elif foundMaxCapVi:
                rptData.foundMaxCapVi[1] = foundMaxCapVi.group(2)
            elif foundMaxFanVi:
                rptData.foundMaxFanVi[1] = foundMaxFanVi.group(2)

        reportDataItems.append(tuple(rptData.foundVersion))
        reportDataItems.append(tuple(rptData.foundCritSlack))
        reportDataItems.append(tuple(rptData.foundWorstHoldVio))
        reportDataItems.append(tuple(rptData.foundCritPathLength))
        reportDataItems.append(tuple(rptData.foundTotNegSlack))
        reportDataItems.append(tuple(rptData.foundTotHoldVio))
        reportDataItems.append(tuple(rptData.foundCellCount))
        reportDataItems.append(tuple(rptData.foundCompileTime))
        reportDataItems.append(tuple(rptData.foundMaxTransVi))
        reportDataItems.append(tuple(rptData.foundMaxCapVi))
        reportDataItems.append(tuple(rptData.foundMaxFanVi))

        return reportDataItems
