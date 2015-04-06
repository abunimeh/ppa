class PVTMetricData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)


class PVTMetric:
    def metric_naming(file):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', file, re.I)
        apr = re.search(r'.*apr.*', file, re.I)
        pv_max = re.search(r'.*pv.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*', file, re.I)
        pv_power = re.search(r'.*pv.*power.*', file, re.I)
        if syn:
            stage = 'syn'
        if apr:
            stage = 'apr'
        if pv_max:
            stage = 'pv_max'
        if pv_min:
            stage = 'pv_min'
        if pv_noise:
            stage = 'pv_noise'
        if pv_power:
            stage = 'pv_power'
        return stage

    def searchfile(file):
        import re
        from Configurations import Configurations
        from operator import itemgetter
        base_path = Configurations().parser_final()
        stage = PVTMetric.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        DataItems = []
        foundValue = []
        value_sum = ""
        value = 0
        pvtdata = PVTMetricData()
        for line in lines:
            found_db_file = re.search(r'(Loading[\s]*db[\s]*file).*_([rx\d]+_[prt][sft]+_[\d\.]+v_[-]*[\d]+c_[\w]+)', line, re.I)
            if found_db_file:
                value = found_db_file.group(2)
                if value not in foundValue:
                    foundValue.append(value)
        for value in foundValue:
            value_sum += (value+" ")
        if value:
            pvtdata.foundDBfile = (stage + "_pvt"), value_sum
            DataItems.append(pvtdata.foundDBfile)

        data_items = sorted(DataItems, key=itemgetter(0))
        return ["%s" % i[0] for i in data_items], ["%s" % i[1] for i in data_items]
