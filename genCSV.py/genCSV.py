# MAIN
# STATUS -- MISSING TOTAL RUNSET ERROR (OF ALL LAYOUT ERROR RUNS OF THE TESTCASE) COUNT METRIC
import csv
from Configurations import Configurations
from findFiles import findFiles
from QorRpt import QorRpt
from FinalRpt import FinalRpt
from PVTmetric import PVTMetric
from PhysicalRpt import PhysicalRpt
from RunTimeRpt import RunTimeRpt
from clockTree import clockTreeRpt
from Drc_Errors import DRCError
from dpLog import dpLog
from PvPower import PvPower
testcases = ["cpu_testcase", "fdkex_SCAN"]
base_path = Configurations().parser_final()
csv_file_exist = 0
for test_case in testcases:
    metricNames = []
    metricNames.append([['Testcase'], [test_case]])
    list_of_files = findFiles.searchDir(test_case)

    for file in list_of_files:
        if file.endswith('.qor.rpt'):
            qrpt = QorRpt.searchfile(file)
            metricNames.append(qrpt)
        if file.endswith('power.power.rpt'):
            ppower = PvPower.searchfile(file)
            metricNames.append(ppower)
        if file.endswith('dc.log'):
            pvtmetrics = PVTMetric.searchfile(file)
            metricNames.append(pvtmetrics)
        if file.endswith('icc.log'):
            pvtmetrics = PVTMetric.searchfile(file)
            metricNames.append(pvtmetrics)
        if file.endswith('link.rpt'):
            pvtmetrics = PVTMetric.searchfile(file)
            metricNames.append(pvtmetrics)
        if file.endswith('fill.physical.rpt'):
            physicalrpt = PhysicalRpt.searchfile(file)
            metricNames.append(physicalrpt)
        if file.endswith('run_time.rpt'):
            runtimerpt = RunTimeRpt.searchfile(file)
            metricNames.append(runtimerpt)
        if file.endswith('cts.clock_tree.rpt'):
            clocktreerpt = clockTreeRpt.searchfile(file)
            metricNames.append(clocktreerpt)
        if file.endswith('.dp.log'):
            dplog = dpLog.searchfile(file)
            metricNames.append(dplog)
        if file.endswith('Final_Report.txt'):
            finalrpt = FinalRpt.searchfile(file)
            metricNames.append(finalrpt)
        if file.endswith('LAYOUT_ERRORS'):
            layouter = DRCError.searchfile(file)
            metricNames.append(layouter)

    names = []
    values = []
    # temp =[]
    #
    # syn = []
    # apr = []
    # drc = []
    # pv_max = []
    # pv_min = []
    # pv_power = []
    # pv_noise = []
    # import re
    # for metric in metricNames:
    #     try:
    #         if metric[0][0]:
    #             print("metric[0][0]", metric[0][0])
    #
    #             print("metric[0]", metric[0], metric[1])
    #             sy = re.search('.*syn.*', metric[0][0], re.I)
    #             if sy:
    #                 print(metric[0], metric[1])
    #                 syn.append([[metric[0]], [metric[1]]])
    #             if "apr" in metric[0][0]:
    #                 apr.append((metric[0], metric[1]))
    #             if "drc" in metric[0][0]:
    #                 drc.append((metric[0], metric[1]))
    #             if "pv_max" in metric[0][0]:
    #                 pv_max.append((metric[0], metric[1]))
    #             if "pv_min" in metric[0][0]:
    #                 pv_min.append((metric[0], metric[1]))
    #             if "pv_power" in metric[0][0]:
    #                 pv_power.append((metric[0], metric[1]))
    #             if "pv_noise" in metric[0][0]:
    #                 pv_noise.append((metric[0], metric[1]))
    #     except IndexError:
    #         print("not found")
    #
    # print("Metrics Found:")
    # for syn in syn:
    #     print(syn[0], syn[1])
    # for apr in apr:
    #     print(apr[0], apr[1])
    # for drc in drc:
    #     print(drc[0], drc[1])
    # for pv_max in pv_max:
    #     print(pv_max[0], pv_max[1])
    # for pv_min in pv_min:
    #     print(pv_min[0], pv_min[1])
    # for pv_power in pv_power:
    #     print(pv_power[0], pv_power[1])
    # for pv_noise in pv_noise:
    #     print(pv_noise[0], pv_noise[1])
    #
    # #temp = [syn, apr , drc , pv_max , pv_min , pv_power , pv_noise]
    # temp.append(syn)
    # temp.append(apr)
    # temp.append(drc)
    # temp.append(pv_max)
    # temp.append(pv_min)
    # temp.append(pv_power)
    # temp.append(pv_noise)
    for items in metricNames:
        try:
            # Names and values are concatenated into a string in order to have horizontal column
            names += items[0]
            values += items[1]
        except IndexError:
            print("not found")
    print("Metrics found: \n", names, values)
    if csv_file_exist == 0:
        csv_file_exist = 1
        # Creates a csv with the first testcase
        with open(base_path + r'goodfile.csv', 'wt') as myfile:
            writer = csv.writer(myfile, lineterminator='\n')
            writer.writerow(names)
            writer.writerow(values)
            writer.writerow(' ')
        myfile.close()
        print('csv created (%sgoodfile.csv) with %s' % (base_path, test_case))

    else:
        # Appends the csv with the following testcases
        with open(base_path + r'goodfile.csv', 'a') as myfile:
            writer = csv.writer(myfile, lineterminator='\n')
            writer.writerow(names)
            writer.writerow(values)
            writer.writerow(' ')
        myfile.close()
        print('csv appended (%sgoodfile.csv) with %s' % (base_path, test_case))
