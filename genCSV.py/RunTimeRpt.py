class RunTimeRptData:
    pass

class RunTimeRpt:

    def SearchFile(self):
        import re
        from Metrics import Metric

        MetricNames = []
        # Open the file with read only permit
        f = open(r'C:\dev\ppa\ppa\cpu_testcase\pv_runs\max\cpu.run_time.rpt', "r")
        # use readlines to read all lines in the file
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        rptData = RunTimeRptData()

        for line in lines:
            rptData.foundRunTime = re.search(r'(Runtime[\s]*of[\s]*Entire[\s]*Timing[\s]*Run)[\s]*=+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if foundRunTime:
                rptData.RunTime = re.sub(r'[\W]+', "_", foundRunTime.group(1))
                MetricNames.append(Metric(RunTime, foundRunTime.group(2)))

        for met in MetricNames:
            print(met.name, met.value)