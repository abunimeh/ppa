class PvPowerData:
    pass

from FileParsers.Parser import Parser


class PvPower(Parser):
    def __init__(self, file):
        super(PvPower, self).__init__(file)

    @staticmethod
    def match_line(regex1,regex2, regex3, line):
        import re
        regexR = r'(%s[\s]*%s[\s]*%s)[\s]*=+[\s]*([\d]+[\.]*[\d]*[\S]+)+[\s]*' %(regex1, regex2, regex3)
        result = re.search(regexR, line, re.I)
        return result

    def search_file(self):
        import Metrics.FormatMetric as Format

        pv = "pv power tttt"

        for line in self.get_file_lines():
            foundCInternPwr = PvPower.match_line("Cell", "Internal", "Power", line)
            foundCLeakPwr = PvPower.match_line("Cell", "Leakage", "Power", line)
            foundNetSwPwr = PvPower.match_line("Net", "switching", "Power", line)
            foundTotalPwr = PvPower.match_line("Total", "Power", " ", line)

            if foundCInternPwr:
                self.metrics.append((Format.replace_space(pv + " internal"), Format.format_metric_values(foundCInternPwr.group(2))))
            elif foundCLeakPwr:
                self.metrics.append((Format.replace_space(pv + " leakage"), Format.format_metric_values(foundCLeakPwr.group(2))))
            elif foundNetSwPwr:
                self.metrics.append((Format.replace_space(pv + " switch"), Format.format_metric_values(foundNetSwPwr.group(2))))
            elif foundTotalPwr:
                self.metrics.append((Format.replace_space(pv + " total"), Format.format_metric_values(foundTotalPwr.group(2))))






