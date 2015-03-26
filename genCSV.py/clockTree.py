class clockTreeRptData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)
class clockTreeRpt:
    def searchfile():
        import re

        DataItems = []
        # Open the file with read only permit
        f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\apr\cpu.cts.clock_tree.rpt', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        rptData = clockTreeRptData()

        for line in lines:
            foundMaxGlobeSkew = re.search(r'(Max[\s]*global[\s]*skew)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if foundMaxGlobeSkew:
                rptData.foundMaxGlobeSkew = foundMaxGlobeSkew.group(1),foundMaxGlobeSkew.group(2)
                DataItems.append(rptData.foundMaxGlobeSkew)

        rptData.outdata(DataItems)