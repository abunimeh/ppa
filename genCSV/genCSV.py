#!/usr/bin/env python3.3.1
# MAIN

# import os
import sys
# import pdb
# import genCSV
from Metrics.GenerateMetric import GenerateMetric
# sys_args = ["C:\dev\intel\ppa\cadence\mult_1bit_scan(copy)"]

GenerateMetric.determine_testcases(sys.argv)
# pdb.set_trace()
# If a config.json file is passed in then the program will use that as the configuration file otherwise we use the one
#  located at the script location

