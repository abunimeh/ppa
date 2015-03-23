
class PVTmetric:
    pass
    import re
    from Metrics import Metric

    MetricNames = []
    variableName = []
    # Open the file with read only permit
    #f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\syn\dc.log', "r")
    f = open(r'C:\python\ppa\cpu_testcase\syn\dc.log', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    for line in lines:
        foundDBfile = re.search(r'(Loading[\s]*db[\s]*file).*_([rx\d]+_[prt][sft]+_[\d\.]+v_[-]*[\d]+c_[\w]+)', line, re.I)
        if foundDBfile:
            DBfile = re.sub(r'[\W]+', "_", foundDBfile.group(1))
            value = foundDBfile.group(2)
            if value not in MetricNames:
                variableName.append(value)
                MetricNames.append(Metric(DBfile, value))
    for met in MetricNames:
        print(met.name, met.value)