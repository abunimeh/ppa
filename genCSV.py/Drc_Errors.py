class DRCErrorData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class DRCError:
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

    def replaceSpace(metricname):
        import re
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName
    def searchfile(file):
#         import os
# os.path.join(os.path.dirname(__file__), os.pardir)
#     def searchErrLayout(file):
        import re
        from Configurations import Configurations
        base_path = Configurations().parser_final()
        stage = DRCError.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        errorData = DRCErrorData()
        violationCount = 0
        DataItems = []

        for line in lines:
            foundToolVersion = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
            foundViolation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)

            if foundToolVersion:
                errorData.foundToolVersion = DRCError.replaceSpace("drc tool version"), foundToolVersion.group(2)
                DataItems.append(errorData.foundToolVersion)
            if foundViolation:
                violationCount += int(foundViolation.group(1))
                
        if violationCount > 0:
            errorData.foundViolation = DRCError.replaceSpace(stage), violationCount
            DataItems.append(errorData.foundViolation)
        else:
            errorData.foundViolation = DRCError.replaceSpace(stage), "PASS"
            DataItems.append(errorData.foundViolation)
        return ["%s" % i[0] for i in DataItems], ["%s" % i[1] for i in DataItems]

    # def searchFinalrpt(file):
    #     import re
    #     from Configurations import Configurations
    #     DataItems = []
    #     base_path = Configurations().parser_final()
    #     # Open the file with read only permit
    #     f = open(file, "r")
    #     # The variable "lines" is a list containing all lines
    #     lines = f.readlines()
    #     f.close()
    #
    #     rptData = FinalRptData()
    #
    #     for line in lines:
    #         foundNumOfActuEr = re.search(r'(The[\s]*number[\s]*of[\s]*actual[\s]*errors)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)
    #
    #         if foundNumOfActuEr:
    #             rptData.foundNumOfActuEr = (re.sub(r'[\W]+', "_", foundNumOfActuEr.group(1)), foundNumOfActuEr.group(2))
    #             DataItems.append(rptData.foundNumOfActuEr)
    #
    #     return ["%s" % i[0] for i in DataItems], ["%s" % i[1] for i in DataItems]
