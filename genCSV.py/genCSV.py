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
test_cases_list = ["cpu_testcase", "fdkex_SCAN"]
base_path = Configurations().parser_final()
csv_file_exist = 0
for test_case in test_cases_list:
    metricNames = []
    test_case_metric = [("Testcase", test_case)]
    metricNames.append(test_case_metric)
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

    names, values, temp, syn, apr, drc, pv_max, pv_min, pv_power, pv_noise = [], [], [], [], [], [], [], [], [], []

    for metric in metricNames:
        met = tuple(metric)
        for name in range(len(met)):
                print("metric[%s]" % name, met[name])
                if "syn" in met[name][0]:
                    print("metric", met[name], "added")
                    syn.append(met[name])
                    continue
                if "apr" in met[name][0]:
                    print("metric added:", met[name])
                    apr.append(met[name])
                    continue
                if "drc" in met[name][0]:
                    print("metric", met[name], "added")
                    drc.append(met[name])
                    continue
                if "pv_max" in met[name][0]:
                    print("metric", met[name], "added")
                    pv_max.append(met[name])
                    continue
                if "pv_min" in met[name][0]:
                    print("metric", met[name], "added")
                    pv_min.append((met[name]))
                    continue
                if "pv_power" in met[name][0]:
                    print("metric", met[name], "added")
                    pv_power.append((met[name]))
                    continue
                if "pv_noise" in met[name][0]:
                    print("metric", met[name], "added")
                    pv_noise.append((met[name]))
                    continue

    temp = [test_case_metric, syn, apr, drc, pv_max, pv_min, pv_power, pv_noise]
    print("temp:", temp)

    for metrics in temp:
        metric = tuple(metrics)
        print("The length of the 'item' is :", len(metric), "items: ", metric)
        for name in range(len(metric)):
                # Names and values are concatenated into a string in order to have horizontal column
                names += [metric[name][0]]
                values += [metric[name][1]]
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
