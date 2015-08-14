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
        pv = "pv power tttt"

        for line in self.get_file_lines():
            found_internal_power = self.match_line("Cell", "Internal", "Power", line)
            found_leakage_power = self.match_line("Cell", "Leakage", "Power", line)
            found_switching_power = self.match_line("Net", "switching", "Power", line)
            found_total_power = self.match_line("Total", "Power", " ", line)

            if self.add_to_metrics(found_internal_power, self.replace_space(pv + " internal")):
                pass
            elif self.add_to_metrics(found_leakage_power, self.replace_space(pv + " leakage")):
                pass
            elif self.add_to_metrics(found_switching_power, self.replace_space(pv + " switch")):
                pass
            elif self.add_to_metrics(found_total_power, self.replace_space(pv + " total")):
                pass






