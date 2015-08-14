from FileParsers.Parser import Parser


class CadenceRunTime(Parser):
    def __init__(self, file):
        super(CadenceRunTime, self).__init__(file)

    @staticmethod
    def match_line(line, *args):
        import re
        match_words = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
        line_variables = '.*(%s)[\D]*([-\d\:]*).*' % match_words
        result = re.search(line_variables, line, re.I)
        return result

    def search_file(self):
        import sys

        run_time_name = self.replace_space('sta Run TIME') + " (secs)"

        for line in open(self.file):
            try:
                found_run_time = CadenceRunTime.match_line(line, 'Ending "Tempus Timing Signoff Solution"')

                if self.add_to_metrics(found_run_time, run_time_name):
                    break

            except:
                e = sys.exc_info()[0]



