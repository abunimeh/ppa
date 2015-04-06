class LayoutErrorData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)

class LayoutError:

    def replaceSpace(metricname):
        import re
        
        newName = re.sub(r'[\W]+', "_", metricname)
        return newName

    def searchfile(file):
        import re
        from Configurations import Configurations
        from operator import itemgetter
        base_path = Configurations().parser_final()
        # Open the file with read only permit
        
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        errorData = LayoutErrorData()
        violationCount = 0
        DataItems = []

        for line in lines:
            foundToolVersion = re.search(r'(Generated[\s]*by):.*[\s]+([\S]*[\.]+[\S]*[\.]*[\S]*[\.]*[\S]*[\.]*[\S]*)[\s]*', line, re.I)
            foundViolation = re.search(r'[\s]*([\d]+)[\s]*(violation+[s]*[\s]*found)+[\s]*', line, re.I)

            if foundToolVersion:
                errorData.foundToolVersion = LayoutError.replaceSpace(foundToolVersion.group(1)), foundToolVersion.group(2)
                DataItems.append(errorData.foundToolVersion)
            if foundViolation:
                tempfound = foundViolation.group(2)
                violationCount += int(foundViolation.group(1))
                
        if violationCount > 0:
            errorData.foundViolation = (tempfound, violationCount)
            DataItems.append(errorData.foundViolation)

        data_items = sorted(DataItems, key=itemgetter(0))
        return ["%s" % i[0] for i in data_items], ["%s" % i[1] for i in data_items]
