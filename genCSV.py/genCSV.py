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
from Layout_Error import LayoutError
from dpLog import dpLog
from PvPower import PvPower

base_path = Configurations().parser_final()
list_of_files = findFiles.searchDir()
metricNames = []
i = 0
for file in list_of_files:
    if file.endswith('.qor.rpt'):
        i += 1
        print(file)
        qrpt = QorRpt.searchfile(file)
        metricNames.append(qrpt)
    if file.endswith('power.power.rpt'):
        i += 1
        print(file)
        ppower = PvPower.searchfile(file)
        metricNames.append(ppower)
    if file.endswith('dc.log'):
        i += 1
        print(file)
        pvtmetrics = PVTMetric.searchfile(file)
        metricNames.append(pvtmetrics)
    if file.endswith('icc.log'):
        i += 1
        print(file)
        pvtmetrics = PVTMetric.searchfile(file)
        metricNames.append(pvtmetrics)
    if file.endswith('link.rpt'):
        i += 1
        print(file)
        pvtmetrics = PVTMetric.searchfile(file)
        metricNames.append(pvtmetrics)
    if file.endswith('fill.physical.rpt'):
        i += 1
        print(file)
        physicalrpt = PhysicalRpt.searchfile(file)
        metricNames.append(physicalrpt)
    if file.endswith('run_time.rpt'):
        i += 1
        print(file)
        runtimerpt = RunTimeRpt.searchfile(file)
        metricNames.append(runtimerpt)
    if file.endswith('cts.clock_tree.rpt'):
        i += 1
        print(file)
        clocktreerpt = clockTreeRpt.searchfile(file)
        metricNames.append(clocktreerpt)
    if file.endswith('.dp.log'):
        i += 1
        print(file)
        dplog = dpLog.searchfile(file)
        metricNames.append(dplog)
    if file.endswith('Final_Report.txt'):
            i += 1
            print(file)
            finalrpt = FinalRpt.searchfile(file)
            metricNames.append(layouter)
    if file.endswith('LAYOUT_ERRORS'):
            i += 1
            print(file)
            layouter = LayoutError.searchfile(file)
            metricNames.append(layouter)
print(i)
names = []
values = []
for met in metricNames:
    print(met[0])
for metric in metricNames:
    names += metric[0]
    values += metric[1]

with open(base_path + r'goodfile.csv', 'wt') as myfile:
    writer = csv.writer(myfile, lineterminator='\n')
    writer.writerow(names)
    writer.writerow(values)
myfile.close()
