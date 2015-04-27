__author__ = ''


class GetSynopsysMetrics:
    @staticmethod
    def get_synopsys_metrics(list_of_files, test_case, tool):
        import os
        from datetime import datetime
        from operator import itemgetter
        from PVTmetric import PVTMetric
        from Drc_Errors import DRCError
        from dpLog import dpLog
        from TotalDrcErrors import TotalDrcErrors
        from OtherMetricClass import OtherMetricClass
        # from FinalRpt import FinalRpt
        # from PhysicalRpt import PhysicalRpt
        # from RunTimeRpt import RunTimeRpt
        # from QorRpt import QorRpt
        # from clockTree import clockTreeRpt
        # from PvPower import PvPower
        metricNames = []
        found_tool_version = 0
        for file in list_of_files:

            if file.endswith('dc.log'):
                pvtmetrics = PVTMetric.searchfile(file)
                metricNames.append(pvtmetrics)
            elif file.endswith('icc.log'):
                pvtmetrics = PVTMetric.searchfile(file)
                metricNames.append(pvtmetrics)
            elif file.endswith('link.rpt'):
                pvtmetrics = PVTMetric.searchfile(file)
                metricNames.append(pvtmetrics)
            elif file.endswith('.dp.log'):
                dplog = dpLog.searchfile(file)
                metricNames.append(dplog)

            elif file.endswith('LAYOUT_ERRORS'):
                if found_tool_version == 0:
                    layout_er = DRCError.searchfile(file)
                    for i in range(len(layout_er)):
                        if "drc_tool_version" in layout_er[i]:
                            found_tool_version = 1
                    metricNames.append(layout_er)
            else:
                metricNames.append(OtherMetricClass.searchfile(file, tool))
            # uncomment the code below if we want to search for metrics with hard coded classes
            # elif file.endswith('fill.physical.rpt'):
            #     physicalrpt = PhysicalRpt.searchfile(file)
            #     metricNames.append(physicalrpt)
            # elif file.endswith('Final_Report.txt'):
            #     finalrpt = FinalRpt.searchfile(file)
            #     metricNames.append(finalrpt)
            # elif file.endswith('run_time.rpt'):
            #     runtimerpt = RunTimeRpt.searchfile(file)
            #     metricNames.append(runtimerpt)
            # if file.endswith('.qor.rpt'):
            #     qrpt = QorRpt.searchfile(file)
            #     metricNames.append(qrpt)
            # elif file.endswith('power.power.rpt'):
            #     ppower = PvPower.searchfile(file)
            #     metricNames.append(ppower)

        total_drc_errors = TotalDrcErrors.get_total_count(metricNames)
        metricNames.append([("drc_total_viols", total_drc_errors)])


        temp, syn, apr, drc, pv_max, pv_min, pv_power, pv_noise = [], [], [], [], [], [], [], []

        # This loop is to arrange the files in the correct order
        i = 0
        for metric in metricNames:
            met = tuple(metric)
            i += 1
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
        print(i)
        tool_metric = [("Tool", "synopsys")]
        test_case_metric = [("Testcase_Name", os.path.basename(test_case))]
        date_metric = [("DateTime", str(datetime.now()))]

        temp = [test_case_metric, date_metric, tool_metric, tuple(sorted(syn, key=itemgetter(0))),
                tuple(sorted(apr, key=itemgetter(0))), tuple(sorted(drc, key=itemgetter(0))),
                tuple(sorted(pv_max, key=itemgetter(0))), tuple(sorted(pv_min, key=itemgetter(0))),
                tuple(sorted(pv_power, key=itemgetter(0))), tuple(sorted(pv_noise, key=itemgetter(0)))]

        return temp