__author__ = ''


class GetCadenceMetrics:
    @staticmethod
    def get_cadence_metrics(list_of_files, test_case, tool):
        from OrganizingAndFormatingMetrics.OrganizeMetrics import OrganizeFoundMetrics
        from FileParsers.Cadence.QorReportCad import CaQorReport
        from FileParsers.Cadence.RunTime import CaRunTime
        from FileParsers.Cadence.StaMaxQor import StaMaxQor
        from FileParsers.Cadence.StaMinQor import StaMinQor
        from FileParsers.Cadence.CalibreErrors import CalibreErrors
        from FileParsers.Cadence.AprRunLog import AprRunLog
        from FileParsers.OtherMetricClass import OtherMetricClass
        # from CadenceSignOffSum import CadenceSignOffSum
        from FileParsers.Cadence.GateCount import CadenceGateCount
        # from CadencePowerReport import CadencePowerRpt
        # from CadenceViolations import CadenceViolations
        metric_collections = []

        for file in list_of_files:
            if file.endswith('.qor.rpt'):
                if 'reports_max' in file:
                    sta_max_qor = StaMaxQor.search_file(file)
                    metric_collections.append(sta_max_qor)
                elif 'reports_min' in file:
                    sta_min_qor = StaMinQor.search_file(file)
                    metric_collections.append(sta_min_qor)
                elif '.final.qor.rpt' in file:
                    cadence_qor = CaQorReport.search_file(file)
                    metric_collections.append(cadence_qor)
            elif file.endswith('sta.max.log'):
                cadence_runtime = CaRunTime.search_file(file)
                metric_collections.append(cadence_runtime)
            elif file.endswith('drc.sum'):
                calibre_errors = CalibreErrors.search_file(file)
                metric_collections.append(calibre_errors)
            elif file.endswith("lvs.report"):
                calibre_fail_errors = CalibreErrors.search_file(file)
                metric_collections.append(calibre_fail_errors)
            elif file.endswith('apr_run.log'):
                apr_run_log = AprRunLog.search_file(file)
                metric_collections.append(apr_run_log)
            elif file.endswith('block_stats_signoff.rpt'):
                gate_count = CadenceGateCount.search_file(file)
                metric_collections.append(gate_count)
            else:
                metric_collections.append(OtherMetricClass.search_file(file, tool))
        #     import sys
        # print("ARGUMENTS", sys.argv)
            # elif file.endswith('post_route_hold_optDesign.summary'):
            #     route_design = CadenceSignOffSum.search_file(file)
            #     metric_collections.append(route_design)
            # elif file.endswith('signoff.power.rpt'):
            #     pwr_rpt_data = CadencePowerRpt.search_file(file)
            #     metric_collections.append(pwr_rpt_data)
            # elif file.endswith('.final.all_violators.rpt'):
            #     cadence_violations = CadenceViolations.search_file(file)
            #     metric_collections.append(cadence_violations)
            # elif file.endswith('block_stats_signoff.rpt'):
            #     gate_count = CadenceGateCount.search_file(file)
            #     metric_collections.append(gate_count)

        temp_metric_collections = OrganizeFoundMetrics.add_missing_metrics(metric_collections, test_case, tool)


        return temp_metric_collections
