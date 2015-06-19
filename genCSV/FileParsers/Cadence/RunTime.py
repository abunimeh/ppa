__author__ = ''


class CadenceRunTimeData:
    pass


class CaRunTime:
    @staticmethod
    def match_line(line, *args):
        import re
        match_words = ""
        no_match = ""
        for arg in args:
            match_words += arg.replace(" ", "[\s]*") + "[\s]*"
        line_variables = '.*(%s)[\D]*([-\d\:]*).*' % match_words
        result = re.search(line_variables, line, re.I)
        return result

    @staticmethod
    def replace_space(metric_list):
        import re
        new_name = re.sub(r'[\W]+', "_", metric_list)
        return new_name

    @staticmethod
    def search_file(file):
        import sys
        import Metrics.FormatMetric as Format
        # Open the file with read only permit
        #open(file, "r")as lines:
        # The variable "lines" is a list containing all lines
        #lines = f.readlines()
        # close the file after reading the lines.
        #f.close()
        data_items = []
        run_time_data = CadenceRunTimeData()
        run_time_data.found_run_time = [Format.replace_space('sta Run Time') + " (secs)", "N/A"]

        #f = open(file, 'r')
        #line = f.readline()
        i = 0
        for line in open(file):   
        #while line:
            try:
                found_run_time = CaRunTime.match_line(line, 'Ending "Tempus Timing Signoff Solution"')

                if found_run_time:
                    run_time_data.found_run_time[1] = Format.convert_to_seconds_format(found_run_time.group(2))
                # if i % 300 == 0:
                #     print("mult of 300")
                # i += 1
                # # print(i)
                #line = f.readline()
            except:
                e = sys.exc_info()[0]
                # print(e)
                #write_to_page("<p>Error:%s</p>" % e)
        #f.close()
        # print("left loop")
        data_items.append(tuple(run_time_data.found_run_time))

        return data_items
