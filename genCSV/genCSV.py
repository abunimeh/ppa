#!/usr/bin/env python3.3.1
# MAIN
import argparse

parser = argparse.ArgumentParser(description='Parses the given testcases and creates a csv.')
parser.add_argument('--c', '--config', type=str, help='For a different JSON configuration file use this option along '
                                                      'with the JSON file name.')
parser.add_argument('--d', '--dir_lvls', '--dirs', type=int, help='Enter how many directory levels deep the genCSV script has to '
                                                        'search for the testcases. Defaults to the '
                                                        'Search_Key.Order.default value located in the configuration file'
                                                        '. For example, "-d=1" would be entered for a search_path of '
                                                        '/nfs/d04 when the testcase is located at /nfs/d04/cpu_testcase.')
parser.add_argument('--a', '--auto', action='store_true', help='Automatically find testcases. For each search path '
                                                               'passed in, the script will stop at the first directory '
                                                               'level that has a valid test_case. This option may be '
                                                               'more time consuming and prone to errors.')
parser.add_argument('--comb', '--combine', action='store_true', help='Use this option to combine alike testcases. '
                                                                     'Useful for megatest testcases.')
parser.add_argument('search_paths', type=str, nargs='+', help='Path(s) to search. At least one path has to be entered '
                                                              'for the script to operate.')
args = parser.parse_args()

if __name__ == "__main__":
    import Metrics.GenerateMetric
    Metrics.GenerateMetric.determine_testcases(args.search_paths)