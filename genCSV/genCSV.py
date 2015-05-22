#!/usr/bin/env python3.3.1
# MAIN

# import os
import sys
# import pdb
# import genCSV
from GenerateMetrics import GenerateMetrics
# sys_args = ["C:\dev\intel\ppa\cadence\mult_1bit_scan(copy)"]

GenerateMetrics.determine_testcases(sys.argv)
# pdb.set_trace()
print("HEEEY MAIN")
# If a config.json file is passed in then the program will use that as the configuration file otherwise we use the one
#  located at the script location

