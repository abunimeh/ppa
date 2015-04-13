class DRCErrorData:
    pass

class DRCError:
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
    def does_fin_rpt_exist(file):
        import os
        directory = os.path.dirname(file)
        files_in_directory = os.listdir(directory)
        if "Final_Report.txt" in files_in_directory:
            print("Using Final_Report.txt to get errors\n")
            return 1

    @staticmethod
    def searchfile(file):
        import re
        stage = DRCError.metric_naming(file)
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        errorData = DRCErrorData()
        violationCount = 0
        DataItems = []
        fin_rpt = DRCError.does_fin_rpt_exist(file)
        for line in lines:
            foundToolVersion = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
            if foundToolVersion:
                errorData.foundToolVersion = DRCError.replaceSpace("drc tool version"), foundToolVersion.group(2)
                DataItems.append(errorData.foundToolVersion)
            if fin_rpt != 1:
                foundViolation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)
                if foundViolation:
                    violationCount += int(foundViolation.group(1))

        if fin_rpt == 1:
            return DataItems
        if violationCount > 0:
            errorData.foundViolation = DRCError.replaceSpace(stage), violationCount
            DataItems.append(errorData.foundViolation)
        else:
            errorData.foundViolation = DRCError.replaceSpace(stage), "PASS"
            DataItems.append(errorData.foundViolation)

        return DataItems