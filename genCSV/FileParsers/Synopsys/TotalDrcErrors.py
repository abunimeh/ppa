def get_total_count(metric_list):
    from FileParsers.Parser import Parser
    import re
    parser = Parser(" ")
    drc_tot_numb = 0
    metric_name = 0
    metric_value = 1

    for metric_pair in metric_list:
        if metric_pair is not None:
            drc_error_found = re.search(r'^(drc_drcd \(NB\)|drc_trclvs \(NB\)|drc_denall \(NB\)|drc_IPall \(NB\))$', metric_pair[metric_name], re.I)
            if drc_error_found:
                er_number = re.search(r'^([\d\.]*)$', str(metric_pair[metric_value]))
                if er_number:
                    drc_tot_numb += float(er_number.group(1))

    drc_tot_numb = parser.format_metric_values(drc_tot_numb)
    return drc_tot_numb
