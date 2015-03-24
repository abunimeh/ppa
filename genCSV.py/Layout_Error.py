class LayoutError:

    import re
    from Metrics import Metric

    violationCount = 0
    MetricNames = []
    # Open the file with read only permit
    f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\drc_lvs\denall\cpu.LAYOUT_ERRORS', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    for line in lines:
        foundToolVersion = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
        foundViolation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)

        if foundToolVersion:
            ToolVersion = re.sub(r'[\W]+', "_", foundToolVersion.group(1))
            MetricNames.append(Metric(ToolVersion, foundToolVersion.group(2)))
        if foundViolation:
            violationCount += int(foundViolation.group(1))

    MetricNames.append(Metric("Violations", violationCount))

    for metric in MetricNames:
        print(metric.name, metric.value)
