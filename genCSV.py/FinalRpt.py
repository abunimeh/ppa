class FinalRptData:
    @staticmethod
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class FinalRpt:
    @staticmethod
    def metric_naming(file):
        import re
        stage = ""
        denall = re.search(r'.*denall.*', file, re.I)
        ipall = re.search(r'.*drcd.*', file, re.I)
        drcd = re.search(r'.*ipall.*', file, re.I)
        trclvs = re.search(r'.*trclvs.*', file, re.I)
        if denall:
            stage = 'drc denall reuse'
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
    def searchfile(file):
        import re
        from operator import itemgetter
        DataItems = []
        stage = FinalRpt.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()

        rptData = FinalRptData()

        for line in lines:
            foundNumOfActuEr = re.search(r'(The[\s]*number[\s]*of[\s]*actual[\s]*errors)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if foundNumOfActuEr:
                rptData.foundNumOfActuEr = FinalRpt.replaceSpace(stage), foundNumOfActuEr.group(2)
                DataItems.append(rptData.foundNumOfActuEr)
        data_items = sorted(DataItems, key=itemgetter(0))
        # return ["%s" % i[0] for i in data_items], ["%s" % i[1] for i in data_items]
        return data_items