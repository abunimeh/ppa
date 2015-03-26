class QorRptData:
    def outData(self, metric):
        print(metric.group(1), metric.group(2))

    def CreateCsv(self, metricNames):
        import csv
        names = ["%s" % i[0] for i in metricNames]
        values = ["%s" % i[1] for i in metricNames]
        with open(r'C:\Dev\Work\Toms Work\Intel\ppa\goodfile.csv', 'wt') as myfile:
            writer = csv.writer(myfile, lineterminator='\n')
            #for val in metricNames:
            writer.writerow(names)
            writer.writerow(values)
        myfile.close()

class QorRpt:
    pass
    def mathcLine(regex1, regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    def searchfile():
        import re
        reportDataItems = []

        # Open the file with read only permit
        f = open(r'C:\Dev\Work\Toms Work\Intel\ppa\cpu_testcase\syn\cpu.inc_compile.qor.rpt', "r")

        # use readlines to read all lines in the file
        # The variable "lines" is a list containing all lines
        lines = f.readlines()

        # lookCount is used to search a certain amount after reg2reg
        lookCount = 0

        # close the file after reading the lines.
        f.close()
        rptData = QorRptData()

        for line in lines:
            rptData.foundRegGroup = re.search(r'.*(REG2REG).*', line, re.I)
            foundVersion = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
            if foundVersion:
                rptData.foundVersion = QorRpt.replaceSpace(foundVersion.group(1)), foundVersion.group(2)
                reportDataItems.append(rptData.foundVersion)
            if rptData.foundRegGroup:
                lookCount = 10
            if lookCount != 0:
                foundCritSlack = QorRpt.mathcLine("Critical", "path", "slack", line)
                foundWorstHoldVio = QorRpt.mathcLine("Worst", "hold", "violation", line)
                foundCritPathLength = QorRpt.mathcLine("critical", "path", "length", line)
                foundTotNegSlack = QorRpt.mathcLine("total", "Negative", "slack", line)
                foundTotHoldVio = QorRpt.mathcLine("total", "hold", "violation", line)

                if foundCritSlack:
                    rptData.foundCritSlack = QorRpt.replaceSpace(foundCritSlack.group(1)), foundCritSlack.group(2)
                    reportDataItems.append(rptData.foundCritSlack)
                if foundWorstHoldVio:
                    rptData.foundWorstHoldVio = QorRpt.replaceSpace(foundWorstHoldVio.group(1)), foundWorstHoldVio.group(2)
                    reportDataItems.append(rptData.foundWorstHoldVio)
                if foundCritPathLength:
                    rptData.foundCritPathLength = QorRpt.replaceSpace(foundCritPathLength.group(1)), foundCritPathLength.group(2)
                    reportDataItems.append(rptData.foundCritPathLength)
                if foundTotNegSlack:
                    rptData.foundTotNegSlack = QorRpt.replaceSpace(foundTotNegSlack.group(1)), foundTotNegSlack.group(2)
                    reportDataItems.append(rptData.foundTotNegSlack)
                if foundTotHoldVio:
                    rptData.foundTotHoldVio = QorRpt.replaceSpace(foundTotHoldVio.group(1)), foundTotHoldVio.group(2)
                    reportDataItems.append(rptData.foundTotHoldVio)
                lookCount -= 1

            foundCellCount = QorRpt.mathcLine("Leaf", "Cell", "Count", line)
            foundCompileTime = QorRpt.mathcLine("Overall", "Compile", "Time", line)
            foundMaxTransVi = QorRpt.mathcLine("Max", "trans", "Violations", line)
            foundMaxCapVi = QorRpt.mathcLine("Max", "Cap", "Violations", line)
            foundMaxFanVi = QorRpt.mathcLine("Max", "trans", "Violations", line)

            #rptData.outData()

            if foundCellCount:
                rptData.foundCellCount = QorRpt.replaceSpace(foundCellCount.group(1)), foundCellCount.group(2)
                reportDataItems.append(rptData.foundCellCount)
            if foundCompileTime:
                rptData.foundCompileTime = QorRpt.replaceSpace(foundCompileTime.group(1)), foundCompileTime.group(2)
                reportDataItems.append(rptData.foundCompileTime)
            if foundMaxTransVi:
                rptData.foundMaxTransVi = QorRpt.replaceSpace(foundMaxTransVi.group(1)), foundMaxTransVi.group(2)
                reportDataItems.append(rptData.foundMaxTransVi)
            if foundMaxCapVi:
                rptData.foundMaxCapVi = QorRpt.replaceSpace(foundMaxCapVi.group(1)), foundMaxCapVi.group(2)
                reportDataItems.append(rptData.foundMaxCapVi)
            if foundMaxFanVi:
                rptData.foundMaxFanVi = QorRpt.replaceSpace(foundMaxFanVi.group(1)), foundMaxFanVi.group(2)
                reportDataItems.append(rptData.foundMaxFanVi)
        rptData.CreateCsv(reportDataItems)
        return reportDataItems