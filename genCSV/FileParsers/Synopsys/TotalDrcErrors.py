class TotalDrcErrors:
    @staticmethod
    def get_total_count(metric_list):
        import re
        drc_tot_numb = 0

        for metrics in metric_list:
            if metrics is not None:
                met = tuple(metrics)
                for i in range(len(met)):
                    drc_error_found = re.search(r'^(drc_drcd|drc_trclvs|drc_denall|drc_IPall)$', met[i][0], re.I)
                    if drc_error_found:
                        er_number = re.search(r'^([\d]*)$', str(met[i][1]))
                        if er_number:
                            drc_tot_numb += int(er_number.group(1))

        return drc_tot_numb
