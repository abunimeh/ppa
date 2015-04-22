__author__ = 'dcart_000'


class GetSynopsysMetrics:
    @staticmethod
    def get_synopsys_metrics(list_of_files, test_case):
        import os
        from datetime import datetime
        from operator import itemgetter
        from QorRpt import QorRpt
        from FinalRpt import FinalRpt
        from PVTmetric import PVTMetric
        from PhysicalRpt import PhysicalRpt
        from RunTimeRpt import RunTimeRpt
        from clockTree import clockTreeRpt
        from Drc_Errors import DRCError
        from dpLog import dpLog
        from PvPower import PvPower
        from TotalDrcErrors import TotalDrcErrors
        metricNames = []
        
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

        total_drc_errors = TotalDrcErrors.get_total_count(metricNames)
        if total_drc_errors:
            metricNames.append([("drc_total_viols", total_drc_errors)])

        temp, syn, apr, drc, pv_max, pv_min, pv_power, pv_noise = [], [], [], [], [], [], [], []

        # This loop is to arrange the files in the correct order
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

        tool_metric = [("Tool", "synopsys")]
        test_case_metric = [("Testcase_Name", os.path.basename(test_case))]
        date_metric = [("DateTime", str(datetime.now()))]

        temp = [test_case_metric, date_metric, tool_metric, tuple(sorted(syn, key=itemgetter(0))),
                tuple(sorted(apr, key=itemgetter(0))), tuple(sorted(drc, key=itemgetter(0))),
                tuple(sorted(pv_max, key=itemgetter(0))), tuple(sorted(pv_min, key=itemgetter(0))),
                tuple(sorted(pv_power, key=itemgetter(0))), tuple(sorted(pv_noise, key=itemgetter(0)))]

        return temp