class total_drc_errors:
    @staticmethod
    def get_total_count(metric_list):
        import re
        drc_tot_numb = 0
        for metrics in metric_list:
            met = tuple(metrics)
            for i in range(len(met)):
                drc_error_found = re.search(r'drc.*', met[i][0], re.I)
                if drc_error_found:
                    er_number = re.search(r'([\d]+).*', met[i][1], re.I)
                    if er_number:
                        drc_tot_numb += int(er_number.group(1))
        return drc_tot_numb
