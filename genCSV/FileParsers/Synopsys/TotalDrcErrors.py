class TotalDrcErrors:
    @staticmethod
    def get_total_count(metric_list):
        import re
        from Metrics.FormatMetric import FormatMetric
        drc_tot_numb = 0

        for metrics in metric_list:
            if metrics is not None:
                met = tuple(metrics)
                for i in range(len(met)):
                    drc_error_found = re.search(r'^(drc_drcd \(NB\)|drc_trclvs \(NB\)|drc_denall \(NB\)|drc_IPall \(NB\))$', met[i][0], re.I)
                    if drc_error_found:
                        er_number = re.search(r'^([\d]*)$', str(met[i][1]))
                        if er_number:
                            drc_tot_numb += int(er_number.group(1))

        drc_tot_numb = FormatMetric.format_metric_values(drc_tot_numb)
        return drc_tot_numb
