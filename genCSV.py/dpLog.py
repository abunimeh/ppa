class dpLog:

    import re
    from Metrics import Metric

    foundFlag = 0
    MetricNames = []
    # Open the file with read only permit
    f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\drc_lvs\trclvs\trclvs.dp.log', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    #reversed in order to find the last value in the file
    for line in reversed(lines):
        foundPeakMem = re.search(r':+[\s]*(Peak)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\s]*\(mb\)+)+', line, re.I)
        foundRuntime = re.search(r'(Overall[\s]*engine[\s]*time)[\s]*=+[\s]*([\d]*:*[\d]*:*[\d]+)+', line, re.I)

        if foundPeakMem and foundFlag != 1:
            MetricNames.append(Metric(foundPeakMem.group(1), foundPeakMem.group(2)))
            foundFlag = 1
        if foundRuntime:
            Runtime = re.sub(r'[\W]+', "_", foundRuntime.group(1))
            MetricNames.append(Metric(Runtime, foundRuntime.group(2)))

    for metric in MetricNames:
        print(metric.name, metric.value)