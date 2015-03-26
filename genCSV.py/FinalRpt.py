class FinalRptData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class FinalRpt:
    def searchfile():
        import re
        DataItems = []
        # Open the file with read only permit
        f = open(r'C:\Users\dcart_000\Desktop\cpu_testcase\drc_lvs\denall\Final_Report.txt', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        rptData = FinalRptData()

        for line in lines:
            foundNumOfActuEr = re.search(r'(The[\s]*number[\s]*of[\s]*actual[\s]*errors)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if foundNumOfActuEr:
                rptData.foundNumOfActuEr = (re.sub(r'[\W]+', "_", foundNumOfActuEr.group(1)), foundNumOfActuEr.group(2))
                DataItems.append(rptData.foundNumOfActuEr)

        rptData.outdata(DataItems)