# MAIN
# STATUS -- MISSING TOTAL RUNSET ERROR (OF ALL LAYOUT ERROR RUNS OF THE TESTCASE) COUNT METRIC
import csv
from operator import itemgetter
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
    list_of_files = findFiles.searchDir(test_case)
    found_tool_version = 0
    for file in list_of_files:
        if file.endswith('.qor.rpt'):
            qrpt = QorRpt.searchfile(file)
            metricNames.append(qrpt)
        elif file.endswith('power.power.rpt'):
            ppower = PvPower.searchfile(file)
            metricNames.append(ppower)
        elif file.endswith('dc.log'):
            pvtmetrics = PVTMetric.searchfile(file)
            metricNames.append(pvtmetrics)
        elif file.endswith('icc.log'):
            pvtmetrics = PVTMetric.searchfile(file)
            metricNames.append(pvtmetrics)
        elif file.endswith('link.rpt'):
            pvtmetrics = PVTMetric.searchfile(file)
            metricNames.append(pvtmetrics)
        elif file.endswith('fill.physical.rpt'):
            physicalrpt = PhysicalRpt.searchfile(file)
            metricNames.append(physicalrpt)
        elif file.endswith('run_time.rpt'):
            runtimerpt = RunTimeRpt.searchfile(file)
            metricNames.append(runtimerpt)
        elif file.endswith('cts.clock_tree.rpt'):
            clocktreerpt = clockTreeRpt.searchfile(file)
            metricNames.append(clocktreerpt)
        elif file.endswith('.dp.log'):
            dplog = dpLog.searchfile(file)
            metricNames.append(dplog)
        elif file.endswith('Final_Report.txt'):
            finalrpt = FinalRpt.searchfile(file)
            metricNames.append(finalrpt)
        elif file.endswith('LAYOUT_ERRORS'):
            if found_tool_version == 0:
                layout_er = DRCError.searchfile(file)
                for i in range(len(layout_er)):
                    if "drc_tool_version" in layout_er[i]:
                        found_tool_version = 1
                metricNames.append(layout_er)

    names, values, temp, syn, apr, drc, pv_max, pv_min, pv_power, pv_noise = [], [], [], [], [], [], [], [], [], []

    for metric in metricNames:
        met = tuple(metric)
        for name in range(len(met)):
                if "syn" in met[name][0]:
                    syn.append(met[name])
                    continue
                elif "apr" in met[name][0]:
                    apr.append(met[name])
                    continue
                elif "drc" in met[name][0]:
                    drc.append(met[name])
                    continue
                elif "pv_max" in met[name][0]:
                    pv_max.append(met[name])
                    continue
                elif "pv_min" in met[name][0]:
                    pv_min.append((met[name]))
                    continue
                elif "pv_power" in met[name][0]:
                    pv_power.append((met[name]))
                    continue
                elif "pv_noise" in met[name][0]:
                    pv_noise.append((met[name]))
                    continue

    test_case_metric = [("Testcase", test_case)]
    syn_list = tuple(sorted(syn, key=itemgetter(0)))
    apr_list = tuple(sorted(apr, key=itemgetter(0)))
    drc_list = tuple(sorted(drc, key=itemgetter(0)))
    pv_max_list = tuple(sorted(pv_max, key=itemgetter(0)))
    pv_min_list = tuple(sorted(pv_min, key=itemgetter(0)))
    pv_power_list = tuple(sorted(pv_power, key=itemgetter(0)))
    pv_noise_list = tuple(sorted(pv_noise, key=itemgetter(0)))

    temp = [test_case_metric, syn_list, apr_list, drc_list, pv_max_list, pv_min_list, pv_power_list, pv_noise_list]

    for metrics in temp:
        metric = tuple(metrics)
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
        print('%sgoodfile.csv created with %s' % (base_path, test_case))
    else:
        # Appends the csv with the following testcases
        with open(base_path + r'goodfile.csv', 'a') as myfile:
            writer = csv.writer(myfile, lineterminator='\n')
            writer.writerow(names)
            writer.writerow(values)
            writer.writerow(' ')
        myfile.close()
        print('%sgoodfile.csv appended with %s' % (base_path, test_case))
