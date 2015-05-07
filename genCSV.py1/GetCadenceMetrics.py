__author__ = ''


class GetCadenceMetrics:
    @staticmethod
    def get_cadence_metrics(list_of_files, test_case, tool):
        import os
        from datetime import datetime
        from operator import itemgetter
        from CadenceQorReport import CadenceQorReport
        from CadenceRunTime import CadenceRunTime
        from CadenceStaMaxQor import CadenceStaMaxQor
        from CadenceStaMinQor import CadenceStaMinQor
        from CalibreErrors import CalibreErrors
        from CadenceAprRunLog import CadenceAprRunLog
        from OtherMetricClass import OtherMetricClass
        # from CadenceSignOffSum import CadenceSignOffSum
        # from CadenceGateCount import CadenceGateCount
        # from CadencePowerReport import CadencePowerRpt
        # from CadenceViolations import CadenceViolations
        metric_names = []

        for file in list_of_files:
            if file.endswith('.qor.rpt'):
                if 'reports_max' in file:
                    sta_max_qor = CadenceStaMaxQor.searchfile(file)
                    metric_names.append(sta_max_qor)
                elif 'reports_min' in file:
                    sta_min_qor = CadenceStaMinQor.searchfile(file)
                    metric_names.append(sta_min_qor)
                elif '.final.qor.rpt' in file:
                    cadence_qor = CadenceQorReport.searchfile(file)
                    metric_names.append(cadence_qor)
            elif file.endswith('sta.max.log'):
                cadence_runtime = CadenceRunTime.searchfile(file)
                metric_names.append(cadence_runtime)
            elif file.endswith('drc.sum'):
                calibre_errors = CalibreErrors.searchfile(file)
                metric_names.append(calibre_errors)
            elif file.endswith("lvs.report"):
                calibre_fail_errors = CalibreErrors.searchfile(file)
                metric_names.append(calibre_fail_errors)
            elif file.endswith('apr_run.log'):
                apr_run_log = CadenceAprRunLog.searchfile(file)
                metric_names.append(apr_run_log)
            else:
                metric_names.append(OtherMetricClass.searchfile(file, tool))

            # elif file.endswith('post_route_hold_optDesign.summary'):
            #     route_design = CadenceSignOffSum.searchfile(file)
            #     metric_names.append(route_design)
            # elif file.endswith('signoff.power.rpt'):
            #     pwr_rpt_data = CadencePowerRpt.searchfile(file)
            #     metric_names.append(pwr_rpt_data)
            # elif file.endswith('.final.all_violators.rpt'):
            #     cadence_violations = CadenceViolations.searchfile(file)
            #     metric_names.append(cadence_violations)
            # elif file.endswith('block_stats_signoff.rpt'):
            #     gate_count = CadenceGateCount.searchfile(file)
            #     metric_names.append(gate_count)


        temp_metric_collections, syn, apr, sta, calibre = [], [], [], [], []
        metric_names.append(GetCadenceMetrics.check_metrics(metric_names, tool))
        metric_names = filter(None, metric_names)
        # This loop is to arrange the files in the correct order
        i = 0
        for metric in metric_names:
            met = tuple(metric)
            for name in range(len(met)):
                i+=1
                if met[name][1] is None or met[name][1] is "":
                    met[name][1] = "\t"
                if "syn" in met[name][0]:
                    syn.append(met[name])
                    continue
                elif "apr" in met[name][0]:
                    apr.append(met[name])
                    continue
                elif "calibre" in met[name][0]:
                    calibre.append(met[name])
                elif "sta" in met[name][0]:
                    sta.append(met[name])
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
        temp_metric_collections = [default_metrics_collection,  tuple(sorted(apr, key=itemgetter(0))),
                tuple(sorted(calibre, key=itemgetter(0))), tuple(sorted(sta, key=itemgetter(0))),
                tuple(sorted(syn, key=itemgetter(0)))]

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