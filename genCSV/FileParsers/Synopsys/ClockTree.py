class clockTreeRptData:
    pass
class clockTreeRpt:
    @staticmethod
    def search_file(file):
        import re
        from OrganizingAndFormatingMetrics.FormatMetrics import FormatMetrics
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
                rptData.foundMaxGlobeSkew = "apr_cts_max_global_skew", FormatMetrics.format_metric_values(found_max_globe_skew.group(2))
                data_items.append(tuple(rptData.foundMaxGlobeSkew))
                break

        return data_items

