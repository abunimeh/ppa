__author__ = ''


class ToolMetric(object):
    def __init__(self, list_of_files, test_case, tool):
        self.list_of_files = list_of_files
        self.test_case = test_case
        self.tool = tool
        self.metrics = []
        self.parser_objects = []

    def gather_metrics(self):
        for parser_object in self.parser_objects:
            print("### Parsing:  %s \n" % parser_object.file)
            parser_object.search_file()
            self.metrics.extend(parser_object.metrics)
        print("\n")

    def organize_metrics(self):
        from Metrics.OrganizeMetric import OrganizeMetric
        organizer = OrganizeMetric(self.metrics, self.test_case, self.tool)
        temp_metric_collections = organizer.add_missing_metrics_old()

        return temp_metric_collections

    def get_cadence_metrics(self):
        from FileParsers.Cadence.QorReportCad import CadenceQorReport
        from FileParsers.Cadence.RunTime import CadenceRunTime
        from FileParsers.Cadence.StaMaxQor import StaMaxQor
        from FileParsers.Cadence.StaMinQor import StaMinQor
        from FileParsers.Cadence.CalibreErrors import CalibreErrors
        from FileParsers.Cadence.AprRunLog import AprRunLog
        from FileParsers.DynamicParser import DynamicParser
        # from FileParsers.Cadence.SignOffSum import CadenceSignOffSum
        from FileParsers.Cadence.GateCount import CadenceGateCount
        # fromFileParsers.Cadence.PowerReport import PowerReport
        # from FileParsers.Cadence.Violations import CadenceViolations

        for file in self.list_of_files:
            if file.endswith('.qor.rpt'):
                if 'reports_max' in file:
                    self.parser_objects.append(StaMaxQor(file))
                elif 'reports_min' in file:
                    self.parser_objects.append(StaMinQor(file))
                elif '.final.qor.rpt' in file:
                    self.parser_objects.append(CadenceQorReport(file))
            elif file.endswith('sta.max.log'):
                self.parser_objects.append(CadenceRunTime(file))
            elif file.endswith('drc.sum'):
                self.parser_objects.append(CalibreErrors(file))
            elif file.endswith("lvs.report"):
                self.parser_objects.append(CalibreErrors(file))
            elif file.endswith('apr_run.log'):
                self.parser_objects.append(AprRunLog(file))
            elif file.endswith('block_stats_signoff.rpt'):
                self.parser_objects.append(CadenceGateCount(file))
            else:
                self.parser_objects.append(DynamicParser(file, self.tool))

            # elif file.endswith('post_route_hold_optDesign.summary'):
            #     self.parser_objects.append(CadenceSignOffSum(file))
            # elif file.endswith('signoff.power.rpt'):
            #     self.parser_objects.append(PowerReport(file))
            # elif file.endswith('.final.all_violators.rpt'):
            #     self.parser_objects.append(CadenceViolations(file))
        self.gather_metrics()
        return self.organize_metrics()


    def get_synopsys_metrics(self):
        import FileParsers.Synopsys.TotalDrcErrors as DrcErrors
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

        # Loop through the list of files given from GenerateMetric
        for file in self.list_of_files:
            if file.endswith('dc.log'):
                self.parser_objects.append(PVTMetric(file))
            elif file.endswith('icc.log'):
                self.parser_objects.append(PVTMetric(file))
            elif file.endswith('link.rpt'):
                self.parser_objects.append(PVTMetric(file))
            elif file.endswith('.dp.log'):
                self.parser_objects.append(DpLog(file))
            elif file.endswith('LAYOUT_ERRORS'):
                self.parser_objects.append(DRCError(file, self.metrics))
            elif file.endswith('Final_Report.txt'):
                self.parser_objects.append(FinalReport(file))
            elif file.endswith('fill.physical.rpt'):
                self.parser_objects.append(PhysicalReport(file))
            elif file.endswith(".cts.clock_tree.rpt"):
                self.parser_objects.append(ClockTreeReport(file))
            else:
                self.parser_objects.append(DynamicParser(file, self.tool))

            # uncomment the code below if we want to search for temp_metric_collection with hard coded classes
            # elif file.endswith('run_time.rpt'):
            #     self.parser_objects.append(RunTimeRpt(file))
            # if file.endswith('.qor.rpt'):
            #     self.parser_objects.append(RunTimeRpt(file)))
            # elif file.endswith('power.power.rpt'):
            #     self.parser_objects.append(PvPower(file))

        self.gather_metrics()
        # Now that we have the list of metrics from all the files we can do use the TotalDrcErrors class to get the
        # total number of drc errors
        total_drc_errors = DrcErrors.get_total_count(self.metrics)
        self.metrics.append(("drc_total_viols", total_drc_errors))

        return self.organize_metrics()