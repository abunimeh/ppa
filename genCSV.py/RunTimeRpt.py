class RunTimeRptData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class RunTimeRpt:
    def searchfile():
        import re
        DataItems = []
        # Open the file with read only permit
        f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\pv_runs\max\cpu.run_time.rpt', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        rptData = RunTimeRptData()

        for line in lines:
            foundRunTime = re.search(r'(Runtime[\s]*of[\s]*Entire[\s]*Timing[\s]*Run)[\s]*=+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if foundRunTime:
                rptData.foundRunTime = (re.sub(r'[\W]+', "_", foundRunTime.group(1)), foundRunTime.group(2))
                DataItems.append(rptData.foundRunTime)

        return DataItems