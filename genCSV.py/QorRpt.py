
class QorRpt:

    import re
    from Metrics import Metric

    # Open the file with read only permit
    f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\syn\cpu.inc_compile.qor.rpt', "r")

    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()

    # lookCount is used to search a certain amount of lines after reading reg2reg
    lookCount = 0
    MetricNames = []

    # close the file after reading the lines.
    f.close()
    for line in lines:
        foundVersion = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
        foundRegGroup = re.search(r'.*(REG2REG).*', line, re.M | re.I)

        if foundVersion:
            MetricNames.append(Metric(foundVersion.group(1), foundVersion.group(2)))
        if foundRegGroup:
            lookCount = 10
        if lookCount != 0:

            foundCritSlack = re.search(r'(Critical[\s]*path[\s]*slack):+[\s]*([\d]+[\.?][\d]+).*', line, re.I)
            foundWorstHoldVio = re.search(r'(Worst[\s]*hold[\s]*violation):+[\s]*([\d]+[\.?][\d]+).*', line, re.I)
            foundCritPathLength = re.search(r'(critical[\s]*path[\s]*length):+[\s]*([\d]+[\.?][\d]+).*', line, re.I)
            foundTotNegSlack = re.search(r'(total[\s]*Negative[\s]*slack):+[\s]*([\d]+[\.?][\d]+).*', line, re.I)
            foundTotHoldVio = re.search(r'(total[\s]*hold[\s]*violation):+[\s]*([\d]+[\.?][\d]+).*', line, re.I)

            if foundCritSlack:
                CritSlack = re.sub(r'[\W]+', "_", foundCritSlack.group(1))
                MetricNames.append(Metric(CritSlack, foundCritSlack.group(2)))
            if foundWorstHoldVio:
                WorstHoldVio = re.sub(r'[\W]+', "_", foundWorstHoldVio.group(1))
                MetricNames.append(Metric(WorstHoldVio, foundWorstHoldVio.group(2)))
            if foundCritPathLength:
                CritPathLength = re.sub(r'[\W]+', "_", foundCritPathLength.group(1))
                MetricNames.append(Metric(CritPathLength, foundCritPathLength.group(2)))
            if foundTotNegSlack:
                TotNegSlack = re.sub(r'[\W]+', "_", foundTotNegSlack.group(1))
                MetricNames.append(Metric(TotNegSlack, foundTotNegSlack.group(2)))
            if foundTotHoldVio:
                TotHoldVio = re.sub(r'[\W]+', "_", foundTotHoldVio.group(1))
                MetricNames.append(Metric(TotHoldVio, foundTotHoldVio.group(2)))
            lookCount -= 1

        # personal Note Come back for more detailed search!!!

        foundCellCount = re.search(r'(Leaf[\s]*Cell[\s]*Count[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
        foundCompileTime = re.search(r'(Overall[\s]*Compile[\s]*Time[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
        foundMaxTransVi = re.search(r'(Max[\s]*trans[\s]*Violations[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
        foundMaxCapVi = re.search(r'(Max[\s]*Cap[\s]*Violations[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
        foundMaxFanVi = re.search(r'(Max[\s]*Fanout[\s]*Violations[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

        if foundCellCount:
            CellCount = re.sub(r'[\W]+', "_", foundCellCount.group(1))
            MetricNames.append(Metric(CellCount, foundCellCount.group(2)))
        if foundCompileTime:
            CompileTime = re.sub(r'[\W]+', "_", foundCompileTime.group(1))
            MetricNames.append(Metric(CompileTime, foundCompileTime.group(2)))
        if foundMaxTransVi:
            MaxTransVi = re.sub(r'[\W]+', "_", foundMaxTransVi.group(1))
            MetricNames.append(Metric(MaxTransVi, foundMaxTransVi.group(2)))
        if foundMaxCapVi:
            MaxCapVi = re.sub(r'[\W]+', "_", foundMaxCapVi.group(1))
            MetricNames.append(Metric(MaxCapVi, foundMaxCapVi.group(2)))
        if foundMaxFanVi:
            MaxFanVi = re.sub(r'[\W]+', "_", foundMaxFanVi.group(1))
            MetricNames.append(Metric(MaxFanVi, foundMaxFanVi.group(2)))

    for met in MetricNames:
            print(met.name, met.value)