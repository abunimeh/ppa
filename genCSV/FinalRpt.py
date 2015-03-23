class FinalRpt:

    import re
    from Metrics import Metric

    MetricNames = []
    # Open the file with read only permit
    f = open(r'C:\python\ppa\cpu_testcase\drc_lvs\denall\Final_Report.txt', "r")
    # use readlines to read all lines in the file
    # The variable "lines" is a list containing all lines
    lines = f.readlines()
    f.close()

    for line in lines:
        foundNumOfActuEr = re.search(r'(The[\s]*number[\s]*of[\s]*actual[\s]*errors)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

        if foundNumOfActuEr:
            NumOfActuEr = re.sub(r'[\W]+', "_", foundNumOfActuEr.group(1))
            MetricNames.append(Metric(NumOfActuEr, foundNumOfActuEr.group(2)))

    for met in MetricNames:
        print(met.name, met.value)