__author__ = 'dcart_000'


class GetCadenceMetrics:
    @staticmethod
    def get_cadence_metrics(list_of_files, test_case):
        import os
        from datetime import datetime
        from operator import itemgetter
        from CadenceSignOffSum import CadenceSignOffSum
        from CadenceGateCount import CadenceGateCount
        from CadencePowerReport import CadencePowerRpt
        from CadenceAprRunLog import CadenceAprRunLog
        from CadenceQorReport import CadenceQorReport
        from CadenceViolations import CadenceViolations
        from CadenceRunTime import CadenceRunTime
        from CadenceStaMaxQor import CadenceStaMaxQor
        from CadenceStaMinQor import CadenceStaMinQor
        from CalibreErrors import CalibreErrors
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
            elif file.endswith('post_route_hold_optDesign.summary'):
                route_design = CadenceSignOffSum.searchfile(file)
                metric_names.append(route_design)
            elif file.endswith('signoff.power.rpt'):
                pwr_rpt_data = CadencePowerRpt.searchfile(file)
                metric_names.append(pwr_rpt_data)
            elif file.endswith('.final.all_violators.rpt'):
                cadence_violations = CadenceViolations.searchfile(file)
                metric_names.append(cadence_violations)
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
            elif file.endswith('block_stats_signoff.rpt'):
                gate_count = CadenceGateCount.searchfile(file)
                metric_names.append(gate_count)

        temp, syn, apr, sta, calibre = [], [], [], [], []

        # This loop is to arrange the files in the correct order
        for metric in metric_names:
            met = tuple(metric)
            for name in range(len(met)):
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

        tool_metric = [("Tool", "cadence")]
        test_case_metric = [("Testcase_Name", os.path.basename(test_case))]
        date_metric = [("DateTime", str(datetime.now()))]
        temp = [test_case_metric, date_metric, tool_metric, tuple(sorted(apr, key=itemgetter(0))),
                tuple(sorted(calibre, key=itemgetter(0))), tuple(sorted(sta, key=itemgetter(0))),
                tuple(sorted(syn, key=itemgetter(0)))]

        return temp