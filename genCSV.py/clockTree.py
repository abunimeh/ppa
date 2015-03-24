
class clockTree:
    import re
    from Metrics import Metric

    MetricNames = []
    # Open the file with read only permit
    f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\apr\cpu.cts.clock_tree.rpt', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    for line in lines:
        foundMaxGlobeSkew = re.search(r'(Max[\s]*global[\s]*skew)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

        if foundMaxGlobeSkew:
            MGS = re.sub(r'[\W]+', "_", foundMaxGlobeSkew.group(1))
            MetricNames.append(Metric(MGS, foundMaxGlobeSkew.group(2)))

    for met in MetricNames:
        print(met.name, met.value)