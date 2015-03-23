class DrcLvs:

    import re
    from Metrics import Metric

    MetricNames = []
    # Open the file with read only permit
    f = open(r'C:\python\ppa\cpu_testcase\apr\cpu.fill.physical.rpt', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    for line in lines:
        foundUtil = re.search(r'(Std[\s]*cells[\s]*utilization):+[\s]*([\d]+[\.]*[\d]*%+)+.*', line, re.I)