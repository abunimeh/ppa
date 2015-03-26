class PhysicalRpt:

    import re
    from Metrics import Metric

    MetricNames = []
    # Open the file with read only permit
    f = open(r'C:\dev\ppa\ppa\cpu_testcase\apr\cpu.fill.physical.rpt', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    for line in lines:
        foundUtil = re.search(r'(Std[\s]*cells[\s]*utilization):+[\s]*([\d]+[\.]*[\d]*%+)+.*', line, re.I)
        foundShort = re.search(r'(Short[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
        foundTotalEr = re.search(r'(Total[\s]*error[\s]*number[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
        foundTotalMem = re.search(r'(Total[\s]*Proc[\s]*Memory[\s]*):+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

        if foundUtil:
            Util = re.sub(r'[\W]+', "_", foundUtil.group(1))
            MetricNames.append(Metric(Util, foundUtil.group(2)))
        if foundShort:
            Short = re.sub(r'[\W]+', "_", foundShort.group(1))
            MetricNames.append(Metric(Short, foundShort.group(2)))
        if foundTotalEr:
            TotalEr = re.sub(r'[\W]+', "_", foundTotalEr.group(1))
            MetricNames.append(Metric(TotalEr, foundTotalEr.group(2)))
        if foundTotalMem:
            TotalMem = re.sub(r'[\W]+', "_", foundTotalMem.group(1))
            MetricNames.append(Metric(TotalMem, foundTotalMem.group(2)))

    for met in MetricNames:
        print(met.name, met.value)