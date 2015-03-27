# MAIN
# STATUS -- MISSING TOTAL RUNSET ERROR (OF ALL LAYOUT ERROR RUNS OF THE TESTCASE) COUNT METRIC
from Configurations import Configurations
base_path = Configurations().parser_final()

from QorRpt import QorRpt
from FinalRpt import FinalRpt
from PVTmetric import PVTMetric
from PhysicalRpt import PhysicalRpt
from RunTimeRpt import RunTimeRpt
from clockTree import clockTreeRpt
from Layout_Error import LayoutError
from dpLog import dpLog
from PvPower import PvPower

import csv

metricNames = []
qrpt = QorRpt.searchfile()
ppower = PvPower.searchfile()
pvtmetrics = PVTMetric.searchfile()
finalrpt = FinalRpt.searchfile()
physicalrpt = PhysicalRpt.searchfile()
runtimerpt = RunTimeRpt.searchfile()
clocktreerpt = clockTreeRpt.searchfile()
dplog = dpLog.searchfile()
layouter = LayoutError.searchfile()

metricNames.append(qrpt)
metricNames.append(ppower)
metricNames.append(pvtmetrics)
metricNames.append(finalrpt)
metricNames.append(physicalrpt)
metricNames.append(runtimerpt)
metricNames.append(clocktreerpt)
metricNames.append(dplog)
metricNames.append(layouter)

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

