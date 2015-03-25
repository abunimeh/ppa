
"""description of class"""
class QorRpt:
    pass
    import re
    from Metrics import Metric
    from Configurations import Configurations

    # Open the file with read only permit
    #f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\syn\cpu.inc_compile.qor.rpt', "r")

    #print(Configurations.parser_final())

    #self is ok as long as you first initialize it
    base_path = Configurations().parser_final()
    print(base_path)

    #f = open(r'C:\python\ppa\cpu_testcase\syn\cpu.inc_compile.qor.rpt', "r")
    f = open(base_path + "syn\cpu.inc_compile.qor.rpt", "r")
    #import genCSV




    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()


    # lookCount is used to search a certain amount after reg2reg
    lookCount = 0
    MetricNames = []

    # close the file after reading the lines.
    f.close()
    for line in lines:
       # print(line)
        foundRegGroup = re.search(r'.*(REG2REG).*', line, re.M | re.I)
        foundVersion = re.search(r'(Version):[\s]*([\S]*)', line, re.I)
        if foundVersion:
            MetricNames.append(Metric(foundVersion.group(1), foundVersion.group(2)))
        if foundRegGroup:
            lookCount = 10
        if lookCount != 0:
            foundLineReg = re.search(r'([\w^]+[\D]*[\D]*):+[\s]*([\d]+[\.?][\d]+)+.*', line, re.I)
            if foundLineReg:
                LineReg = re.sub(r'[\W]+', "_", foundLineReg.group(1))
                MetricNames.append(Metric(LineReg, foundLineReg.group(2)))
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