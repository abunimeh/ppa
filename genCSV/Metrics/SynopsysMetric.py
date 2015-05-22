__author__ = ''


class SynopsysMetric:
    @staticmethod
    def get_synopsys_metrics(list_of_files, test_case, tool):
        from Metrics.OrganizeMetric import OrganizeMetric
        from FileParsers.Synopsys.PVTmetric import PVTMetric
        from FileParsers.Synopsys.DrcErrors import DRCError
        from FileParsers.Synopsys.DpLog import dpLog
        from FileParsers.Synopsys.TotalDrcErrors import TotalDrcErrors
        from FileParsers.DynamicParser import DynamicParser
        from FileParsers.Synopsys.FinalRpt import FinalRpt
        from FileParsers.Synopsys.PhysicalRpt import PhysicalRpt
        from FileParsers.Synopsys.ClockTree import clockTreeRpt
        # from RunTimeRpt import RunTimeRpt
        # from QorRpt import QorRpt
        # from PvPower import PvPower

        # metric_collections contains the multiple list that are returned from the methods in the loop below
        metric_collections = []
        # Loop through the list of files given from main
        for file in list_of_files:
            print("### Parsing:", file)
            if file.endswith('dc.log'):
                pvt_metrics = PVTMetric.search_file(file)
                metric_collections.append(pvt_metrics)
            elif file.endswith('icc.log'):
                pvt_metrics = PVTMetric.search_file(file)
                metric_collections.append(pvt_metrics)
            elif file.endswith('link.rpt'):
                pvt_metrics = PVTMetric.search_file(file)
                metric_collections.append(pvt_metrics)
            elif file.endswith('.dp.log'):
                dp_log = dpLog.search_file(file)
                metric_collections.append(dp_log)
            elif file.endswith('LAYOUT_ERRORS'):
                layout_er = DRCError.search_file(file, metric_collections)
                metric_collections.append(layout_er)
            elif file.endswith('Final_Report.txt'):
                final_rpt = FinalRpt.search_file(file)
                metric_collections.append(final_rpt)
            elif file.endswith('fill.physical.rpt'):
                physical_rpt = PhysicalRpt.search_file(file)
                metric_collections.append(physical_rpt)
            elif file.endswith(".cts.clock_tree.rpt"):
                clock_tree_data = clockTreeRpt.search_file(file)
                metric_collections.append(clock_tree_data)
            else:
                metric_collections.append(DynamicParser.search_file(file, tool))

            # uncomment the code below if we want to search for temp_metric_collection with hard coded classes
            # elif file.endswith('run_time.rpt'):
            #     runtimerpt = RunTimeRpt.search_file(file)
            #     metric_collections.append(runtimerpt)
            # if file.endswith('.qor.rpt'):
            #     qrpt = QorRpt.search_file(file)
            #     metric_collections.append(qrpt)
            # elif file.endswith('power.power.rpt'):
            #     ppower = PvPower.search_file(file)
            #     metric_collections.append(ppower)

        # Now that we have the list of metrics from all the files we can do use the TotalDrcErrors class to get the
        # total number of drc errors
        total_drc_errors = TotalDrcErrors.get_total_count(metric_collections)
        metric_collections.append([("drc_total_viols", total_drc_errors)])
        temp_metric_collections = OrganizeMetric.add_missing_metrics(metric_collections, test_case, tool)

        return temp_metric_collections
