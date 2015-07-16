__author__ = ''


class ToolMetric(object):
    def __init__(self, list_of_files, test_case, tool):
        self.list_of_files = list_of_files
        self.test_case = test_case
        self.tool = tool
        self.metrics = []

    def get_cadence_metrics(self):
        from Metrics.OrganizeMetric import OrganizeMetric
        from FileParsers.Cadence.QorReportCad import CaQorReport
        from FileParsers.Cadence.RunTime import CaRunTime
        from FileParsers.Cadence.StaMaxQor import StaMaxQor
        from FileParsers.Cadence.StaMinQor import StaMinQor
        from FileParsers.Cadence.CalibreErrors import CalibreErrors
        from FileParsers.Cadence.AprRunLog import AprRunLog
        from FileParsers.DynamicParser import DynamicParser
        # from FileParsers.Cadence.SignOffSum import CadenceSignOffSum
        from FileParsers.Cadence.GateCount import CadenceGateCount
        # fromFileParsers.Cadence.PowerReport import CadencePowerRpt
        # from FileParsers.Cadence.Violations import CadenceViolations

        for file in self.list_of_files:
            print("### Parsing:", file)
            if file.endswith('.qor.rpt'):
                if 'reports_max' in file:
                    sta_max_qor = StaMaxQor.search_file(file)
                    self.metrics.extend(sta_max_qor)
                elif 'reports_min' in file:
                    sta_min_qor = StaMinQor(file)
                    sta_min_qor.search_file()
                    self.metrics.extend(sta_min_qor.metrics)
                elif '.final.qor.rpt' in file:
                    cadence_qor = CaQorReport.search_file(file)
                    self.metrics.extend(cadence_qor)
            elif file.endswith('sta.max.log'):
                cadence_runtime = CaRunTime.search_file(file)
                self.metrics.extend(cadence_runtime)
            elif file.endswith('drc.sum'):
                calibre_errors = CalibreErrors.search_file(file)
                self.metrics.extend(calibre_errors)
            elif file.endswith("lvs.report"):
                calibre_fail_errors = CalibreErrors.search_file(file)
                self.metrics.extend(calibre_fail_errors)
            elif file.endswith('apr_run.log'):
                apr_run_log = AprRunLog.search_file(file)
                self.metrics.extend(apr_run_log)
            elif file.endswith('block_stats_signoff.rpt'):
                gate_count = CadenceGateCount.search_file(file)
                # my_list.append(gate_count)
                self.metrics.extend(gate_count)
            else:
                dynamic_parser = DynamicParser(file, self.tool)
                self.metrics.extend(dynamic_parser.search_file())

            # elif file.endswith('post_route_hold_optDesign.summary'):
            #     route_design = CadenceSignOffSum.search_file(file)
            #     metric_collections.append(route_design)
            # elif file.endswith('signoff.power.rpt'):
            #     pwr_rpt_data = CadencePowerRpt.search_file(file)
            #     metric_collections.append(pwr_rpt_data)
            # elif file.endswith('.final.all_violators.rpt'):
            #     cadence_violations = CadenceViolations.search_file(file)
            #     metric_collections.append(cadence_violations)
        print(" ")
        organizer = OrganizeMetric(self.metrics, self.test_case, self.tool)
        temp_metric_collections = organizer.add_missing_metrics_old()

        return temp_metric_collections

    def get_synopsys_metrics(self):
        import FileParsers.Synopsys.TotalDrcErrors as DrcErrors
        from Metrics.OrganizeMetric import OrganizeMetric
        from FileParsers.Synopsys.PVTmetric import PVTMetric
        from FileParsers.Synopsys.DrcErrors import DRCError
        from FileParsers.Synopsys.DpLog import DpLog
        from FileParsers.DynamicParser import DynamicParser
        from FileParsers.Synopsys.FinalReport import FinalReport
        from FileParsers.Synopsys.PhysicalReport import PhysicalReport
        from FileParsers.Synopsys.ClockTree import ClockTreeReport
        # from FileParsers.Synopsys.RunTimeRpt import RunTimeRpt
        # from FileParsers.Synopsys.QorReport import QorReport
        # from FileParsers.Synopsys.PvPower import PvPower

        # metrics contains the multiple list that are returned from the methods in the loop below
        # Loop through the list of files given from main
        my_list =[]
        for file in self.list_of_files:
            print("### Parsing:", file)
            # added_to_metrics = False
            # my_dict = {'dc.log': PVTMetric.search_file(file), 'icc.log': PVTMetric.search_file(file),
            #            'link.rpt': PVTMetric.search_file(file), '.dp.log': DpLog.search_file(file),
            #            'LAYOUT_ERRORS': DRCError.search_file(file, metric_collections),
            #            'Final_Report.txt': FinalReport.search_file(file), 'fill.physical.rpt': PhysicalReport.search_file(file),
            #            '.cts.clock_tree.rpt':ClockTreeReport.search_file(file)}
            # for file_endings in my_dict:
            #
            #     if file.endswith(file_endings):
            #         # metrics = my_dict[file_endings]
            #         metric_collections.extend(my_dict[file_endings])
            #         added_to_metrics = True
            #         break
            #
            # if not added_to_metrics:
            #     metric_collections.extend(DynamicParser.search_file(file, tool))
            if file.endswith('dc.log'):
                # pvt_metrics = PVTMetric.search_file(file)
                my_list.append(PVTMetric(file))
                # self.metrics.extend(pvt_metrics)
            elif file.endswith('icc.log'):
                # pvt_metrics = PVTMetric.search_file(file)
                my_list.append(PVTMetric(file))
                # self.metrics.extend(pvt_metrics)
            elif file.endswith('link.rpt'):
                # pvt_metrics = PVTMetric.search_file(file)
                my_list.append(PVTMetric(file))
                # self.metrics.extend(pvt_metrics)
            elif file.endswith('.dp.log'):
                my_list.append(DpLog(file))
                # dp_log = DpLog.search_file(file)
                # self.metrics.extend(dp_log)
            elif file.endswith('LAYOUT_ERRORS'):
                my_list.append(DRCError(file, self.metrics))
                # layout_er = DRCError.search_file(file, self.metrics)
                # self.metrics.extend(layout_er)
            elif file.endswith('Final_Report.txt'):
                my_list.append(FinalReport(file))
                # final_rpt = FinalReport.search_file(file)
                # self.metrics.extend(final_rpt)
            elif file.endswith('fill.physical.rpt'):
                my_list.append(PhysicalReport(file))
                # physical_rpt = PhysicalReport.search_file(file)
                # self.metrics.extend(physical_rpt)
            elif file.endswith(".cts.clock_tree.rpt"):
                my_list.append(ClockTreeReport(file))
                # clock_tree_data = ClockTreeReport.search_file(file)
                # self.metrics.extend(clock_tree_data)
            else:
                # dynamic_parser = DynamicParser(file, self.tool)
                my_list.append(DynamicParser(file, self.tool))
                # self.metrics.extend(dynamic_parser.search_file())
            # my_list = [dynamic_parser]
        i = 0
        for o in my_list:
            o.search_file()
            # print(o.file)
            self.metrics.extend(o.metrics)
            # print("METRICS", o.metrics)
        print("MYY COUNT", i)
            # uncomment the code below if we want to search for temp_metric_collection with hard coded classes
            # elif file.endswith('run_time.rpt'):
            #     my_list.append(RunTimeRpt(file))
            # if file.endswith('.qor.rpt'):
            #     my_list.append(RunTimeRpt(file)))
            # elif file.endswith('power.power.rpt'):
            #     ppower = PvPower.search_file(file)
            #     metric_collections.extend(ppower)

        print(" ")
        # Now that we have the list of metrics from all the files we can do use the TotalDrcErrors class to get the
        # total number of drc errors
        total_drc_errors = DrcErrors.get_total_count(self.metrics)
        self.metrics.extend([("drc_total_viols", total_drc_errors)])
        organizer = OrganizeMetric(self.metrics, self.test_case, self.tool)
        temp_metric_collections = organizer.add_missing_metrics_old()

        return temp_metric_collections
