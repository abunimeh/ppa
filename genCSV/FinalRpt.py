class FinalRptData:
    pass
class FinalRpt:
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        denall = re.search(r'.*denall.*', file, re.I)
        ipall = re.search(r'.*ipall.*', file, re.I)
        drcd = re.search(r'.*drcd.*', file, re.I)
        trclvs = re.search(r'.*trclvs.*', file, re.I)
        if denall:
            stage = 'drc denall'
        if ipall:
            stage = 'drc IPall'
        if drcd:
            stage = 'drc drcd'
        if trclvs:
            stage = 'drc trclvs'
        return stage

    @staticmethod
    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    @staticmethod
    def search_file(file):
        import re
        DataItems = []
        stage = FinalRpt.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        rptData = FinalRptData()
        rptData.found_num_of_errors = [FinalRpt.replaceSpace(stage) + " (NB)", "N/A"]
        print("FINRPT", file)
        for line in lines:
            found_num_of_errors = re.search(r'(The[\s]*number[\s]*of[\s]*actual[\s]*errors)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
            if found_num_of_errors:
                rptData.found_num_of_errors[1] = (found_num_of_errors.group(2))
                DataItems.append(tuple(rptData.found_num_of_errors))
                return DataItems

        DataItems.append(tuple(rptData.found_num_of_errors))

        return DataItems
