class clockTreeRptData:
    pass
class clockTreeRpt:
    @staticmethod
    def searchfile(file):
        import re
        data_items = []
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        rptData = clockTreeRptData()
        rptData.foundMaxGlobeSkew = ["apr_cts_max_global_skew", "N/A"]

        for line in lines:
            found_max_globe_skew = re.search(r'(Max[\s]*global[\s]*skew)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
            if found_max_globe_skew:
                rptData.foundMaxGlobeSkew = "apr_cts_max_global_skew", found_max_globe_skew.group(2)
                data_items.append(tuple(rptData.foundMaxGlobeSkew))
                break

        return data_items

