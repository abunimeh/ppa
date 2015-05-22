class PVTMetricData:
    pass

class PVTMetric:
    # This class is not part of the configuration
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        syn = re.search(r'.*syn.*', file, re.I)
        apr = re.search(r'.*apr.*', file, re.I)
        pv_max = re.search(r'.*pv.*max.*|.*sta.*max.*', file, re.I)
        pv_min = re.search(r'.*pv.*min.*|.*sta.*min.*', file, re.I)
        pv_power = re.search(r'.*pv.*power.*|.*sta.*power.*', file, re.I)
        pv_noise = re.search(r'.*pv.*noise.*|.*sta.*noise.*', file, re.I)

        if apr:
            stage = 'apr'
        elif pv_max:
            stage = 'pv_max'
        elif pv_min:
            stage = 'pv_min'
        elif pv_noise:
            stage = 'pv_noise'
        elif pv_power:
            stage = 'pv_power'
        elif syn:
            stage = 'syn'
        return stage

    @staticmethod
    def search_file(file):
        import re
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
            found_db_file = re.search(r'(Loading[\s]*db[\s]*file).*/[\w]*_[\w]*_[\w]*_([rx\d]+[\w]+_[\w]+_[\d\.]+v_[-]*[\d]+c_[\w]+)', line, re.I)
            if file.endswith("icc.log"):
                found_kit = re.search(r'(==>SOURCING:)[\s]*.*/([afdkitcsr\._\d]+[\d]+[afdkitcsr\._\d]+)/', line)
                if found_kit:
                    pvtdata.found_kit = "Kit", found_kit.group(2)
                    DataItems.append(pvtdata.found_kit)
            if found_db_file:
                value = found_db_file.group(2)
                if value not in foundValue:
                    foundValue.append(value)
        for values in foundValue:
            value_sum += (values+" ")
        if value:
            pvtdata.found_db_file = (stage + "_pvt"), value_sum
            DataItems.append(pvtdata.found_db_file)


        return DataItems
