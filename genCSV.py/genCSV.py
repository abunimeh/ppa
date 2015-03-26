# MAIN
# STATUS -- MISSING TOTAL RUNSET ERROR (OF ALL LAYOUT ERROR RUNS OF THE TESTCASE) COUNT METRIC

from QorRpt import QorRpt
from FinalRpt import FinalRpt
from PVTmetric import PVTMetric
from PhysicalRpt import PhysicalRpt
from RunTimeRpt import RunTimeRpt
from clockTree import clockTreeRpt
from Layout_Error import LayoutError
from dpLog import dpLog
from PvPower import PvPower

QorRpt.searchfile()
import csv
# metricNames = []
#
# metricNames.append(QorRpt.searchfile())
# metricNames.append(LayoutError.searchfile())
# metricNames.append(PVTMetric.searchfile())
# metricNames.append(PvPower.searchfile())
# metricNames.append(FinalRpt.searchfile())
# metricNames.append(PhysicalRpt.searchfile())
# metricNames.append(RunTimeRpt.searchfile())
# metricNames.append(clockTreeRpt.searchfile())
# metricNames.append(dpLog.searchfile())
# for met in metricNames:
#     print(met[1][0])
# names = ["%s" % i[][0] for i in metricNames]
# values = ["%s" % i[][1] for i in metricNames]
# with open(r'C:\Dev\Work\Toms Work\Intel\ppa\goodfile.csv', 'wt') as myfile:
#     writer = csv.writer(myfile, lineterminator='\n')
#     #for val in metricNames:
#     writer.writerow(names)
#     writer.writerow(values)
# myfile.close()

