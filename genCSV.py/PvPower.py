
class PvPower:
    import re
    from Metrics import Metric

    MetricNames = []
    # Open the file with read only permit
    f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\pv_runs\power\cpu.power.power.rpt', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    for line in lines:
        foundCInternPwr = re.search(r'(Cell[\s]*Internal[\s]*Power)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+[\s]*', line, re.I)
        foundCLeakPwr = re.search(r'(Cell[\s]*Leakage[\s]*Power)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+.[\s]*', line, re.I)
        foundNetSwPwr = re.search(r'(Net[\s]*switching[\s]*power)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+[\s]*', line, re.I)
        foundTotalPwr = re.search(r'(Total[\s]*Power)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+[\s]*', line, re.I)

        if foundCInternPwr:
            CInternPwr = re.sub(r'[\W]+', "_", foundCInternPwr.group(1))
            MetricNames.append(Metric(CInternPwr, foundCInternPwr.group(2)))
        if foundCLeakPwr:
            CLeakPwr = re.sub(r'[\W]+', "_", foundCLeakPwr.group(1))
            MetricNames.append(Metric(CLeakPwr, foundCLeakPwr.group(2)))
        if foundNetSwPwr:
            NetSwPwr = re.sub(r'[\W]+', "_", foundNetSwPwr.group(1))
            MetricNames.append(Metric(NetSwPwr, foundNetSwPwr.group(2)))
        if foundTotalPwr:
            TotalPwr = re.sub(r'[\W]+', "_", foundTotalPwr.group(1))
            MetricNames.append(Metric(TotalPwr, foundTotalPwr.group(2)))

    for met in MetricNames:
        print(met.name, met.value)