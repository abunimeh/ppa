class PVTMetricData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class PVTMetric:
    pass
    def searchfile():
        import re
        from Configurations import Configurations
        base_path = Configurations().parser_final()

        # Open the file with read only permit
        f = open(base_path + r'cpu_testcase\apr\icc.log', "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        DataItems = []
        foundValue = []
        theValue = ""
        pvtdata = PVTMetricData()
        for line in lines:
            foundDBfile = re.search(r'(Loading[\s]*db[\s]*file).*_([rx\d]+_[prt][sft]+_[\d\.]+v_[-]*[\d]+c_[\w]+)', line, re.I)
            if foundDBfile:
                Dbfile = re.sub(r'[\W]+', "_", foundDBfile.group(1))
                value = foundDBfile.group(2)
                if value not in foundValue:
                    foundValue.append(value)
        for value in foundValue:
            theValue += (value+" ")
        if Dbfile:
            pvtdata.foundDBfile = (Dbfile, theValue)
            DataItems.append(pvtdata.foundDBfile)
        return ["%s" % i[0] for i in DataItems], ["%s" % i[1] for i in DataItems]
