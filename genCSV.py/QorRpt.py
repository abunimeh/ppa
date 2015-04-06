from test.test_tools import basepath


class QorRptData:
    def outData(self, metric):
        print(metric.group(1), metric.group(2))

    def CreateCsv(self, metricNames):
        import csv
        from Configurations import Configurations
        names = ["%s" % i[0] for i in metricNames]
        values = ["%s" % i[1] for i in metricNames]
        base_path = Configurations().parser_final()

        with open(base_path + "goodfile.csv", 'wt') as myfile:
            writer = csv.writer(myfile, lineterminator='\n')
            #for val in metricNames:
            writer.writerow(names)
            writer.writerow(values)
        myfile.close()


class QorRpt:
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

    def mathcLine(regex1, regex2, regex3, line):
        import re
        line_variables = r'(%s[\s]*%s[\s]*%s[\s]*):+[\s]*(-*[\d]+[\.]*[\d]*)+.*' % (regex1, regex2, regex3)
        result = re.search(line_variables, line, re.I)
        return result

    def replaceSpace(metricname):
        import re
        new_name = re.sub(r'[\W]+', "_", metricname)
        return new_name

    def searchfile(file):
        import re
        from Configurations import Configurations
        from operator import itemgetter
        stage = QorRpt.metric_naming(file)
        base_path = Configurations().parser_final()
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()

        # lookCount is used to search a certain amount after reg2reg
        lookCount = 0
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
            if rptData.foundRegGroup:
                lookCount = 10
            if lookCount != 0:
                foundCritSlack = QorRpt.mathcLine("Critical", "path", "slack", line)
                foundWorstHoldVio = QorRpt.mathcLine("Worst", "hold", "violation", line)
                foundCritPathLength = QorRpt.mathcLine("critical", "path", "length", line)
                foundTotNegSlack = QorRpt.mathcLine("total", "Negative", "slack", line)
                foundTotHoldVio = QorRpt.mathcLine("total", "hold", "violation", line)

                if foundCritSlack:
                    rptData.foundCritSlack = QorRpt.replaceSpace(stage + " REG2REG " + "worst setup viol"), foundCritSlack.group(2)
                    reportDataItems.append(rptData.foundCritSlack)
                if foundWorstHoldVio:
                    rptData.foundWorstHoldVio = QorRpt.replaceSpace(stage + " REG2REG " + "worst hold viol"), foundWorstHoldVio.group(2)
                    reportDataItems.append(rptData.foundWorstHoldVio)
                if foundCritPathLength:
                    rptData.foundCritPathLength = QorRpt.replaceSpace(stage + " REG2REG " + "critical path len"), foundCritPathLength.group(2)
                    reportDataItems.append(rptData.foundCritPathLength)
                if foundTotNegSlack:
                    rptData.foundTotNegSlack = QorRpt.replaceSpace(stage + " REG2REG " + "total neg slack"), foundTotNegSlack.group(2)
                    reportDataItems.append(rptData.foundTotNegSlack)
                if foundTotHoldVio:
                    rptData.foundTotHoldVio = QorRpt.replaceSpace(stage + " REG2REG " + "total hold viol"), foundTotHoldVio.group(2)
                    reportDataItems.append(rptData.foundTotHoldVio)
                lookCount -= 1

            foundCellCount = QorRpt.mathcLine("Leaf", "Cell", "Count", line)
            foundCompileTime = QorRpt.mathcLine("Overall", "Compile", "Time", line)
            foundMaxTransVi = QorRpt.mathcLine("Max", "trans", "Violations", line)
            foundMaxCapVi = QorRpt.mathcLine("Max", "Cap", "Violations", line)
            foundMaxFanVi = QorRpt.mathcLine("Max", "trans", "Violations", line)

            if foundCellCount:
                rptData.foundCellCount = QorRpt.replaceSpace(stage + " Cell Count"), foundCellCount.group(2)
                reportDataItems.append(rptData.foundCellCount)
            if foundCompileTime:
                rptData.foundCompileTime = QorRpt.replaceSpace(stage + " cpu runtime"), foundCompileTime.group(2)
                reportDataItems.append(rptData.foundCompileTime)
            if foundMaxTransVi:
                rptData.foundMaxTransVi = QorRpt.replaceSpace(stage + " max trans viols"), foundMaxTransVi.group(2)
                reportDataItems.append(rptData.foundMaxTransVi)
            if foundMaxCapVi:
                rptData.foundMaxCapVi = QorRpt.replaceSpace(stage + " max cap viols"), foundMaxCapVi.group(2)
                reportDataItems.append(rptData.foundMaxCapVi)
            if foundMaxFanVi:
                rptData.foundMaxFanVi = QorRpt.replaceSpace(stage + " max fanout viols"), foundMaxFanVi.group(2)
                reportDataItems.append(rptData.foundMaxFanVi)
        print(["%s" % i[0] for i in reportDataItems], ["%s" % i[1] for i in reportDataItems])
        data_items = sorted(reportDataItems, key=itemgetter(0))
        return ["%s" % i[0] for i in data_items], ["%s" % i[1] for i in data_items]