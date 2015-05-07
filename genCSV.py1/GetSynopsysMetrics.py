__author__ = ''


class GetSynopsysMetrics:
    @staticmethod
    def get_synopsys_metrics(list_of_files, test_case, tool):
        import os
        from datetime import datetime
        from operator import itemgetter
        from PVTmetric import PVTMetric
        from Drc_Errors import DRCError
        from DpLog import DpLog
        from TotalDrcErrors import TotalDrcErrors
        from OtherMetricClass import OtherMetricClass
        from FinalRpt import FinalRpt
        from PhysicalRpt import PhysicalRpt
        from clockTree import clockTreeRpt
        # from RunTimeRpt import RunTimeRpt
        # from QorRpt import QorRpt
        # from PvPower import PvPower
        metric_collections = []
        for file in list_of_files:
            print("### Parsing:", file)
            if file.endswith('dc.log'):
                pvt_metrics = PVTMetric.searchfile(file)
                metric_collections.append(pvt_metrics)
            elif file.endswith('icc.log'):
                pvt_metrics = PVTMetric.searchfile(file)
                metric_collections.append(pvt_metrics)
            elif file.endswith('link.rpt'):
                pvt_metrics = PVTMetric.searchfile(file)
                metric_collections.append(pvt_metrics)
            elif file.endswith('.dp.log'):
                dp_log = DpLog.searchfile(file)
                metric_collections.append(dp_log)
            elif file.endswith('LAYOUT_ERRORS'):
                layout_er = DRCError.searchfile(file, metric_collections)
                metric_collections.append(layout_er)
            elif file.endswith('Final_Report.txt'):
                final_rpt_collections = FinalRpt.searchfile(file)
                metric_collections.append(final_rpt_collections)
            elif file.endswith('fill.physical.rpt'):
                physicalrpt = PhysicalRpt.searchfile(file)
                metric_collections.append(physicalrpt)
            elif file.endswith(".cts.clock_tree.rpt"):
                clock_tree_data = clockTreeRpt.searchfile(file)
                metric_collections.append(clock_tree_data)
            else:
                metric_collections.append(OtherMetricClass.searchfile(file, tool))
            # uncomment the code below if we want to search for metrics with hard coded classes
            # elif file.endswith('run_time.rpt'):
            #     runtimerpt = RunTimeRpt.searchfile(file)
            #     metric_collections.append(runtimerpt)
            # if file.endswith('.qor.rpt'):
            #     qrpt = QorRpt.searchfile(file)
            #     metric_collections.append(qrpt)
            # elif file.endswith('power.power.rpt'):
            #     ppower = PvPower.searchfile(file)
            #     metric_collections.append(ppower)

        total_drc_errors = TotalDrcErrors.get_total_count(metric_collections)
        metric_collections.append([("drc_total_viols", total_drc_errors)])
        metric_collections.append(GetSynopsysMetrics.check_metrics(metric_collections, tool))

        temp_metric_collections, syn, apr, drc, pv_max, pv_min, pv_power, pv_noise = [], [], [], [], [], [], [], []
        metric_pairs = [GetSynopsysMetrics.MetricPair("syn", syn), GetSynopsysMetrics.MetricPair("apr", apr),
                        GetSynopsysMetrics.MetricPair("drc", drc),  GetSynopsysMetrics.MetricPair("pv_max", pv_max),
                        GetSynopsysMetrics.MetricPair("pv_min", pv_min),
                        GetSynopsysMetrics.MetricPair("pv_power", pv_power),
                        GetSynopsysMetrics.MetricPair("pv_noise", pv_noise),
                        ]
        for metric_pair in metric_pairs:
            metric_pair = str(metric_pair)
            print(metric_pair)

        # # This loop is to arrange the files in the correct order
        i = 0
        for metric_collection in metric_collections:
            metric_names = list(metric_collection)
            for metric_name in range(len(metric_names)):
                for metric_pair in metric_pairs:
                    print(metric_pair)
                    i += 1
                #     if(GetSynopsysMetrics.organize_metrics(metric_pair.metric_name, metric_names[metric_name][0],
                #                                            metric_names, metric_pair.state_list)):
                #         break
                #
                # if GetSynopsysMetrics.organize_metrics("syn", metric_names[metric_name][0],  metric_names, syn):
                #     continue

                if "syn" in metric_names[metric_name][0]:
                    syn.append(metric_names[metric_name])
                    continue
                elif "apr" in metric_names[metric_name][0]:
                    apr.append(metric_names[metric_name])
                    continue
                elif "drc" in metric_names[metric_name][0]:
                    drc.append(metric_names[metric_name])
                    continue
                elif "pv_max" in metric_names[metric_name][0]:
                    pv_max.append(metric_names[metric_name])
                    continue
                elif "pv_min" in metric_names[metric_name][0]:
                    pv_min.append((metric_names[metric_name]))
                    continue
                elif "pv_power" in metric_names[metric_name][0]:
                    pv_power.append((metric_names[metric_name]))
                    continue
                elif "pv_noise" in metric_names[metric_name][0]:
                    pv_noise.append((metric_names[metric_name]))
                    continue

        print(i)
        if os.path.basename(test_case) != "":
            test_case_name = os.path.basename(test_case)
            kit_name = os.path.basename(os.path.dirname(test_case))
        else:
            test_case_name = os.path.basename(os.path.dirname(test_case))
            kit_name = os.path.basename(os.path.dirname(os.path.dirname(test_case)))
        default_metrics_collection = [("Testcase_Name", test_case_name), ("kit", kit_name),
                                      ("DateTime", str(datetime.now())), ("Tool", tool)]
        temp_metric_collections = [default_metrics_collection,  tuple(sorted(syn, key=itemgetter(0))),
                tuple(sorted(apr, key=itemgetter(0))), tuple(sorted(drc, key=itemgetter(0))),
                tuple(sorted(pv_max, key=itemgetter(0))), tuple(sorted(pv_min, key=itemgetter(0))),
                tuple(sorted(pv_power, key=itemgetter(0))), tuple(sorted(pv_noise, key=itemgetter(0)))]

        return temp_metric_collections

    @staticmethod
    def check_metrics(metricNames, tool):
        import json
        metric_names = []
        return_list = []
        with open(r'C:\dev\intel\ppa\genCSV.py\config.json', 'r') as f:
            json_data = json.load(f)
            # gets the line_keywords from the JSON file
            default_metrics = json_data['default_list_of_metrics'][tool]
        for metrics in metricNames:
            for name in range(len(metrics)):
                metric_names.append(metrics[name][0])
        for def_names in default_metrics:
            if def_names not in metric_names:
                default_value = def_names, "\t"
                return_list.append(default_value)

        return return_list

    @staticmethod
    def organize_metrics(match_metric_name, metric_name, metric_names, stage_list):
        result = False

        if match_metric_name in metric_names[metric_name][0]:
            stage_list.append(metric_names[metric_name])
            result = True

        return result

    class MetricPair:
        def __init__(self, metric_name, state_list):
            self.metric_name = metric_name
            self.state_list = state_list