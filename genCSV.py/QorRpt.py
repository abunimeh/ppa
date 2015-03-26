class QorRptData:
    def outData(self, metric):
        print(metric.group(1), metric.group(2))

    def CreateCsv(metricNames):
        import csv
        from itertools import zip_longest
        acsvfile = open('C:\Dev\Work\Toms Work\Intel\ppa\cpu_testcase\csvtest.csv', 'w+')
        thecsv = csv.writer(acsvfile, delimiter=',')
        #rows = ([metricNames] for metrics in metricNames)
        rows =""
        row2 =""
        for metrics in metricNames:
            rows += (metrics.name + " , ")
            row2 += metrics.value + " , "
            thecsv.writerow(zip_longest(metrics.name, metrics.value))
        print(rows)
        print(row2)

        thecsv.writerow([row2])
        acsvfile.close()

class QorRpt:
    pass
    def mathcLine(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname.group(1))
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
            rptData.foundVersion = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
            if rptData.foundVersion:
                reportDataItems.append(rptData.foundVersion)
            if rptData.foundRegGroup:
                lookCount = 10
            if lookCount != 0:
                rptData.foundCritSlack = QorRpt.mathcLine("Critical", "path", "slack", line)
                rptData.foundWorstHoldVio = QorRpt.mathcLine("Worst", "hold", "violation", line)
                rptData.foundCritPathLength = QorRpt.mathcLine("critical", "path", "length", line)
                rptData.foundTotNegSlack = QorRpt.mathcLine("total", "Negative", "slack", line)
                rptData.foundTotHoldVio = QorRpt.mathcLine("total", "hold", "violation", line)

                if rptData.foundCritSlack:
                    reportDataItems.append(rptData.foundCritSlack)
                if rptData.foundWorstHoldVio:
                    reportDataItems.append(rptData.foundWorstHoldVio)
                if rptData.foundCritPathLength:
                    reportDataItems.append(rptData.foundCritPathLength)
                if rptData.foundTotNegSlack:
                    reportDataItems.append(rptData.foundTotNegSlack)
                if rptData.foundTotHoldVio:
                    reportDataItems.append(rptData.foundTotHoldVio)
                lookCount -= 1

            rptData.foundCellCount = QorRpt.mathcLine("Leaf", "Cell", "Count", line)
            rptData.foundCompileTime = QorRpt.mathcLine("Overall", "Compile", "Time", line)
            rptData.foundMaxTransVi = QorRpt.mathcLine("Max", "trans", "Violations", line)
            rptData.foundMaxCapVi = QorRpt.mathcLine("Max", "Cap", "Violations", line)
            rptData.foundMaxFanVi = QorRpt.mathcLine("Max", "trans", "Violations", line)

            #rptData.outData()

            if rptData.foundCellCount:
                QorRpt.replaceSpace(rptData.foundCellCount)
                reportDataItems.append(rptData.foundCellCount)
            if rptData.foundCompileTime:
                reportDataItems.append(rptData.foundCompileTime)
            if rptData.foundMaxTransVi:
                reportDataItems.append(rptData.foundMaxTransVi)
            if rptData.foundMaxCapVi:
                reportDataItems.append(rptData.foundMaxCapVi)
            if rptData.foundMaxFanVi:
                reportDataItems.append(rptData.foundMaxFanVi)

        for metrics in reportDataItems:
            qdata =QorRptData()
            qdata.outData(metrics)
        #QorRptData.CreateCsv()