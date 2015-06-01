__author__ = 'tjstickx'


class OrganizeMetric:
    @staticmethod
    def add_missing_metrics_old(metric_list, test_case, tool):
        import json
        from FindFile import FindFiles
        from Metrics.GenerateMetric import GenerateMetric

        config_file = FindFiles.return_config_name()
        metric_names = []
        new_metrics_collections = []
        metric_name = 0

        # Open the JSON file and get the default list of metrics
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # gets the line_keywords from the JSON file
            default_metric_names = json_data['default_list_of_metrics']
        # Add each metric name that was captured from parsing the files to the list metric_names

        for metric_pair in metric_list:
            # Because metric_pair is a list that might have different lengths we use range(len(metric_pair))
            # in the following for loop
            metric_names.append(metric_pair[metric_name])

        for default_metric_name in default_metric_names:
            if default_metric_name not in metric_names:
                # "" is the default value for blank metrics
                new_metric = (default_metric_name, "")
                new_metrics_collections.append(new_metric)

        metric_list.extend(new_metrics_collections)
        # metric_list = OrganizeMetric.format_metric_values(metric_list)
        temp_metric_collections = OrganizeMetric.sort_metrics(metric_list, test_case, tool)
        return temp_metric_collections

    @staticmethod
    def normalize_list(metrics_collections):
        longest_list_length = 0
        default_metrics_list = OrganizeMetric.create_default_metric_list(metrics_collections)
        metrics_collections = OrganizeMetric.add_missing_metrics(metrics_collections, default_metrics_list)
        formatted_metrics_list = OrganizeMetric.sort_metrics(metrics_collections)
        return formatted_metrics_list
        # default_metric_names = []
        # metric_name = 0
        # # This loop is for creating a default list metrics
        # for metric_collection in metrics_collections:
        #     metric_list = tuple(metric_collection)
        #     for metric_pair in range(len(metric_list)):
        #         if metric_pair[metric_name] not in default_metric_names:
        #             default_metric_names.append(metric_pair[metric_name])
        # # This loop creates a list of
        # for metric_collection in metrics_collections:
        #     metric_list = list(metric_collection)
        #     temp_metric_names = []
        #     for metric_pair in range(len(metric_list)):
        #         temp_metric_names.append(metric_pair[metric_name])
        #     for default_metric_name in default_metric_names:
        #         if default_metric_name not in temp_metric_names:
        #             new_metric = (default_metric_name, "\t")
        #             metric_list.append(new_metric)
    @staticmethod
    def create_default_metric_list(metrics_collections):
        default_metric_names = []
        metric_name = 0
        # This loop is for creating a default list metrics
        # print("Collect", metrics_collections)
        for metric_list in metrics_collections:
            # print("list", metric_list)
            for metric_pair in metric_list:
                # print(metric_pair)
                # print("met name", metric_pair[metric_name])
                if metric_pair[metric_name] not in default_metric_names:
                    default_metric_names.append(metric_pair[metric_name])
        print(default_metric_names)
        return default_metric_names

    @staticmethod
    def add_missing_metrics(metrics_collections, default_metric_names):
        metric_name = 0
        for metric_list in metrics_collections:
            temp_metric_names = []
            for metric_pair in metric_list:
                temp_metric_names.append(metric_pair[metric_name])
            for default_metric_name in default_metric_names:
                if default_metric_name not in temp_metric_names:
                    new_metric = (default_metric_name, "\t")
                    metric_list.append(new_metric)
        print(metrics_collections)
        return metrics_collections

    # This method is used to add the metrics that don't appear after parsing the required files
    @staticmethod
    def sort_metrics(metric_collections, test_case, tool):
        import os
        from datetime import datetime
        from operator import itemgetter
        temp_metric_collections, syn, apr, calibre, drc, pv_max, pv_min, pv_power, pv_noise, sta, kit = [], [], [], [], [], [], [], [], [], [], []
        # metric_pairs = [SynopsysMetric.MetricPair("syn", syn), SynopsysMetric.MetricPair("apr", apr),
        #                 SynopsysMetric.MetricPair("drc", drc),  SynopsysMetric.MetricPair("pv_max", pv_max),
        #                 SynopsysMetric.MetricPair("pv_min", pv_min),
        #                 SynopsysMetric.MetricPair("pv_power", pv_power),
        #                 SynopsysMetric.MetricPair("pv_noise", pv_noise),
        #                 ]
        metric_collections = filter(None, metric_collections)
        metric_count = 0
        metric_name = 0

        # This loop is to arrange the files in the correct order
        for metric_pair in metric_collections:
            # Metric_collection needs to be converted to list/tuple from a object reference
            # print("TYPE", type(metric_collection), metric_collection)
            # print("00", metric_collection[0])
            # metric_pair = tuple(metric_collection)
            # for metric_pair in range(len(metric_pair)):
            metric_count += 1
            if "syn" in metric_pair[metric_name]:
                syn.append(metric_pair)

            elif "apr" in metric_pair[metric_name]:
                apr.append(metric_pair)

            elif "drc" in metric_pair[metric_name]:
                drc.append(metric_pair)

            elif "pv_max" in metric_pair[metric_name]:
                pv_max.append(metric_pair)

            elif "pv_min" in metric_pair[metric_name]:
                pv_min.append(metric_pair)

            elif "pv_power" in metric_pair[metric_name]:
                pv_power.append(metric_pair)

            elif "pv_noise" in metric_pair[metric_name]:
                pv_noise.append(metric_pair)

            elif "calibre" in metric_pair[metric_name]:
                calibre.append(metric_pair)

            elif "sta" in metric_pair[metric_name]:
                sta.append(metric_pair)

            elif "Kit" in metric_pair[metric_name]:
                kit.append(metric_pair)

            # elif "Testcase_Name" in metric_pair[metric_name]:
            #     kit.append(metric_pair)
            #
            # elif "DateTime" in metric_pair[metric_name]:
            #     kit.append(metric_pair)
            #
            # elif "Tool" in metric_pair[metric_name]:
            #     kit.append(metric_pair)
            # for metric_pair in metric_pairs:
            #     metric_count += 1
            #     if(SynopsysMetric.organize_metrics(metric_pair.metric_pair, metric_pair[metric_pair][0],
            #                                            metric_pair, metric_pair.state_list)):
            #         break

            # if SynopsysMetric.organize_metrics("syn", metric_pair[metric_pair][0],  metric_pair, syn):
            #     continue
            #

        # If the file name given ends with a '/' or a '\' then os.path.basename() would return "" therefore we do the
        # following "if" statements when gathering the test case name
        if os.path.basename(test_case) != "":
            test_case_name = os.path.basename(test_case)
        else:
            test_case_name = os.path.basename(os.path.dirname(test_case))

        default_metrics_collection = [("Testcase_Name", test_case_name),
                                      ("DateTime", str(datetime.now())), ("Tool", tool)]

        temp_metric_collections.extend(default_metrics_collection + kit + sorted(syn, key=itemgetter(0)) +
                                   sorted(apr, key=itemgetter(0)) + sorted(drc, key=itemgetter(0)) +
                                   sorted(calibre, key=itemgetter(0)) + sorted(pv_max, key=itemgetter(0)) +
                                   sorted(pv_min, key=itemgetter(0)) + sorted(pv_power, key=itemgetter(0)) +
                                   sorted(pv_noise, key=itemgetter(0)) + sorted(sta, key=itemgetter(0)))

        return temp_metric_collections

    # # The last two methods are for future refactoring
    # @staticmethod
    # def organize_metrics(match_metric_name, metric_name, metric_names, stage_list):
    #     result = False
    #
    #     if match_metric_name in metric_names[metric_name][0]:
    #         stage_list.append(metric_names[metric_name])
    #         result = True
    #
    #     return result
    #
    # class MetricPair:
    #     def __init__(self, metric_name, state_list):
    #         self.metric_name = metric_name
    #         self.state_list = state_list
