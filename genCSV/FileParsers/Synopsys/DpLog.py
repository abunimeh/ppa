from FileParsers.Parser import Parser


class DpLog(Parser):
    def __init__(self, file):
        super(DpLog, self).__init__(file)

    def metric_naming(self):
        import re
        stage = ""
        denall = re.search(r'.*denall_reuse.*', self.file, re.I)
        drcd = re.search(r'.*drcd.*', self.file, re.I)
        ipall = re.search(r'.*ipall.*', self.file, re.I)
        trclvs = re.search(r'.*trclvs.*', self.file, re.I)
        if denall:
            stage = 'drc denall reuse'
        if ipall:
            stage = 'drc IPall'
        if drcd:
            stage = 'drc drcd'
        if trclvs:
            stage = 'drc trclvs'
        return stage

    def search_file(self):
        import re

        stage = self.metric_naming()

        peak_memory_name = self.replace_space(stage + " Peak Memory") + " (MB)"
        runtime_name = self.replace_space(stage + " RunTIME")+" (secs)"
        # We read in the lines in reversed in order to find the last value in the file
        for line in reversed(self.get_file_lines()):
            if not self.check_list(peak_memory_name):
                found_peak_memory = re.search(r'.*:[\s]*(Peak)[\s]*=[\s]*([\d]+[\s]*)\(mb\)', line, re.I)
                self.add_to_metrics(found_peak_memory, peak_memory_name)
            elif not self.check_list(runtime_name):
                found_runtime = re.search(r'(Overall[\s]*engine[\s]*time)[\s]*=+[\s]*([\d]*:*[\d]*:*[\d]+)+', line, re.I)
                self.add_to_metrics(found_runtime, runtime_name)
            if len(self.metrics) == 2:
                break
