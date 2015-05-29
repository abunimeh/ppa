__author__ = ''


class SynopsysMetric:
    @staticmethod
    def get_synopsys_metrics(list_of_files, test_case, tool):
        import os
        from datetime import datetime
        from Metrics.OrganizeMetric import OrganizeMetric
        from FileParsers.Synopsys.PVTmetric import PVTMetric
        from FileParsers.Synopsys.DrcErrors import DRCError
        from FileParsers.Synopsys.DpLog import dpLog
        from FileParsers.Synopsys.TotalDrcErrors import TotalDrcErrors
        from FileParsers.DynamicParser import DynamicParser
        from FileParsers.Synopsys.FinalRpt import FinalRpt
        from FileParsers.Synopsys.PhysicalRpt import PhysicalRpt
        from FileParsers.Synopsys.ClockTree import clockTreeRpt
        # from FileParsers.Synopsys.RunTimeRpt import RunTimeRpt
        # from FileParsers.Synopsys.QorRpt import QorRpt
        # from FileParsers.Synopsys.PvPower import PvPower

        # metric_collections contains the multiple list that are returned from the methods in the loop below
        metric_collections = []
        # Loop through the list of files given from main
        for file in list_of_files:
            print("### Parsing:", file)
            if file.endswith('dc.log'):
                pvt_metrics = PVTMetric.search_file(file)
                metric_collections.extend(pvt_metrics)
            elif file.endswith('icc.log'):
                pvt_metrics = PVTMetric.search_file(file)
                metric_collections.extend(pvt_metrics)
            elif file.endswith('link.rpt'):
                pvt_metrics = PVTMetric.search_file(file)
                metric_collections.extend(pvt_metrics)
            elif file.endswith('.dp.log'):
                dp_log = dpLog.search_file(file)
                metric_collections.extend(dp_log)
            elif file.endswith('LAYOUT_ERRORS'):
                layout_er = DRCError.search_file(file, metric_collections)
                metric_collections.extend(layout_er)
            elif file.endswith('Final_Report.txt'):
                final_rpt = FinalRpt.search_file(file)
                metric_collections.extend(final_rpt)
            elif file.endswith('fill.physical.rpt'):
                physical_rpt = PhysicalRpt.search_file(file)
                metric_collections.extend(physical_rpt)
            elif file.endswith(".cts.clock_tree.rpt"):
                clock_tree_data = clockTreeRpt.search_file(file)
                metric_collections.extend(clock_tree_data)
            else:
                metric_collections.extend(DynamicParser.search_file(file, tool))

            # uncomment the code below if we want to search for temp_metric_collection with hard coded classes
            # elif file.endswith('run_time.rpt'):
            #     runtimerpt = RunTimeRpt.search_file(file)
            #     metric_collections.extend(runtimerpt)
            # if file.endswith('.qor.rpt'):
            #     qrpt = QorRpt.search_file(file)
            #     metric_collections.extend(qrpt)
            # elif file.endswith('power.power.rpt'):
            #     ppower = PvPower.search_file(file)
            #     metric_collections.extend(ppower)

        # Now that we have the list of metrics from all the files we can do use the TotalDrcErrors class to get the
        # total number of drc errors
        # if os.path.basename(test_case) != "":
        #     test_case_name = os.path.basename(test_case)
        # else:
        #     test_case_name = os.path.basename(os.path.dirname(test_case))
        #
        # metric_collections.extend([("Testcase_Name", test_case_name), ("DateTime", str(datetime.now())), ("Tool", tool)])
        total_drc_errors = TotalDrcErrors.get_total_count(metric_collections)
        metric_collections.extend([("drc_total_viols", total_drc_errors)])

        temp_metric_collections = OrganizeMetric.add_missing_metrics_old(metric_collections, test_case, tool)

        return temp_metric_collections
