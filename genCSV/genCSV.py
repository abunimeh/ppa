#!/usr/bin/env python3.3.1
# MAIN

# import os
import sys
# import genCSV
from Metrics.GenerateMetric import GenerateMetric
# sys_args = ["C:\dev\intel\ppa\cadence\mult_1bit_scan(copy)"]

GenerateMetric.determine_testcases(sys.argv)

