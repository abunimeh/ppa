__author__ = ''


# class OtherMetricClass:
#     @staticmethod
#     def mathcLine(regex1, line):
#         import re
#         keyword = regex1.replace(" ", "")
#         line_variables = '.*(%s)[^%s\d]*([-\d\.]*).*' % (regex1, keyword)
#         print(line_variables)
#         result = re.search(line_variables, line, re.I)
#         return result
#
#     @staticmethod
#     def replaceSpace(metricname):
#         import re
#         new_name = re.sub(r'[\W]+', "_", metricname)
#         return new_name
#
#     @staticmethod
#     def searchfile(file):
#         # Open the file with read only permit
#         f = open(file, "r")
#         # The variable "lines" is a list containing all lines
#         lines = f.readlines()
#         data_items = []
#         # close the file after reading the lines.
#         f.close()
#         other_metric_class = OtherMetricClass()
#         for line in lines:

