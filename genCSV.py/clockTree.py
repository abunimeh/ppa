class clockTreeRptData:
    @staticmethod
    def outdata(metric_list):
        for metrics in metric_list:
            print(metrics)

class clockTreeRpt:
    @staticmethod
    def searchfile(file):
        import re
        from operator import itemgetter
        DataItems = []
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        rptData = clockTreeRptData()

        for line in lines:
            found_max_globe_skew = re.search(r'(Max[\s]*global[\s]*skew)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if found_max_globe_skew:
                rptData.foundMaxGlobeSkew = "apr_cts_max_global_skew", found_max_globe_skew.group(2)
                DataItems.append(rptData.foundMaxGlobeSkew)

        data_items = sorted(DataItems, key=itemgetter(0))
        #return ["%s" % i[0] for i in data_items], ["%s" % i[1] for i in data_items]
        return data_items

