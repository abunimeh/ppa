class PVTMetricData:
    pass

from FileParsers.Parser import Parser


class PVTMetric(Parser):
    def __init__(self, file):
        super(PVTMetric, self).__init__(file)

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

    def search_file(self):
        import re
        stage = PVTMetric.metric_naming(self.file)
        lines = self.get_file_lines()
        pvt_values = []
        value_sum = ""
        # pvt_value = 0
        # pvt_data = PVTMetricData()
        for line in lines:
            found_pvt_value = re.search(r'(Loading[\s]*db[\s]*file).*/[\w]*_[\w]*_[\w]*_([rx\d]+[\w]+_[\w]+_[\d\.]+v_[-]*[\d]+c_[\w]+)', line, re.I)
            if self.file.endswith("icc.log"):
                found_kit = re.search(r'(==>SOURCING:)[\s]*.*/([afdkitcsr]+[afdkitcsr\._\d]+[\d]+[afdkitcsr\._\d]+)/', line)
                if found_kit:
                    # pvt_data.found_kit = "Kit", found_kit.group(2)
                    self.metrics.append(("Kit", found_kit.group(2)))
            if found_pvt_value:
                pvt_value = found_pvt_value.group(2)
                if pvt_value not in pvt_values:
                    pvt_values.append(pvt_value)
        for pvt_value in pvt_values:
            value_sum += (pvt_value+" ")
        if len(pvt_values):
            #pvt_data.found_db_file = (stage + "_pvt"), value_sum
            self.metrics.append((stage + "_pvt", value_sum))
        if not self.check_list("Kit"):
            kit_in_file_name = re.search(r'/([a-zA-Z_]{1,3}[\d\.]+_[sScC]{1})/', self.file)
            if kit_in_file_name:
                self.metrics.append(kit_in_file_name.group(1))